# Run "python pytudes.py" to create README.md for pytudes


def nbs(category, *notebooks):
    """Make a table entry for jupyter/ipython notebooks."""
    header = f'|Run|Year|{category}|\n|---|----|---|\n'
    return header + '\n'.join(nb(*line) for line in notebooks)
    
def nb(title, year, url, comment=''):
    """Make a markdown table entry for a jupyter/ipython notebook."""
    urlb = f'/blob/master/ipynb/{url}'
    co = f'[co](https://colab.research.google.com/github/norvig/pytudes{urlb})'
    dn = f'[dn](https://beta.deepnote.org/launch?template=python_3.6&url=https%3A%2F%2Fgithub.com%2Fnorvig%2Fpytudes%2Fblob%2Fmaster%2Fipynb%2F{url}) '
    my = f'[my](https://mybinder.org/v2/gh/norvig/pytudes/master?filepath=ipynb%2F{url})'
    nb = f'[nb](https://nbviewer.jupyter.org/github/norvig/pytudes{urlb})'
    ti = f'<b><a href="ipynb/{url}" title="{comment}">{title}</a></b>'
    if year == 2020: year = f'<u>{year}</u>'
    return f'| {co} {dn} {my} {nb} | {year} | {ti} |'

def pys(*pyfiles):
    header = '| File | Description | Documentation |\n|:--|:----|----|\n'
    return header +  '\n'.join(py(*line) for line in pyfiles)
    
def py(url, description, doc=''):
    """Make a markdown table entry for a .py file."""
    if doc: doc = f'[documentation]({doc})'
    return f'|[{url}](/blob/master/py/{url})|*{description}*|{doc}|'


