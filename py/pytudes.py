# Run "python pytudes.py" to create README.md for pytudes

notebooks = {
 
'Newest': [], # Gets updated automatically
 
'Programming Examples': [
("AlphaCode Automated Programming", 2022, 'AlphaCode.ipynb', "Analysis of AlphaCode's automated solution to a coding problem"),
("Beal's Conjecture Revisited", 2018, 'Beal.ipynb', "A search for counterexamples to Beal's Conjecture"),
('Bicycling Statistics', 2020, 'Bike-Stats.ipynb', 'Visualizing statistics about bike routes'),
("Can't Stop", 2018, 'Cant-Stop.ipynb', 'Optimal play in a dice board game'),
('Chaos with Triangles', 2019, 'Sierpinski.ipynb', 'A surprising appearance of the Sierpinski triangle in a random walk'),
("Conway's Game of Life", 2017, 'Life.ipynb', 'The cellular automata zero-player game'),
('Generating and Solving Mazes', 2020, 'Maze.ipynb', 'Make a maze by generating a random tree superimposed on a grid and solve it'),
("Mel's Konane Board", 2021, 'Konane.ipynb', 'Solving the game of Konane (Hawaiian checkers).'),
("One Letter Off", 2023, 'OneLetterOff.ipynb', "Word game; use of a large language model to generate clues."),
('Photo Focal Lengths', 2020, 'PhotoFocalLengths.ipynb', 'Generate charts of what focal lengths were used on a photo trip'),
('Pickleball Tournament', 2018, 'Pickleball.ipynb', 'Scheduling a doubles tournament fairly and efficiently'),
('Project Euler Utilities', 2017, 'Project%20Euler%20Utils.ipynb', 'My utility functions for the Project Euler problems, including `Primes` and `Factors`'),
("Selecting Names from a Menu", 2022, 'Menu.ipynb', 'Efficiently Selecting Names from a Menu, by typing characters and arrows'),
('Tracking Polls: Electoral Votes', 2020, 'Electoral%20Votes.ipynb', 
 'How many electoral votes would Trump get if he wins the state where he has positive net approval?')],
 
'Advent of Code': [
('Advent of Code 2023', 2023, 'Advent-2023.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2022'),
('Advent of Code 2022', 2022, 'Advent-2022.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2022'),
('Advent of Code 2021', 2021, 'Advent-2021.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2021'),
('Advent of Code 2020', 2020, 'Advent-2020.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2020'),
('Advent of Code 2018', 2018, 'Advent-2018.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2018'),
('Advent of Code 2017', 2017, 'Advent-2017.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2017'),
('Advent of Code 2016', 2016, 'Advent-2016.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2016'),
('Advent of Code Utilities', 2022, 'AdventUtils.ipynb', 'Utility functions for Advent of Code puzzles')],

'Probability and Uncertainty': [
("Effectiveness of Language Models", 2019, 'Goldberg.ipynb', "A re-implementation in Python 3 of Yoav Goldberg's unreasonably effective character-level n-gram language model."),
('A Concrete Introduction to Probability', 2018, 'Probability.ipynb', 'Code and examples of the basic principles of Probability Theory'),
('Probability, Paradox, and the Reasonable Person Principle', 2016, 'ProbabilityParadox.ipynb', 
 'Some classic paradoxes in Probability Theory, and how to think about disagreements'),
('Estimating Probabilities with Simulations', 2020, 'ProbabilitySimulation.ipynb', 'When the sample space is too complex, simulations can estimate probabilities'),
('The Diamond Game: A Probability Puzzle', 2023, 'Diamonds.ipynb', "Finding an optimal strategy for buying bags with unknown numbers of diamonds."),
('The Devil and the Coin Flip Game', 2019, 'Coin%20Flip.ipynb', 'How to beat the Devil at his own game'),
('Dice Baseball', 2020, 'Dice%20Baseball.ipynb', 'Simulating baseball games'),
('Economics Simulation', 2018, 'Economics.ipynb', 'A simulation of a simple economic game'),
("Overtime in American Football", 2024, 'Overtime.ipynb', "In American Football, which team has the advantage in overtime?"),
('Poker Hand Ranking', 2012, "poker.ipynb", 'How do we decide which poker hand wins? Several variants of poker are considered'),
('The Unfinished Game .... of Risk', 2020, "risk.ipynb", "Determining who is likely to win an interminably long game of Risk"),
('WWW: Who Will Win (NBA Title)?', 2019, 'WWW.ipynb', 'Computing the probability of winning the NBA title, for my home town Warriors, or any other team')],

'Logic and Number Puzzles': [
('Cryptarithmetic', 2014, 'Cryptarithmetic.ipynb', 'Substitute digits for letters and make NUM + BER = PLAY'),
("Euler's Sum of Powers Conjecture", 2018, "Euler's%20Conjecture.ipynb", 
 'Solving a 200-year-old puzzle by finding integers that satisfy a<sup>5</sup> + b<sup>5</sup> + c<sup>5</sup> + d<sup>5</sup> = e<sup>5</sup>'),
('Four 4s, Five 5s, and Countdowns', 2020, 'Countdown.ipynb', 'Solving the equation 10 _ 9 _ 8 _ 7 _ 6 _ 5 _ 4 _ 3 _ 2 _ 1 = 2016. From an Alex Bellos puzzle'),
('KenKen (Sudoku-like Puzzle)', 2021, 'KenKen.ipynb', 'A Sudoku-like puzzle, but with arithmetic.'),
('Pairing Socks', 2019, 'Socks.ipynb', 'What is the probability that you will be able to pair up socks as you randomly pull them out of the dryer?'),
('Sicherman Dice', 2018, 'Sicherman%20Dice.ipynb', 'Find a pair of dice that is like a regular pair of dice, only different'),
("Sol Golomb's Rectangle Puzzle", 2014, 'Golomb-Puzzle.ipynb', 'A Puzzle involving placing rectangles of different sizes inside a square'),
('Star Battle (Sudoku-like Puzzle)', 2021, 'StarBattle.ipynb', 'Fill-in-the-grid puzzle similar to Sudoku'),
('Sudoku', 2006, 'Sudoku.ipynb', 'Classic fill-in-the-grid puzzle'),
('Sudoku: 100,000 puzzles/second in Java', 2021, 'SudokuJava.ipynb', 'A version of the Sudoku solver using parallel threads and other optimizations'),
('Square Sum Puzzle', 2020, 'SquareSum.ipynb', 'Place the numbers from 1 to n in a chain (or a circle) such that adjacent pairs sum to a perfect square'),
("When is Cheryl's Birthday?", 2020, 'Cheryl.ipynb', "Solving the *Cheryl's Birthday* logic puzzle"),
('When Cheryl Met Eve: A Birthday Story', 2015, 'Cheryl-and-Eve.ipynb', "Inventing new puzzles in the Style of Cheryl's Birthday"),
('xkcd 1313: Regex Golf', 2015, 'xkcd1313.ipynb', 'Find the smallest regular expression; inspired by Randall Munroe'),
('xkcd 1313: Regex Golf (Part 2: Infinite Problems)', 2015, 'xkcd1313-part2.ipynb', 'Regex Golf: better, faster, funner (with Stefan Pochmann)')],

'Word Puzzles': [
('Boggle / Inverse Boggle', 2020, 'Boggle.ipynb', 'Find all the words on a Boggle board; then find a board with a lot of words'),
('Chemical Element Spelling', 2020, 'ElementSpelling.ipynb', 'Spelling words using the chemical element symbols, like CoIn'),
('Equilength Numbers: FOUR = 4', 2020, 'equilength-numbers.ipynb', 'What number names have the same letter count as the number they name (such as FOUR)?'),
('Gesture Typing', 2017, 'Gesture%20Typing.ipynb', 'What word has the longest path on a gesture-typing smartphone keyboard?'),
('Ghost: A Word game', 2017, 'Ghost.ipynb', 'The word game Ghost (add letters, try to avoid making a word)'),
('How to Do Things with Words: NLP in Python', 2018, 'How%20to%20Do%20Things%20with%20Words.ipynb', 'Spelling Correction, Secret Codes, Word Segmentation, and more'),
('Jotto and Wordle: Word Guessing Games', 2020, 'jotto.ipynb', 'The word guessing game Jotto, and the popular variant Wordle'),
("Let's Code About Bike Locks", 2015, 'Fred%20Buns.ipynb', 'A tale of a bicycle combination lock that uses letters instead of digits. Inspired by Bike Snob NYC'),
('Scrabble: Refactoring a Crossword Game Program', 2017, 'Scrabble.ipynb', 'Refactoring the Scrabble / Word with Friends game from Udacity 212'),
('Spelling Bee', 2020, 'SpellingBee.ipynb', 'Find the highest-scoring board for the NY Times Spelling Bee puzzle'),
('Translating English into Propositional Logic', 2017, 'PropositionalLogic.ipynb', 'Automatically convert informal English sentences into formal Propositional Logic'),
('Winning Wordle', 2022, 'Wordle.ipynb', 'A simple human-usable strategy to always win at Wordle. And an analysis of 2-guess wins'),
("World's Longest Palindrome", 2017, 'pal3.ipynb', 'Searching for a long Panama-style palindrome, this time letter-by-letter'),
("World's Shortest Portmantout Word", 2020, 'Portmantout.ipynb',  'Find a word that squishes together a bunch of words'),
('xkcd 1970: Name Dominoes', 2018, 'xkcd-Name-Dominoes.ipynb', 'Lay out dominoes legally; the dominoes have people names, not numbers')],

'The Riddler (from 538)': [
('Anigrams: Word Chains', 2022, 'Anigrams.ipynb', 'Finding the longest chain of anagrams that each add one letter'),
('Battle Royale', 2017, 'Riddler%20Battle%20Royale.ipynb', 'A puzzle involving allocating your troops and going up against an opponent'),
('CrossProduct', 2021, 'CrossProduct.ipynb', 'A puzzle where digits fill a table, subject to constraints on their products'),
('Flipping Cards; A Guessing Game', 2020, 'flipping.ipynb', 'Can you go through a deck of cards, guessing higher or lower correctly for each card?'),
('Lottery', 2019, 'RiddlerLottery.ipynb',  'Can you find what lottery number tickets these five friends picked?'),
('How Many Soldiers to Beat the Night King?', 2019, 'NightKing.ipynb',  'A battle between the army of the dead and the army of the living'),
('Misanthropic Neighbors', 2017, 'Mean%20Misanthrope%20Density.ipynb', 'How crowded will this neighborhood be, if nobody wants to live next door to anyone else?'),
('Properly Ordered Card Hands', 2018, 'Orderable%20Cards.ipynb', 'Can you get your hand of cards into a nice order with just one move?'),
('Split the States', 2021, 'SplitStates.ipynb', 'Split the US states into two near-halves by area.'),
('Tour de 538', 2020, 'TourDe538.ipynb', 'Solve a puzzle involving the best pace for a bicycle race.'),
('Weighing Twelve Balls', 2020, 'TwelveBalls.ipynb', 
 'A puzzle where you are given some billiard balls and a balance scale, and asked to find the one ball that is heavier or lighter, in a limited number of weighings'),
('War. What is it Good For?', 2020, 'war.ipynb', 'How likely is it to win a game of war in 26 turns?')],

'Computer Science Algorithms and Concepts': [
('BASIC Interpreter', 2017, 'BASIC.ipynb', 'How to write an interpreter for the BASIC programming language'),
('Convex Hull Problem', 2017, 'Convex%20Hull.ipynb', 'A classic Computer Science Algorithm'),
('How to Count Things', 2020, 'How%20To%20Count%20Things.ipynb', 'Combinatorial math: how to count how many things there are, when there are a lot of them'),
('Stable Matching Problem', 2020, 'StableMatching.ipynb', 'What is the best way to pair up two groups with each other, obeying preferences?'),
('Symbolic Algebra, Simplification, and Differentiation', 2017, 'Differentiation.ipynb', 'A computer algebra system that, including symbolic differentiation'),
('Snobol: Bad Grade, Good Experience', 2017, 'Snobol.ipynb', 'As a student, did you ever get a bad grade on a programming assignment?'),
('Traveling Salesperson Problem', 2018, 'TSP.ipynb', 'Another of the classics')]
}

