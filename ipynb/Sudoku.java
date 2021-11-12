import java.io.*;
import java.lang.Integer.*;
import java.util.*;
import java.util.stream.*;
import java.lang.StringBuilder;
import java.util.concurrent.CountDownLatch;

////////////////////////////////   Solve Sudoku Puzzles   ////////////////////////////////
////////////////////////////////   @author Peter Norvig   ////////////////////////////////

/**  There are two representations of puzzles that we will use:
 **  1. A gridstring is 81 chars, with characters '0' or '.' for blank and '1' to '9' for digits.
 **  2. A puzzle grid is an int[81] with a digit d (1-9) represented by the integer (1 << (d - 1));
 **     that is, a bit pattern that has a single 1 bit representing the digit.
 **     A blank is represented by the OR of all the digits 1-9, meaning that any digit is possible.
 **     While solving the puzzle, some of these digits are eliminated, leaving fewer possibilities.
 **     The puzzle is solved when every square has only a single possibility.
 **
 ** Search for a solution with `search`:
 **   - Fill an empty square with a guessed digit and do constraint propagation.
 **   - If the guess is consistent, search deeper; if not, try a different guess for the square.
 **   - If all guesses fail, back up to the previous level.
 **   - In selecting an empty square, we pick one that has the minimum number of possible digits.
 **   - To be able to back up, we need to keep the grid from the previous recursive level.
 **     But we only need to keep one grid for each level, so to save garbage collection,
 **     we pre-allocate one grid per level (there are 81 levels) in a `gridpool`.
 ** Do constraint propagation with `arcConsistent`, `dualConsistent`, and `nakedPairs`.
 **/

public class Sudoku {

//////////////////////////////// main; command line options //////////////////////////////
    
    static final String usage = String.join("\n",
        "usage: java Sudoku -(no)[fghnprstuv] | -[RT]<number> | <filename> ...",
        "E.g., -v turns verify flag on, -nov turns it off. -R and -T require a number. The options:\n",
        "  -f(ile)    Print summary stats for each file (default on)",
        "  -g(rid)    Print each puzzle grid and solution grid (default off)",
        "  -h(elp)    Print this usage message",
        "  -n(aked)   Run naked pairs (default on)",
        "  -p(uzzle)  Print summary stats for each puzzle (default off)",
        "  -r(everse) Solve the reverse of each puzzle as well as each puzzle itself (default off)",
        "  -s(earch)  Run search (default on, but some puzzles can be solved with CSP methods alone)",
        "  -t(hread)  Print summary stats for each thread (default off)",
        "  -u(nitTest)Run a suite of unit tests (default off)",
        "  -v(erify)  Verify each solution is valid (default on)",
        "  -T<number> Concurrently run <number> threads (default 26)",
        "  -R<number> Repeat each puzzle <number> times (default 1)",
        "  <filename> Solve all puzzles in filename, which has one puzzle per line");

    boolean printFileStats   = true;  // -f
    boolean printGrid        = false; // -g
    boolean runNakedPairs    = true;  // -n
    boolean printPuzzleStats = false; // -p
    boolean reversePuzzle    = false; // -r
    boolean runSearch        = true;  // -s
    boolean printThreadStats = false; // -t
    boolean verifySolution   = true;  // -v
    int     nThreads         = 26;    // -T
    int     repeat           = 1;     // -R
    
    int     backtracks       = 0;     // count total backtracks

    /** Parse command line args and solve puzzles in files. **/
    public static void main(String[] args) throws IOException {
        Sudoku s = new Sudoku();
        for (String arg: args) {
            if (!arg.startsWith("-")) {
                s.solveFile(arg);
            } else {
                boolean value = !arg.startsWith("-no");
                switch(arg.charAt(value ? 1 : 3)) {
                    case 'f': s.printFileStats   = value; break;
                    case 'g': s.printGrid        = value; break;
                    case 'h': System.out.println(usage);  break; 
                    case 'n': s.runNakedPairs    = value; break;
                    case 'p': s.printPuzzleStats = value; break;
                    case 'r': s.reversePuzzle    = value; break;
                    case 's': s.runSearch        = value; break;
                    case 't': s.printThreadStats = value; break;
                    case 'u': s.runUnitTests();           break;
                    case 'v': s.verifySolution   = value; break;
                    case 'T': s.nThreads = Integer.parseInt(arg.substring(2)); break;
                    case 'R': s.repeat   = Integer.parseInt(arg.substring(2)); break;
                    default:  System.out.println("Unrecognized option: " + arg + "\n" + usage);
                }
            }
        }
    }


