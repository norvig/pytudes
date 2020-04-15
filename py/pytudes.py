# Run "python pytudes.py" to create README.md for pytudes


def nb(title, url, comment=''):
    """Make a table entry for a ipython notebook."""
    urlb = f'/blob/master/ipynb/{url}'
    co = f'[co](https://colab.research.google.com/github/norvig/pytudes{urlb})'
    dn = f'[dn](https://beta.deepnote.org/launch?template=python_3.6&url=https%3A%2F%2Fgithub.com%2Fnorvig%2Fpytudes%2Fblob%2Fmaster%2Fipynb%2F{url}) '
    my = f'[my](https://mybinder.org/v2/gh/norvig/pytudes/master?filepath=ipynb%2F{url})'
    nb = f'[nb](https://nbviewer.jupyter.org/github/norvig/pytudes{urlb})'
    ti = f'<b><a href="ipynb/{url}" title="{comment}">{title}</a></b>'
    return f'| {co} {dn} {my} {nb} | {ti} |'


def py(url, description, doc=''):
    """Make a table entry for a .py file."""
    if doc: doc = f'[documentation]({doc})'
    return f'|[{url}](/blob/master/py/{url})|*{description}*|{doc}|'


body = f'''
<div align="right" style="text-align: right"><i>Peter Norvig<br><a href="https://github.com/norvig/pytudes/blob/master/LICENSE">MIT License</a><br>2015-2020</i></div>

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

|Run|Programming Examples|
|---|--|
{nb('Advent of Code 2018', 'Advent-2018.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2018 ')}
{nb('Advent of Code 2017', 'Advent%202017.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2017')}
{nb('Advent of Code 2016', 'Advent%20of%20Code.ipynb', 'Puzzle site with a coding puzzle each day for Advent 2016*')}
{nb("Beal's Conjecture Revisited", 'Beal.ipynb', "A search for counterexamples to Beal's Conjecture")}
{nb('Bike Speed Versus Grade', 'Bike%20Speed%20versus%20Grade.ipynb', 'How fast can I bike as the route gets steeper?')}
{nb("Can't Stop", 'Cant-Stop.ipynb', 'Optimal play in a dice board game')}
{nb('Chaos with Triangles', 'Sierpinski.ipynb', 'A surprising appearance of the Sierpinski triangle in a random walk between vertexes')}
{nb("Conway's Game of Life", 'Life.ipynb', 'The cellular automata zero-player game')}
{nb('Dice Baseball', 'Dice%20Baseball.ipynb', 'Simulating baseball games')}
{nb('Generating Mazes', 'Maze.ipynb', 'Make a maze by generating a random tree superimposed on a grid')}
{nb('Pickleball Tournament', 'Pickleball.ipynb', 'Scheduling a doubles tournament fairly and efficiently')}
{nb('Project Euler Utilities', 'Project%20Euler%20Utils.ipynb', 'My utility functions for the Project Euler problems, including `Primes` and `Factors`')}
{nb('Properly Ordered Card Hands', 'Orderable%20Cards.ipynb', 'Can you get your hand of cards into a nice order with just one move?')}
{nb('Tracking Trump: Electoral Votes', 'Electoral%20Votes.ipynb', 'How many electoral votes would Trump get if he wins the state where he has positive net approval?')}
{nb('Weighing Twelve Balls', 'TwelveBalls.ipynb', 'A puzzle where you are given some billiard balls and a balance scale, and asked to find the one ball that is heavier or lighter, in a limited number of weighings')}
{nb('WWW: Who Will Win (NBA Title)?', 'WWW.ipynb', 'Computing the probability of winning the NBA title, for my home town Warriors, or any other team')}


|Run | Logic and Number Puzzles|
|--|---|
{nb('Boggle / Inverse Boggle', 'Boggle.ipynb', 'Find all the words on a Boggle board; then find a board with a lot of words')}
{nb('Chemical Element Spelling', 'ElementSpelling.ipynb', 'Spelling words using the chemical element symbols, like CoIn')}
{nb('Cryptarithmetic', 'Cryptarithmetic.ipynb', 'Substitute digits for letters and make NUM + BER = PLAY')}
{nb('Four 4s, Five 5s, and Countdown to 2016', 'Countdown.ipynb', 'Solving the equation 10 _ 9 _ 8 _ 7 _ 6 _ 5 _ 4 _ 3 _ 2 _ 1 = 2016. From an Alex Bellos puzzle')}
{nb('Gesture Typing', 'Gesture%20Typing.ipynb', 'What word has the longest path on a gesture-typing smartphone keyboard?')}
{nb('Ghost', 'Ghost.ipynb', 'The word game Ghost (add letters, try to avoid making a word)')}
{nb('How Many Soldiers Do You Need to Beat the Night King?', 'NightKing.ipynb',  'Investigasting a battle between the army of the dead and the army of the living')}
{nb("Let's Code About Bike Locks", 'Fred%20Buns.ipynb', 'A tale of a bicycle combination lock that uses letters instead of digits. Inspired by Bike Snob NYC')}
{nb('Pairing Socks', 'Socks.ipynb', 'What is the probability that you will be able to pair up socks as you randomly pull them out of the dryer?')}
{nb('Portmantout Words', 'Portmantout.ipynb',  'Find a long word that squishes together a bunch of words')}
{nb('Refactoring a Crossword Game Program', 'Scrabble.ipynb', 'Refactoring the Scrabble / Word with Friends game from Udacity 212')}
{nb('Riddler Lottery', 'RiddlerLottery.ipynb',  'Can you find what lottery number tickets these five friends picked?')}
{nb('Sicherman Dice', 'Sicherman%20Dice.ipynb', 'Find a pair of dice that is like a regular pair of dice, only different')}
{nb("Sol Golomb's Rectangle Puzzle", 'Golomb-Puzzle.ipynb', 'A Puzzle involving placing rectangles of different sizes inside a square')}
{nb('Spelling Bee', 'SpellingBee.ipynb', 'Find the highest-scoring board for the NY Times Spelling Bee puzzle')}
{nb('The Devil and the Coin Flip Game', 'Coin%20Flip.ipynb', 'How to beat the Devil at his own game')}
{nb('The Puzzle of the Misanthropic Neighbors', 'Mean%20Misanthrope%20Density.ipynb', 'How crowded will this neighborhood be, if nobody wants to live next door to anyone else?')}
{nb('The Riddler: Battle Royale', 'Riddler%20Battle%20Royale.ipynb', 'A puzzle involving allocating your troops and going up against an opponent')}
{nb('Translating English Sentences into Propositional Logic Statements', 'PropositionalLogic.ipynb', 'Automatically convert informal English sentences into formal Propositional Logic')}
{nb('How to Do Things with Words: NLP in Python', 'How%20to%20Do%20Things%20with%20Words.ipynb', 'Spelling Correction, Secret Codes, Word Segmentation, and more')}
{nb('When Cheryl Met Eve: A Birthday Story', 'Cheryl-and-Eve.ipynb', "Inventing new puzzles in the Style of Cheryl's Birthday")}
{nb("When is Cheryl's Birthday?", 'Cheryl.ipynb', "Solving the *Cheryl's Birthday* logic puzzle")}
{nb("World's Longest Palindrome", 'pal3.ipynb', 'Searching for a long Panama-style palindrome, this time letter-by-letter')}
{nb('xkcd 1313: Regex Golf (Part 2: Infinite Problems)', 'xkcd1313-part2.ipynb', 'Regex Golf: better, faster, funner. With Stefan Pochmann')}
{nb('xkcd 1313: Regex Golf', 'xkcd1313.ipynb', 'Find the smallest regular expression; inspired by Randall Monroe')}
{nb('xkcd 1970: Name Dominoes', 'xkcd-Name-Dominoes.ipynb', 'Lay out dominoes legally; the dominoes have people names, not numbers')}

|Run|Math Concepts|
|--|--|
{nb('A Concrete Introduction to Probability', 'Probability.ipynb', 'Code and examples of the basic principles of Probability Theory')}
{nb('Probability, Paradox, and the Reasonable Person Principle', 'ProbabilityParadox.ipynb', 'Some classic paradoxes in Probability Theory, and how to think about disagreements')}
{nb('Estimating Probabilities with Simulations', 'ProbabilitySimulation.ipynb', 'When the sample space is too complex, simulations can estimate probabilities')}
{nb('Economics Simulation', 'Economics.ipynb', 'A simulation of a simple economic game')}
{nb("Euler's Sum of Powers Conjecture", "Euler's%20Conjecture.ipynb", 'Solving a 200-year-old puzzle by finding integers that satisfy a<sup>5</sup> + b<sup>5</sup> + c<sup>5</sup> + d<sup>5</sup> = e<sup>5</sup>')}
{nb('How to Count Things', 'How%20To%20Count%20Things.ipynb', 'Combinatorial math: how to count how many things there are, when there are a lot of them')}
{nb('Symbolic Algebra, Simplification, and Differentiation', 'Differentiation.ipynb', 'A computer algebra system that  manipulates expressions, including symbolic differentiation')}

|Run|Computer Science Algorithms and Concepts|
|--|--|
{nb('Bad Grade, Good Experience', 'Snobol.ipynb', 'As a student, did you ever get a bad grade on a programming assignment? (Snobol, Concordance)')}
{nb('BASIC Interpreter', 'BASIC.ipynb', 'How to write an interpreter for the BASIC programming language')}
{nb('The Convex Hull Problem', 'Convex%20Hull.ipynb', 'A classic Computer Science Algorithm')}
{nb('The Stable Matching Problem', 'StableMatching.ipynb', 'What is the best way to pair up two grpups with each other, obeying preferences?')}
{nb('The Traveling Salesperson Problem', 'TSP.ipynb', 'Another of the classics')}

# Index of Python Files

| File | Description | Documentation |
|:--------|:-------------------|----|
{py('beal.py',    "Search for counterexamples to Beal's Conjecture", 'http://norvig.com/beal.html')}
{py('docex.py',   'A framework for running unit tests, similar to `doctest`')}
{py('ibol.py',    'An Exercise in Species Barcoding', 'http://norvig.com/ibol.html')}
{py('lettercount.py', 'Convert Google Ngram Counts to Letter Counts', 'http://norvig.com/mayzner.html')}
{py('lis.py',     'Lisp Interpreter written in Python', 'http://norvig.com/lispy.html')}
{py('lispy.py',   'Even Better Lisp Interpreter written in Python', 'http://norvig.com/lispy2.html')}
{py('lispytest.py', 'Tests for Lisp Interpreters')}
{py('pal.py',     'Find long palindromes', 'http://norvig.com/palindrome.html')}
{py('pal2.py',    'Find longer palindromes', 'http://norvig.com/palindrome.html')}
{py('pal3.py',    'Find even longer palindromes', 'http://norvig.com/palindrome.html')}
{py('pytudes.py', 'Pre-process text to generate this README.md file.')}
{py('py2html.py', 'Pretty-printer to format Python files as html')}
{py('SET.py',     'Analyze the card game SET', 'http://norvig.com/SET.html')}
{py('spell.py',   'Spelling corrector', 'http://norvig.com/spell-correct.html')}
{py('sudoku.py',  'Program to solve sudoku puzzles', 'http://norvig.com/sudoku.html')}
{py('testaccum.py', 'Tests for my failed Python `accumulation display` proposal', 'http://norvig.com/pyacc.html')}
{py('yaptu.py',   'Yet Another Python Templating Utility')}

# Etudes for Programmers

I got the idea for the *"etudes"* part of the name from
this [1978 book](https://books.google.com/books/about/Etudes_for_programmers.html?id=u89WAAAAMAAJ)
by [Charles Wetherell](http://demin.ws/blog/english/2012/08/25/interview-with-charles-wetherell)
that was very influential to me when I was first learning to program. I still have my copy.

![](https://images-na.ssl-images-amazon.com/images/I/51ZnZH29dvL._SX394_BO1,204,203,200_.jpg)
'''

output = 'README.md'
with open(output, 'w') as out:
    out.write(body)
    print(f'Wrote {output}; {len(body)} characters')

    



