import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.IntStream;

////////////////////////////////   Solve Sudoku Puzzles   ////////////////////////////////
////////////////////////////////   @author Peter Norvig   ////////////////////////////////
////////////////////////////////     2007, 2021, 2026     ////////////////////////////////

/** 
 ** There are two representations of puzzles that we will use:
 **  1. A gridstring is 81 chars, with characters '0' or '.' for blank and '1' to '9' for digits.
 **  2. A puzzle grid is an int[81] with a digit d (1-9) represented by the integer (1 << (d - 1));
 **     that is, a bit pattern that has a single 1 bit representing the digit.
 **     A blank is represented by the OR of all the digits 1-9, meaning any digit is possible.
 **     While solving the puzzle, some of these digits are eliminated, leaving fewer possibilities.
 **     The puzzle is solved when every square has only a single possibility.
 **
 ** Search for a solution with `search`:
 **   - Fill an empty square with a guessed digit and do constraint propagation.
 **   - If the guess is consistent, search deeper; if not, try a different guess for the square.
 **   - If all guesses fail, back up to the previous level.
 **   - In selecting an empty square, we pick one that has the minimum number of possible digits.
 **     That makes us more likely to fail early if we guess wrong.
 **   - To be able to back up, we need to keep the grid from the previous recursive level.
 **     To save garbage collection, we pre-allocate one grid per level (81 levels) in a `gridpool`.
 **   - We can work in parallel in multiple threads, each with its own gridpool.
 **
 ** Do constraint propagation with `arcConsistent`, `dualConsistent`, and `nakedPairs`.
 **/

public class Sudoku {

    //////////////////////////////// main; command line options //////////////////////////////

    static final String USAGE = """
        usage: java Sudoku -(no)[fghnprstuv] | -[RT]<number> | <filename> ...\n
        Options and filenames are processed left-to-right. Use '-no' to turn an option off
        E.g.: -v turns verify flag on, -nov turns it off. -R and -T require a number. The options:\n
          -g(rid)     Print each puzzle grid and solution grid (default off)
          -h(elp)     Print this usage message
          -n(aked)    Run the naked pairs strategy (default on)
          -p(uzzle)   Print summary stats for each puzzle (default off)
          -r(everse)  Solve the reverse of each puzzle as well as each puzzle itself (default off)
          -s(ummary)  Print per-file summary stats (default on)
          -t(hread)   Print summary stats for each thread (default off)
          -v(erify)   Verify each solution is valid (default on)
          -T<number>  Concurrently run <number> threads (default 28)
          -R<number>  Repeat the solving of each puzzle <number> times (default 1)
          <filename>  Solve all puzzles in filename, which has one puzzle per line""";

    boolean printGrid        = false; // -g
    boolean runNakedPairs    = true;  // -n
    boolean printPuzzleStats = false; // -p
    boolean reversePuzzle    = false; // -r
    boolean printFileStats   = true;  // -s
    boolean printThreadStats = false; // -t
    boolean verifySolution   = true;  // -v
    int     nThreads         = 28;    // -T
    int     repeat           = 1;     // -R

    private volatile boolean headerPrinted = false;
    private static final int WORK_BLOCK_SIZE = 16;
    private static final int BOX_SIZE = 3;

    /** Mutable state owned by exactly one solver thread. **/
    static final class WorkerState {
        final int[] root = new int[N * N];
        final int[][] gridpool = new int[N * N][N * N];
        long backtracks;
        int puzzlesSolved;
    }

    /** Parse command line args and solve puzzles in files. **/
    public static void main(String[] args) throws IOException {
        Sudoku s = new Sudoku();
        
        // Warm up the JIT code cache by solving a puzzle a few times
        String puzzle = "........8..3...4...9..2..6.....79.......612...6.5.2.7...8...5...1.....2.4.5.....3";
        s.solveListWithWorkers(Collections.nCopies(9999, s.parseGrid(puzzle)), 1);
        
        // Process the options and filenames
        for (String arg : args) {
            if (!arg.startsWith("-")) {
                s.solveFile(arg);
            } else {
                boolean value = !arg.startsWith("-no");
                switch (arg.charAt(value ? 1 : 3)) {
                    case 'g' -> s.printGrid        = value;
                    case 'h' -> System.out.println(USAGE);
                    case 'n' -> s.runNakedPairs    = value;
                    case 'p' -> s.printPuzzleStats = value;
                    case 'r' -> s.reversePuzzle    = value;
                    case 's' -> s.printFileStats   = value;
                    case 't' -> s.printThreadStats = value;
                    case 'v' -> s.verifySolution   = value;
                    case 'T' -> s.nThreads = Integer.parseInt(arg.substring(2));
                    case 'R' -> s.repeat   = Integer.parseInt(arg.substring(2));
                    default  -> System.out.println("Unrecognized option: " + arg + "\n" + USAGE);
                }
            }
        }
    }