    //////////////////////////////// Handling Lists of Puzzles ////////////////////////////////

    /**  Solve all the puzzles in a file. Report timing statistics. **/
    void solveFile(String filename) throws IOException {
        List<int[]> grids = readFile(filename);
        long startFileTime = System.nanoTime();
        switch(nThreads) {
            case 1:  solveList(grids);                   break;
            default: solveListThreaded(grids, nThreads); break;
        }
        if (printFileStats) printStats(grids.size() * repeat, startFileTime, filename);
    }


    /** Solve a list of puzzles in a single thread. 
     ** repeat -R<number> times; print each puzzle's stats if -p; print grid if -g; verify if -v. **/
    void solveList(List<int[]> grids) {
        int[] puzzle = new int[N * N]; // Used to save a copy of the original grid
        int[][] gridpool = new int[N * N][N * N]; // Reuse grids during the search
        for (int g=0; g<grids.size(); ++g) {
            int grid[] = grids.get(g);
            System.arraycopy(grid, 0, puzzle, 0, grid.length);
            for (int i = 0; i < repeat; ++i) {
                long startTime = printPuzzleStats ? System.nanoTime() : 0;
                int[] solution = initialize(grid);                        // All the real work is
                if (runSearch) solution = search(solution, gridpool, 0); // on these 2 lines.
                if (printPuzzleStats) {
                    printStats(1, startTime, "Puzzle " + (g + 1));
                }
                if (i == 0 && (printGrid || (verifySolution && !verify(solution, puzzle)))) {
                    printGrids("Puzzle " + (g + 1), grid, solution);
                }
            }
        }
    }


    /** Break a list of puzzles into nThreads sublists and solve each sublist in a separate thread. **/
    void solveListThreaded(List<int[]> grids, int nThreads) {
        try {
            final long startTime  = System.nanoTime();
            int nGrids = grids.size();            
            final CountDownLatch latch = new CountDownLatch(nThreads);
            int size = nGrids / nThreads;
            for (int c = 0; c < nThreads; ++c) {
                int end = c == nThreads - 1 ? nGrids : (c + 1) * size;
                final List<int[]> sublist = grids.subList(c * size, end);
                new Thread() {
                    public void run() {
                        solveList(sublist);
                        latch.countDown();
                        if (printThreadStats) {
                            printStats(repeat * sublist.size(), startTime, "Thread");
                        }
                    }
                }.start();
            }
            latch.await(); // Wait for all threads to finish
        } catch (InterruptedException e) {
            System.err.println("And you may ask yourself, 'Well, how did I get here?'");
        }
    }


    //////////////////////////////// Utility functions ////////////////////////////////

    /** Return an array of all squares in the intersection of these rows and cols **/
    int[] cross(int[] rows, int[] cols) {
        int[] result = new int[rows.length * cols.length];
        int i = 0;
        for (int r: rows) { for (int c: cols) { result[i++] = N * r + c; } }
        return result;
    }


    /** Return true iff item is an element of array, or of array[0:end]. **/
    boolean member(int item, int[] array) { return member(item, array, array.length); }
    boolean member(int item, int[] array, int end) {
        for (int i = 0; i<end; ++i) {
            if (array[i] == item) { return true; }
        }
        return false;
    }


    //////////////////////////////// Constants ////////////////////////////////
        