python_files = [
('beal.py',    "Search for counterexamples to Beal's Conjecture", 'http://norvig.com/beal.html'),
('docex.py',   'An obsolete framework for running unit tests, similar to `doctest`'),
('ibol.py',    'An Exercise in Species Barcoding', 'http://norvig.com/ibol.html'),
('lettercount.py', 'Convert Google Ngram Counts to Letter Counts', 'http://norvig.com/mayzner.html'),
('lis.py',     'Lisp Interpreter written in Python', 'http://norvig.com/lispy.html'),
('lispy.py',   'Even Better Lisp Interpreter written in Python', 'http://norvig.com/lispy2.html'),
('lispytest.py', 'Tests for Lisp Interpreters'),
('pal.py',     'Find long palindromes', 'http://norvig.com/palindrome.html'),
('pal2.py',    'Find longer palindromes', 'http://norvig.com/palindrome.html'),
('pal3.py',    'Find even longer palindromes', 'http://norvig.com/palindrome.html'),
('pytudes.py', 'Pre-process text to generate this README.md file.'),
('py2html.py', 'Pretty-printer to format Python files as html'),
('SET.py',     'Analyze the card game SET', 'http://norvig.com/SET.html'),
('spell.py',   'Spelling corrector', 'http://norvig.com/spell-correct.html'),
('sudoku.py',  'Program to solve sudoku puzzles', 'http://norvig.com/sudoku.html'),
('testaccum.py', 'Tests for my failed Python `accumulation display` proposal', 'http://norvig.com/pyacc.html'),
('yaptu.py',   'Yet Another Python Templating Utility'),
]    