    //////////////////////////////// Handling Lists of Puzzles ////////////////////////////////

    /** Solve all the puzzles in a file. Report timing statistics. **/
    void solveFile(String filename) throws IOException {
        var grids = readPuzzlesFromFile(filename);
        long startFileTime = System.nanoTime();
        long backtracks = solveListWithWorkers(grids, nThreads);
        if (printFileStats) {
            printStats(grids.size() * repeat, startFileTime, filename, backtracks);
        }
    }    


    /** Use nThreads workers to pull puzzle grids off the list and solve them. 
        Keep track of the number of backtracks each worker does and return the sum. **/
    long solveListWithWorkers(List<int[]> grids, int nThreads) {
        int nGrids = grids.size();
        var nextGrid = new AtomicInteger(0);
        try (var pool = Executors.newFixedThreadPool(nThreads)) {
            var tasks = IntStream.range(0, nThreads)
                .<Callable<Long>>mapToObj(c -> () -> {
                    var worker = new WorkerState();
                    for (int start; (start = nextGrid.getAndAdd(WORK_BLOCK_SIZE)) < nGrids; ) {
                        solveRange(grids, start, Math.min(start + WORK_BLOCK_SIZE, nGrids), worker);
                    }
                    return worker.backtracks;
                }).toList();
            long totalBacktracks = 0;
            for (var future : pool.invokeAll(tasks)) {
                try {
                    totalBacktracks += future.get();
                } catch (ExecutionException e) {
                    throw new RuntimeException("Solver worker failed", e.getCause());
                }
            }
            return totalBacktracks;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Solver thread was interrupted.");
            return 0;
        }
    }

    
    /** Solve grids in [start, end) using one worker in a thread. **/
    void solveRange(List<int[]> grids, int start, int end, WorkerState worker) {
        for (int g = start; g < end; ++g) {
            var grid = grids.get(g);
            for (int i = 0; i < repeat; ++i) {
                long startTime = printPuzzleStats ? System.nanoTime() : 0;
                long startingBacktracks = worker.backtracks;
                initialize(grid, worker.root);
                var solution = search(worker.root, worker, 0);
                if (printPuzzleStats) {
                    printStats(1, startTime, "Puzzle " + (g + 1),
                        worker.backtracks - startingBacktracks);
                }
                if (i == 0 && (printGrid || (verifySolution && !verify(solution, grid)))) {
                    printGrids("Puzzle " + (g + 1), grid, solution);
                }
            }
            ++worker.puzzlesSolved;
        }
    }


    //////////////////////////////// Utility functions ////////////////////////////////

    /** Return an array of all squares in the intersection of these rows and cols **/
    static int[] cross(int[] rows, int[] cols) {
        var result = new int[rows.length * cols.length];
        int i = 0;
        for (int r : rows) {
            for (int c : cols) {
                result[i++] = N * r + c;
            }
        }
        return result;
    }

    /** Return true iff item is an element of array. **/
    static boolean member(int item, int[] array) { return member(item, array, array.length); }

    /** Return true iff item appears within array[0..end). **/
    static boolean member(int item, int[] array, int end) {
        for (int i = 0; i < end; ++i) {
            if (array[i] == item) return true;
        }
        return false;
    }


    //////////////////////////////// Constants ////////////////////////////////

    static final int       N          = 9; // Number of distinct digits, also length of side of grid
    static final int[]     DIGITS     = {1<<0, 1<<1, 1<<2, 1<<3, 1<<4, 1<<5, 1<<6, 1<<7, 1<<8};
    static final int       ALL_DIGITS = 0b111111111;
    static final int[]     ROWS       = IntStream.range(0, N).toArray();
    static final int[]     COLS       = ROWS;
    static final int[]     SQUARES    = IntStream.range(0, N * N).toArray();
    static final int[][]   BLOCKS     = {{0,1,2},{3,4,5},{6,7,8}};
    static final int[][]   ALL_UNITS  = new int[3 * N][];
    static final int[][][] UNITS      = new int[N * N][3][N];
    static final int[][]   PEERS      = new int[N * N][20];
    static final int[]     NUM_DIGITS = new int[ALL_DIGITS + 1];
    static final int[]     HIGHEST_DIGIT = new int[ALL_DIGITS + 1];