    final int       N          = 9; // Number of cells on a side of grid.
    final int[]     DIGITS     = {1<<0, 1<<1, 1<<2, 1<<3, 1<<4, 1<<5, 1<<6, 1<<7, 1<<8};
    final int       ALL_DIGITS = Integer.parseInt("111111111", 2);
    final int[]     ROWS       = IntStream.range(0, N).toArray();
    final int[]     COLS       = ROWS;
    final int[]     SQUARES    = IntStream.range(0, N * N).toArray();
    final int[][]   BLOCKS     = {{0, 1, 2}, {3, 4, 5}, {6, 7, 8}};
    final int[][]   ALL_UNITS  = new int[3 * N][];
    final int[][][] UNITS      = new int[N * N][3][N];
    final int[][]   PEERS      = new int[N * N][20];
    final int[]     NUM_DIGITS  = new int[ALL_DIGITS + 1];
    final int[]     HIGHEST_DIGIT = new int[ALL_DIGITS + 1];

    {
        // Initialize ALL_UNITS to be an array of the 27 units: rows, columns, and blocks
        int i = 0;
        for (int r: ROWS) {ALL_UNITS[i++] = cross(new int[] {r}, COLS); }
        for (int c: COLS) {ALL_UNITS[i++] = cross(ROWS, new int[] {c}); }
        for (int[] rb: BLOCKS) {for (int[] cb: BLOCKS) {ALL_UNITS[i++] = cross(rb, cb); } }

        // Initialize each UNITS[s] to be an array of the 3 units for square s.
        for (int s: SQUARES) {
            i = 0;
            for (int[] u: ALL_UNITS) {
                if (member(s, u)) UNITS[s][i++] = u;
            }
        }

        // Initialize each PEERS[s] to be an array of the 20 squares that are peers of square s.
        for (int s: SQUARES) {
            i = 0;
            for (int[] u: UNITS[s]) {
                for (int s2: u) {
                    if (s2 != s && !member(s2, PEERS[s], i)) {
                        PEERS[s][i++] = s2;
                    }
                }
            }
        }

        // Initialize NUM_DIGITS[val] to be the number of 1 bits in the bitset val
        // and HIGHEST_DIGIT[val] to the highest bit set in the bitset val
        for (int val = 0; val <= ALL_DIGITS; val++) {
            NUM_DIGITS[val] = Integer.bitCount(val);
            HIGHEST_DIGIT[val] = Integer.highestOneBit(val);
        }
    }


    //////////////////////////////// Search algorithm ////////////////////////////////

    /** Search for a solution to grid. If there is an unfilled square, select one
     ** and try--that is, search recursively--every possible digit for the square. **/
    int[] search(int[] grid, int[][] gridpool, int level) {
        if (grid == null) {
            return null;
        }
        int s = select_square(grid);
        if (s == -1) {
            return grid; // No squares to select means we are done!
        } 
        for (int d: DIGITS) {
            // For each possible digit d that could fill square s, try it
            if ((d & grid[s]) > 0) {
                // Copy grid's contents into gridpool[level], and use that at the next level
                System.arraycopy(grid, 0, gridpool[level], 0, grid.length);
                int[] result = search(fill(gridpool[level], s, d), gridpool, level + 1);
                if (result != null) {
                    return result;
                }
                backtracks += 1;
            }
        }
        return null;
    }


    /** Verify that grid is a solution to the puzzle. **/
    boolean verify(int[] grid, int[] puzzle) {
        if (grid == null) { return false; }
        // Check that all squares have a single digit, and
        // no filled square in the puzzle was changed in the solution.
        for (int s: SQUARES) {
            if ((NUM_DIGITS[grid[s]] != 1) || (NUM_DIGITS[puzzle[s]] == 1 && grid[s] != puzzle[s])) {
                return false;
            }
        }
        // Check that each unit is a permutation of digits
        for (int[] u: ALL_UNITS) {
            int unit_digits = 0; // All the digits in a unit.
            for (int s : u) {unit_digits |= grid[s]; }
            if (unit_digits != ALL_DIGITS) { 
                return false; 
            }
        }
        return true;
    }

    
    /** Choose an unfilled square with the minimum number of possible values. 
     ** If all squares are filled, return -1 (which means the puzzle is complete). **/
    int select_square(int[] grid) {
        int square = -1;
        int min = N + 1;
        for (int s: SQUARES) {
            int c = NUM_DIGITS[grid[s]];
            if (c == 2) {
                return s; // Can't get fewer than 2 possible digits
            } else if (c > 1 && c < min) {
                square = s;
                min = c;
            }
        }
        return square;
    }