def cols(items) -> str: 
    """Make columns"""
    return '|' + '|'.join(items) + '|'

def table(headers, lines) -> str: 
    """Create markdown for a table."""
    return f'\n\n{cols(headers)}\n{cols(["---"]*len(headers))}\n' + '\n'.join(lines)

def format_notebooks() -> str:
    """Tables for all the notebook categories."""
    find_newest(notebooks)
    return '\n'.join(format_category(name) for name in notebooks)

def find_newest(notebooks, year=2022) -> None:
    """Mutate `notebooks['Newest']` to have a collection of newest notebooks."""
    for category in notebooks:
        for line in notebooks[category]:
            if line[1] >= year:
                notebooks['Newest'].append(line)
    notebooks['Newest'].sort(key=lambda line: (-line[1], line[0]))
    
def format_category(category) -> str:
    """Make a table of multiple jupyter/ipython notebooks, under a header."""
    print(f'{len(notebooks[category]):2d} notebooks in {category}')
    return table(('Run', 'Year', category),
                 [format_notebook(*line) for line in notebooks[category]])
    
def format_notebook(title, year, url, comment=''):
    """Make a markdown table entry for a jupyter/ipython notebook."""
    urlb = f'/blob/main/ipynb/{url}'
    co = f'[C](https://colab.research.google.com/github/norvig/pytudes{urlb})'
    gh = f'[G](ipynb/{url})'
    dn = f'[D](https://beta.deepnote.org/launch?template=python_3.6&url=https%3A%2F%2Fgithub.com%2Fnorvig%2Fpytudes%2Fblob%2Fmain%2Fipynb%2F{url})'
    my = f'[M](https://mybinder.org/v2/gh/norvig/pytudes/main?filepath=ipynb%2F{url})'
    nb = f'[N](https://nbviewer.jupyter.org/github/norvig/pytudes{urlb})'
    sm = f'[S](https://studiolab.sagemaker.aws/import/github/norvig/pytudes{urlb})'
    ti = f'<a href="{gh[4:-1]}" title="{comment}">{title}</a>'
    if year == 2022: year = f'<u>{year}</u>'
    return f'| {co} {dn} {my} {nb} {sm} | {year} | {ti} |'