    static { // Initialize UNITS, ALL_UNITS, PEERS, NUM_DIGITS, HIGHEST_DIGIT
        int i = 0;
        for (int r : ROWS)   { ALL_UNITS[i++] = cross(new int[]{r}, COLS); }
        for (int c : COLS)   { ALL_UNITS[i++] = cross(ROWS, new int[]{c}); }
        for (int[] rb : BLOCKS) {
            for (int[] cb : BLOCKS) { ALL_UNITS[i++] = cross(rb, cb); }
        }

        for (int s : SQUARES) {
            i = 0;
            for (int[] u : ALL_UNITS) {
                if (member(s, u)) UNITS[s][i++] = u;
            }
        }

        for (int s : SQUARES) {
            i = 0;
            for (int[] u : UNITS[s]) {
                for (int s2 : u) {
                    if (s2 != s && !member(s2, PEERS[s], i)) {
                        PEERS[s][i++] = s2;
                    }
                }
            }
        }

        for (int val = 0; val <= ALL_DIGITS; val++) {
            NUM_DIGITS[val]    = Integer.bitCount(val);
            HIGHEST_DIGIT[val] = Integer.highestOneBit(val);
        }
    }


    //////////////////////////////// Search algorithm ////////////////////////////////

    /** Search for a solution to grid. If there is an unfilled square, select one
     ** and try--that is, search recursively--every possible digit for the square. **/
    int[] search(int[] grid, WorkerState worker, int level) {
        if (grid == null) return null;
        int square = selectSquare(grid);
        if (square == -1) return grid; // All squares filled — puzzle is solved.
        for (int candidates = grid[square]; candidates != 0; candidates &= candidates - 1) {
            int digitMask = candidates & -candidates; // lowest set bit
            System.arraycopy(grid, 0, worker.gridpool[level], 0, grid.length);
            var result = search(fill(worker.gridpool[level], square, digitMask), worker, level + 1);
            if (result != null) return result;
            ++worker.backtracks;
        }
        return null;
    }


    /** Verify that grid is a valid solution to puzzle. **/
    boolean verify(int[] grid, int[] puzzle) {
        if (grid == null) return false;
        for (int s : SQUARES) {
            if (NUM_DIGITS[grid[s]] != 1
                    || (NUM_DIGITS[puzzle[s]] == 1 && grid[s] != puzzle[s])) {
                return false;
            }
        }
        for (int[] u : ALL_UNITS) {
            int unitDigits = 0;
            for (int s : u) { unitDigits |= grid[s]; }
            if (unitDigits != ALL_DIGITS) return false;
        }
        return true;
    }


    /** Choose the unfilled square with the fewest possible values.
     ** Return -1 if all squares are filled (puzzle complete). **/
    int selectSquare(int[] grid) {
        int square = -1;
        int min = N + 1;
        for (int s : SQUARES) {
            int c = NUM_DIGITS[grid[s]];
            if (c == 2) return s;       // Can't do better than 2
            if (c > 1 && c < min) {
                square = s;
                min = c;
            }
        }
        return square;
    }


    /** Fill grid[s] = d. Return grid, or return null if this creates a contradiction. **/
    int[] fill(int[] grid, int square, int digitMask) {
        if (grid == null || (grid[square] & digitMask) == 0) return null;
        grid[square] = digitMask;
        for (int peer : PEERS[square]) {
            if (!eliminate(grid, peer, digitMask)) return null;
        }
        return grid;
    }


    /** Eliminate digit d as a possibility for grid[s].
     ** Run all three constraint-propagation routines.
     ** Return false if a contradiction is detected. **/
    boolean eliminate(int[] grid, int square, int digitMask) {
        if ((grid[square] & digitMask) == 0) return true; // Already eliminated
        grid[square] &= ~digitMask;
        return arcConsistent(grid, square)
            && dualConsistent(grid, square, digitMask)
            && nakedPairs(grid, square);
    }


    //////////////////////////////// Constraint Propagation ////////////////////////////////

    /** Check arc consistency: either s has multiple possibilities, or its single
     ** remaining value can be filled without contradiction. **/
    boolean arcConsistent(int[] grid, int square) {
        int count = NUM_DIGITS[grid[square]];
        return count >= 2 || (count == 1 && fill(grid, square, grid[square]) != null);
    }


    /** After eliminating d from grid[s], ensure d still has at least one valid
     ** position in each of s's units. If exactly one remains, fill it. **/
    boolean dualConsistent(int[] grid, int square, int digitMask) {
        for (int[] unit : UNITS[square]) {
            int possiblePlaces = 0;
            int onlyPlace = -1;
            for (int otherSquare : unit) {
                if ((grid[otherSquare] & digitMask) != 0) {
                    if (++possiblePlaces > 1) break;
                    onlyPlace = otherSquare;
                }
            }
            if (possiblePlaces == 0
                    || (possiblePlaces == 1 && fill(grid, onlyPlace, digitMask) == null)) {
                return false;
            }
        }
        return true;
    }