    /** fill grid[s] = d. If this leads to contradiction, return null. **/
    int[] fill(int[] grid, int s, int d) {
        if ((grid == null) || ((grid[s] & d) == 0)) { return null; } // d not possible for grid[s]
        grid[s] = d;
        for (int p: PEERS[s]) {
            if (!eliminate(grid, p, d)) { // If we can't eliminate d from all peers of s, then fail
                return null;
            }
        }
        return grid;
    }


    /** Eliminate digit d as a possibility for grid[s]. 
     ** Run the 3 constraint propagation routines.
     ** If constraint propagation detects a contradiction, return false. **/
    boolean eliminate(int[] grid, int s, int d) {
        if ((grid[s] & d) == 0) { return true; } // d already eliminated from grid[s]
        grid[s] -= d;
        return arc_consistent(grid, s) && dual_consistent(grid, s, d) && naked_pairs(grid, s);
    }


    //////////////////////////////// Constraint Propagation ////////////////////////////////

    /** Check if square s is consistent: that is, it has multiple possible values, or it has
     ** one possible value which we can consistently fill. **/
    boolean arc_consistent(int[] grid, int s) {
        int count = NUM_DIGITS[grid[s]];
        return count >= 2 || (count == 1 && (fill(grid, s, grid[s]) != null));
    }


    /** After we eliminate d from possibilities for grid[s], check each unit of s
     ** and make sure there is some position in the unit where d can go.
     ** If there is only one possible place for d, fill it with d. **/
    boolean dual_consistent(int[] grid, int s, int d) {
        for (int[] u: UNITS[s]) {
            int dPlaces = 0; // The number of possible places for d within unit u
            int dplace = -1; // Try to find a place in the unit where d can go
            for (int s2: u) {
                if ((grid[s2] & d) > 0) { // s2 is a possible place for d
                    dPlaces++;
                    if (dPlaces > 1) break;
                    dplace = s2;
                }
            }
            if (dPlaces == 0 || (dPlaces == 1 && (fill(grid, dplace, d) == null))) {
                return false;
            }
        }
        return true;
    }