def format_pythons() -> str:
    """Make a table of multiple python programs."""
    print(f'{len(python_files):2d} pyfiles')
    return table(('File', 'Description', 'Documentation'),
                 [format_python(*line) for line in python_files])
    
def format_python(url, description, doc='') -> str:
    """Make a markdown table entry for a .py file."""
    if doc: doc = f'[documentation]({doc})'
    return f'|[{url}](/py/{url})|*{description}*|{doc}|'


body = f"""
<div align="right" style="text-align:right"><i>Peter Norvig
<br><a href="https://github.com/norvig/pytudes/blob/main/LICENSE">MIT License</a><br>2015-2022</i></div>

# pytudes

"An ***étude*** (a French word meaning *study*) is an instrumental musical composition, usually short, of considerable difficulty, 
and designed to provide practice material for perfecting a particular musical skill." — [*Wikipedia*](https://en.wikipedia.org/wiki/%C3%89tude)

This project contains ***pytudes***—Python programs, usually short, for perfecting particular programming skills.

# Who is this for?

To continue the musical analogy, some people think of programming like [Spotify](http://spotify.com): they want to know how to install the app, find a good playlist, and hit the "play" button; after that they don't want to think about it. There are plenty of other tutorials that will tell you how to do the equivalent of that for various programming tasks—this one won't help. But if you think of programming like playing the piano—a craft that can take [years](https://norvig.com/21-days.html) to perfect—then I hope this collection can help.


# Index of Jupyter (IPython) Notebooks

For each notebook you can hover on the title to see a description, or click the title to view on github, or click one of the letters in the left column to launch the notebook on 
[**C**olab](https://colab.research.google.com),
[**D**eepnote](https://deepnote.com),
[**M**ybinder](https://mybinder.org),
[**S**agemaker](https://studiolab.sagemaker.aws/), or
[**N**BViewer](https://nbviewer.jupyter.org/).

{format_notebooks()}

# Index of Python Files

{format_pythons()}

# Etudes for Programmers
I got the idea for the *"etudes"* part of the name from
this [1978 book](https://books.google.com/books/about/Etudes_for_programmers.html?id=u89WAAAAMAAJ)
by [Charles Wetherell](http://demin.ws/blog/english/2012/08/25/interview-with-charles-wetherell)
that was very influential to me when I was first learning to program. I still have my copy.

![](https://images-na.ssl-images-amazon.com/images/I/51ZnZH29dvL._SX394_BO1,204,203,200_.jpg)
"""

output = 'README.md'
print(f'Wrote {open(output, "w").write(body)} characters to {output}')