body = f"""

<div align="right" style="text-align:right"><i>Peter Norvig<br><a href="https://github.com/norvig/pytudes/blob/master/LICENSE">MIT License</a><br>2015-2020</i></div>

# pytudes

"An *étude* (a French word meaning *study*) is an instrumental musical composition, usually short, of considerable difficulty, and designed to provide practice material for perfecting a particular musical skill." &mdash; [Wikipedia](https://en.wikipedia.org/wiki/%C3%89tude)

This project contains **pytudes**&mdash;Python programs, usually short, for perfecting particular programming skills.
Some programs are in Jupyter (`.ipynb`) notebooks, some in `.py` files. For each notebook you can:
- Click on [co](https://colab.research.google.com) to **run** the file on Colab
- Click on [dn](https://deepnote.com) to **run** the notebook on DeepNote
- Click on [my](https://mybinder.org) to **run** the notebook on MyBinder
- Click on [nb](https://nbviewer.jupyter.org/) to **view** the notebook on NBViewer
- Click on the title to **view** the notebook on github.
- Hover over the title to **view** a description.


# Index of Jupyter (IPython) Notebooks


{nbs('Programming Examples',
('Advent of Code 2018', 2018, 'Advent-2018.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2018 '),
('Advent of Code 2017', 2017, 'Advent%202017.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2017'),
('Advent of Code 2016', 2016, 'Advent%20of%20Code.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2016*'),
("Beal's Conjecture Revisited", 2018, 'Beal.ipynb', "A search for counterexamples to Beal's Conjecture"),
('Bike Speed Versus Grade', 2020, 'Bike%20Speed%20versus%20Grade.ipynb', 'How fast can I bike as the route gets steeper?'),
("Can't Stop", 2018, 'Cant-Stop.ipynb', 'Optimal play in a dice board game'),
('Chaos with Triangles', 2019, 'Sierpinski.ipynb', 'A surprising appearance of the Sierpinski triangle in a random walk between vertexes'),
("Conway's Game of Life", 2017, 'Life.ipynb', 'The cellular automata zero-player game'),
('Generating and Solving Mazes', 2020, 'Maze.ipynb', 'Make a maze by generating a random tree superimposed on a grid and solve it.'),
('Photo Focal Lengths', 2020, 'PhotoFocalLengths.ipynb', 'Generate charts of what focal lengths were used on a photo trip.'),
('Pickleball Tournament', 2018, 'Pickleball.ipynb', 'Scheduling a doubles tournament fairly and efficiently'),
('Project Euler Utilities', 2017, 'Project%20Euler%20Utils.ipynb', 'My utility functions for the Project Euler problems, including `Primes` and `Factors`'),
('Tracking Trump: Electoral Votes', 2020, 'Electoral%20Votes.ipynb', 'How many electoral votes would Trump get if he wins the state where he has positive net approval?'))}

{nbs('Logic and Number Puzzles',
('Cryptarithmetic', 2014, 'Cryptarithmetic.ipynb', 'Substitute digits for letters and make NUM + BER = PLAY'),
('Four 4s, Five 5s, Equilength Numbers, and Countdown to 2016', 2020, 'Countdown.ipynb', 'Solving the equation 10 _ 9 _ 8 _ 7 _ 6 _ 5 _ 4 _ 3 _ 2 _ 1 = 2016. From an Alex Bellos puzzle'),
('Pairing Socks', 2019, 'Socks.ipynb', 'What is the probability that you will be able to pair up socks as you randomly pull them out of the dryer?'),
('Sicherman Dice', 2018, 'Sicherman%20Dice.ipynb', 'Find a pair of dice that is like a regular pair of dice, only different'),
("Sol Golomb's Rectangle Puzzle", 2014, 'Golomb-Puzzle.ipynb', 'A Puzzle involving placing rectangles of different sizes inside a square'),
("When is Cheryl's Birthday? (new: Mad Cheryl)", 2020, 'Cheryl.ipynb', "Solving the *Cheryl's Birthday* logic puzzle"),
('When Cheryl Met Eve: A Birthday Story', 2015, 'Cheryl-and-Eve.ipynb', "Inventing new puzzles in the Style of Cheryl's Birthday"),
('xkcd 1313: Regex Golf', 2015, 'xkcd1313.ipynb', 'Find the smallest regular expression; inspired by Randall Munroe'),
('xkcd 1313: Regex Golf (Part 2: Infinite Problems)', 2015, 'xkcd1313-part2.ipynb', 'Regex Golf: better, faster, funner. With Stefan Pochmann.'))}

{nbs('The Riddler (from 538)',
('Battle Royale', 2017, 'Riddler%20Battle%20Royale.ipynb', 'A puzzle involving allocating your troops and going up against an opponent'),
('Flipping Cards; A Guessing Game', 2020, 'flipping.ipynb', 'Can you go through a deck of cards, guessing higher or lower correctly for each card?'),
('Lottery', 2019, 'RiddlerLottery.ipynb',  'Can you find what lottery number tickets these five friends picked?'),
('How Many Soldiers to Beat the Night King?', 2019, 'NightKing.ipynb',  'A battle between the army of the dead and the army of the living'),
('Properly Ordered Card Hands', 2018, 'Orderable%20Cards.ipynb', 'Can you get your hand of cards into a nice order with just one move?'),
('The Puzzle of the Misanthropic Neighbors', 2017, 'Mean%20Misanthrope%20Density.ipynb', 'How crowded will this neighborhood be, if nobody wants to live next door to anyone else?'),
('Tour de 538', 2020, 'TourDe538.ipynb', 'Solve a puzzle involving the best pace for a bicycle race.'),
('Weighing Twelve Balls', 2020, 'TwelveBalls.ipynb', 'A puzzle where you are given some billiard balls and a balance scale, and asked to find the one ball that is heavier or lighter, in a limited number of weighings'),
('War. Waht is it Good For?', 2020, 'war.ipynb', 'How likely is it to win a game of war in 26 turns?'))}

{nbs('Word Puzzles',
('Boggle / Inverse Boggle', 2020, 'Boggle.ipynb', 'Find all the words on a Boggle board; then find a board with a lot of words'),
('Chemical Element Spelling', 2020, 'ElementSpelling.ipynb', 'Spelling words using the chemical element symbols, like CoIn'),
('Gesture Typing', 2017, 'Gesture%20Typing.ipynb', 'What word has the longest path on a gesture-typing smartphone keyboard?'),
('Ghost: A Word game', 2017, 'Ghost.ipynb', 'The word game Ghost (add letters, try to avoid making a word)'),
('How to Do Things with Words: NLP in Python', 2018, 'How%20to%20Do%20Things%20with%20Words.ipynb', 'Spelling Correction, Secret Codes, Word Segmentation, and more'),
('Jotto: A Word Guessing Game', 2020, 'jotto.ipynb', 'The word guessing game Jotto'),
("Let's Code About Bike Locks", 2015, 'Fred%20Buns.ipynb', 'A tale of a bicycle combination lock that uses letters instead of digits. Inspired by Bike Snob NYC'),
('Scrabble: Refactoring a Crossword Game Program', 2017, 'Scrabble.ipynb', 'Refactoring the Scrabble / Word with Friends game from Udacity 212'),
('Spelling Bee', 2020, 'SpellingBee.ipynb', 'Find the highest-scoring board for the NY Times Spelling Bee puzzle'),
('Translating English into Propositional Logic', 2017, 'PropositionalLogic.ipynb', 'Automatically convert informal English sentences into formal Propositional Logic'),
("World's Longest Palindrome", 2017, 'pal3.ipynb', 'Searching for a long Panama-style palindrome, this time letter-by-letter'),
("World's Shortest Portmantout Word", 2020, 'Portmantout.ipynb',  'Find a word that squishes together a bunch of words'),
('xkcd 1970: Name Dominoes', 2018, 'xkcd-Name-Dominoes.ipynb', 'Lay out dominoes legally; the dominoes have people names, not numbers'))}

{nbs('Probability, Uncertainty, and Counting',
('A Concrete Introduction to Probability', 2018, 'Probability.ipynb', 'Code and examples of the basic principles of Probability Theory'),
('Probability, Paradox, and the Reasonable Person Principle', 2016, 'ProbabilityParadox.ipynb', 'Some classic paradoxes in Probability Theory, and how to think about disagreements'),
('Estimating Probabilities with Simulations', 2020, 'ProbabilitySimulation.ipynb', 'When the sample space is too complex, simulations can estimate probabilities'),
('The Devil and the Coin Flip Game', 2019, 'Coin%20Flip.ipynb', 'How to beat the Devil at his own game'),
('Dice Baseball', 2020, 'Dice%20Baseball.ipynb', 'Simulating baseball games'),
('Economics Simulation', 2018, 'Economics.ipynb', 'A simulation of a simple economic game'),
("Euler's Sum of Powers Conjecture", 2018, "Euler's%20Conjecture.ipynb", 'Solving a 200-year-old puzzle by finding integers that satisfy a<sup>5</sup> + b<sup>5</sup> + c<sup>5</sup> + d<sup>5</sup> = e<sup>5</sup>'),
('How to Count Things', 2020, 'How%20To%20Count%20Things.ipynb', 'Combinatorial math: how to count how many things there are, when there are a lot of them'),
('The Unfinished Game .... of Risk', 2020, "risk.ipynb", "Determining who is likely to win an interminably long game of Risk"),
('WWW: Who Will Win (NBA Title)?', 2019, 'WWW.ipynb', 'Computing the probability of winning the NBA title, for my home town Warriors, or any other team'))}


{nbs('Computer Science Algorithms and Concepts',
('Bad Grade, Good Experience', 2017, 'Snobol.ipynb', 'As a student, did you ever get a bad grade on a programming assignment? (Snobol, Concordance)'),
('BASIC Interpreter', 2017, 'BASIC.ipynb', 'How to write an interpreter for the BASIC programming language'),
('The Convex Hull Problem', 2017, 'Convex%20Hull.ipynb', 'A classic Computer Science Algorithm'),
('The Stable Matching Problem', 2020, 'StableMatching.ipynb', 'What is the best way to pair up two groups with each other, obeying preferences?'),
('Symbolic Algebra, Simplification, and Differentiation', 2017, 'Differentiation.ipynb', 'A computer algebra system that  manipulates expressions, including symbolic differentiation'),
('The Traveling Salesperson Problem', 2018, 'TSP.ipynb', 'Another of the classics'))}


# Index of Python Files

{pys(
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
('yaptu.py',   'Yet Another Python Templating Utility'))}

# Etudes for Programmers
I got the idea for the *"etudes"* part of the name from
this [1978 book](https://books.google.com/books/about/Etudes_for_programmers.html?id=u89WAAAAMAAJ)
by [Charles Wetherell](http://demin.ws/blog/english/2012/08/25/interview-with-charles-wetherell)
that was very influential to me when I was first learning to program. I still have my copy.

![](https://images-na.ssl-images-amazon.com/images/I/51ZnZH29dvL._SX394_BO1,204,203,200_.jpg)
"""

output = 'README.md'
with open(output, 'w') as out:
    print(f'Wrote {output}; {out.write(body)}, characters')