    /** If two squares in a unit share exactly the same two possible values, eliminate
     ** those values from every other square in that unit. **/
    boolean nakedPairs(int[] grid, int square) {
        if (!runNakedPairs || NUM_DIGITS[grid[square]] != 2) return true;
        int pairMask = grid[square];
        for (int peer : PEERS[square]) {
            if (grid[peer] == pairMask) {
                for (int[] unit : UNITS[square]) {
                    if (member(peer, unit)) {
                        int firstDigitMask = HIGHEST_DIGIT[pairMask];
                        int secondDigitMask = pairMask & ~firstDigitMask;
                        for (int otherSquare : unit) {
                            if (otherSquare != square && otherSquare != peer) {
                                if (!eliminate(grid, otherSquare, firstDigitMask)
                                        || !eliminate(grid, otherSquare, secondDigitMask)) {
                                    return false;
                                }
                            }
                        }
                    }
                }
            }
        }
        return true;
    }


    //////////////////////////////// Input ////////////////////////////////

    /** Read one puzzle per line from filename and return a list of puzzle grids.
     ** if -reverse option is true, also include the reversed puzzle. **/
    List<int[]> readPuzzlesFromFile(String filename) throws IOException {
        try (BufferedReader in = Files.newBufferedReader(Path.of(filename))) {
            var grids = new ArrayList<int[]>(400);
            String gridstring;
            while ((gridstring = in.readLine()) != null) {
                grids.add(parseGrid(gridstring));
                if (reversePuzzle) {
                    grids.add(parseGrid(new StringBuilder(gridstring).reverse().toString()));
                }
            }
            return grids;
        }
    }


    /** Parse a gridstring into a puzzle grid. **/
    int[] parseGrid(String gridstring) {
        var grid = new int[N * N];
        int s = 0;
        for (int i = 0; i < gridstring.length(); ++i) {
            char c = gridstring.charAt(i);
            if ('1' <= c && c <= '9') {
                grid[s++] = DIGITS[c - '1'];
            } else if (c == '0' || c == '.') {
                grid[s++] = ALL_DIGITS;
            }
        }
        if (s != N * N) {
            throw new IllegalArgumentException(
                "Grid string yielded " + s + " squares; expected " + (N * N) + ": \"" + gridstring + "\"");
        }
        return grid;
    }


    /** Initialize a fresh grid from puzzle, then fill known squares to trigger constraint propagation. **/
    void initialize(int[] puzzle, int[] grid) {
        Arrays.fill(grid, ALL_DIGITS);
        for (int s : SQUARES) {
            if (puzzle[s] != ALL_DIGITS) fill(grid, s, puzzle[s]);
        }
    }


    //////////////////////////////// Output and Tests ////////////////////////////////

    /** Print stats: puzzles solved, average µs, KHz, threads, backtracks, and name. **/
    void printStats(int nGrids, long startTime, String name, long backtracks) {
        double usecs = (System.nanoTime() - startTime) / 1_000.0;
        String line = String.format("%7d %6.1f %7.3f %7d %10.1f %s",
            nGrids, usecs / nGrids, 1_000 * nGrids / usecs, nThreads,
            backtracks * 1.0 / nGrids, name);
        synchronized (this) {
            if (!headerPrinted) {
                System.out.println("Puzzles   μsec     KHz Threads Backtracks Name\n"
                                 + "======= ====== ======= ======= ========== ====");
                headerPrinted = true;
            }
            System.out.println(line);
        }
    }


    /** Print the original puzzle grid alongside the solution grid. **/
    void printGrids(String name, int[] puzzle, int[] solution) {
        final String BAR = "------+-------+------";
        final String GAP = "      ";
        if (solution == null) solution = new int[N * N];
        synchronized (this) {
            System.out.format("\n%-22s%s%s\n", name + ":", GAP,
                verify(solution, puzzle) ? "Solution:" : "FAILED:");
            for (int r = 0; r < N; ++r) {
                System.out.println(rowString(puzzle, r) + GAP + rowString(solution, r));
                if (r == 2 || r == 5) System.out.println(BAR + GAP + " " + BAR);
            }
        }
    }


    /** Return a String representing one row of the grid. **/
    String rowString(int[] grid, int r) {
        var row = new StringBuilder(30);
        for (int s = r * N; s < (r + 1) * N; ++s) {
            int candidateCount = NUM_DIGITS[grid[s]];
            char cell = candidateCount == N ? '.' : candidateCount != 1 ? '?' : (char)('1' + Integer.numberOfTrailingZeros(grid[s]));
            row.append(cell);
            row.append(s % N == BOX_SIZE - 1 || s % N == 2 * BOX_SIZE - 1 ? " | " : " ");
        }
        return row.toString();
    }
}