    /** Look for two squares in a unit with the same two possible values, and no other values.
     ** For example, if s and s2 both have the possible values 8|9, then we know that 8 and 9
     ** must go in those two squares. We don't know which is which, but we can eliminate 
     ** 8 and 9 from any other square s3 that is in the unit. **/
    boolean naked_pairs(int[] grid, int s) {
        if (!runNakedPairs) { return true; }
        int val = grid[s];
        if (NUM_DIGITS[val] != 2) { return true; } // Doesn't apply
        for (int s2: PEERS[s]) {
            if (grid[s2] == val) {
                // s and s2 are a naked pair; find what unit(s) they share
                for (int[] u: UNITS[s]) {
                    if (member(s2, u)) {
                        for (int s3: u) { // s3 can't have either of the values in val (e.g. 8|9)
                            if (s3 != s && s3 != s2) {
                                int d = HIGHEST_DIGIT[val];
                                int d2 = val - d;
                                if (!eliminate(grid, s3, d) || !eliminate(grid, s3, d2)) {
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
    
    /** The method `readFile` reads one puzzle per file line and returns a List of puzzle grids. **/ 
    List<int[]> readFile(String filename) throws IOException {
        BufferedReader in = new BufferedReader(new FileReader(filename));
        List<int[]> grids = new ArrayList<int[]>(1000);
        String gridstring;
        while ((gridstring = in.readLine()) != null) {
            grids.add(parseGrid(gridstring));
            if (reversePuzzle) { 
                grids.add(parseGrid(new StringBuilder(gridstring).reverse().toString()));
            }
        }
        return grids;
    }


    /** Parse a gridstring into a puzzle grid: an int[] with values DIGITS[0-9] or ALL_DIGITS. **/
    int[] parseGrid(String gridstring) {
        int[] grid = new int[N * N];
        int s = 0;
        for (int i = 0; i<gridstring.length(); ++i) {
            char c = gridstring.charAt(i);
            if ('1' <= c && c <= '9') {
                grid[s++] = DIGITS[c - '1']; // A single-bit set to represent a digit
            } else if (c == '0' || c == '.') {
                grid[s++] = ALL_DIGITS; // Any digit is possible
            }
        }
        assert s == N * N;
        return grid;
    }


    /** Initialize a grid from a puzzle.
     ** First initialize every square in the new grid to ALL_DIGITS, meaning any value is possible.
     ** Then, call `fill` on the puzzle's filled squares to initiate constraint propagation.  **/
    int[] initialize(int[] puzzle) {
        int[] grid = new int[N * N]; Arrays.fill(grid, ALL_DIGITS);
        for (int s: SQUARES) { if (puzzle[s] != ALL_DIGITS) { fill(grid, s, puzzle[s]); } }
        return grid;
    }


    //////////////////////////////// Output and Tests ////////////////////////////////

    boolean headerPrinted = false;
    
    /** Print stats on puzzles solved, average time, frequency, threads used, and name. **/
    void printStats(int nGrids, long startTime, String name) {
        double usecs = (System.nanoTime() - startTime) / 1000.;
        String line = String.format("%7d %6.1f %7.3f %7d %10.1f %s", 
                      nGrids, usecs / nGrids, 1000 * nGrids / usecs, nThreads, backtracks * 1. / nGrids, name);
        synchronized (this) { // So that printing from different threads doesn't get garbled
            if (!headerPrinted) {
                System.out.println("Puzzles   μsec     KHz Threads Backtracks Name\n"
                                 + "======= ====== ======= ======= ========== ====");
                headerPrinted = true;
            }
            System.out.println(line);
            backtracks = 0;
        }
    }


    /** Print the original puzzle grid and the solution grid. **/
    void printGrids(String name, int[] puzzle, int[] solution) {
        String bar = "------+-------+------";
        String gap = "      "; // Space between the puzzle grid and solution grid
        if (solution == null) solution = new int[N * N];
        synchronized (this) { // So that printing from different threads doesn't get garbled
            System.out.format("\n%-22s%s%s\n", name + ":", gap, 
                            (verify(solution, puzzle) ? "Solution:" : "FAILED:"));
            for (int r = 0; r < N; ++r) {
                System.out.println(rowString(puzzle, r) + gap + rowString(solution, r));
                if (r == 2 || r == 5) System.out.println(bar + gap + " " + bar);
            }
        }
    }


    /** Return a String representing a row of this puzzle. **/
    String rowString(int[] grid, int r) {
        String row = "";
        for (int s = r * 9; s < (r + 1) * 9; ++s) {
            row += (char) ((NUM_DIGITS[grid[s]] == 9) ? '.' : (NUM_DIGITS[grid[s]] != 1) ? '?' :
                           ('1' + Integer.numberOfTrailingZeros(grid[s])));
            row += (s % 9 == 2 || s % 9 == 5 ? " | " : " ");
        }
        return row;
    }
    
    
    /** Unit Tests. Just getting started with these. **/
    void runUnitTests() {
        assert N == 9;
        assert SQUARES.length == 81;
        for (int s: SQUARES) {
            assert UNITS[s].length == 3;
            assert PEERS[s].length == 20;
        }
        assert Arrays.equals(PEERS[19], 
                new int[] {18, 20, 21, 22, 23, 24, 25, 26, 1, 10, 28, 37, 46, 55, 64, 73, 0, 2, 9, 11});
        assert Arrays.deepToString(UNITS[19]).equals(
                "[[18, 19, 20, 21, 22, 23, 24, 25, 26], [1, 10, 19, 28, 37, 46, 55, 64, 73], [0, 1, 2, 9, 10, 11, 18, 19, 20]]");
        System.out.println("Unit tests pass.");
    }
}