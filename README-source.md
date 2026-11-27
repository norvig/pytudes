<!-- README-source.md: edit this file; a GitHub Action runs py/make_readme.py to produce README.md.
     Notebook link syntax:   [Label](Notebook.ipynb){Tooltip shown on hover}
     Notebook.ipynb is a file in ipynb/. Each becomes a GitHub link plus a Colab icon link.
     Notebook links on consecutive lines (or on the same line) are joined with " · ". -->

<div align="right" style="text-align:right"><i>Peter Norvig
<br><a href="https://github.com/norvig/pytudes/blob/main/LICENSE">MIT License</a><br>2015-2026</i></div>

# pytudes

"An ***étude*** (a French word meaning *study*) is an instrumental musical composition, usually short, of considerable difficulty, 
and designed to provide practice material for perfecting a particular musical skill." — [*Wikipedia*](https://en.wikipedia.org/wiki/%C3%89tude)

This project contains ***pytudes***—Python programs, usually short, providing practice pieces for perfecting particular programming prowess.

# Who is this for?

To continue the musical analogy, some people think of programming like [Spotify](http://spotify.com): they want to know how to install the app, find a good playlist, and hit the "play" button; after that they don't want to think about it. There are plenty of other tutorials that will tell you how to do the equivalent of that for various programming tasks—this one won't help. But if you think of programming like playing the piano—a craft that can take [years](https://norvig.com/21-days.html) to perfect—then I hope this collection can help.

# Index of Jupyter (IPython) Notebooks

Click a title to see a notebook on GitHub, or click the
<img src="https://colab.research.google.com/img/colab_favicon_256px.png" height="14" alt="[colab]"> icon next to it to run it in [**Colab**](https://colab.research.google.com) <img src="https://colab.research.google.com/img/colab_favicon_256px.png" height="14" alt="[colab]">.
Hover over a title to see the full name, year, and a description.

### 🆕 New in 2026

- [Approximating Pi with a Fraction](RationalPi.ipynb){Approximating Pi with a Fraction (2026): Using continued fractions to find fractions (like 22/7) that are close to pi.}
  [Integer Palindromes](palsum.ipynb){Integer Palindromes (2026): Finding all palindromic integers with no zero digit (human vs LLM solutions)}
  [Largest prime factor](Euler3.ipynb){Largest prime factor (2026): For beginner programmers: How to find the largest prime factor of a number. Project Euler #3.}
  [Provably Shortest Portmantout Word](Portmantout-optimal.ipynb){Provably Shortest Portmantout Word (2026): AI found a provably shortest portmantout}
  [Truncatable Primes](TruncatablePrimes.ipynb){Truncatable Primes (2026): Prime numbers where you can remove digits and still get primes.}
- **Project Euler:**
  [by me](Euler.ipynb){Project Euler #1–100 by a Human (2026): Solutions to the first 100 Project Euler math/programming problems}
  [by Claude Fable](Euler-Fable.ipynb){Project Euler #1–100 by Fable LLM (2026): Solutions to Project Euler math/programming problems by Claude Fable LLM}
  [by Claude Opus](Euler-Opus.ipynb){Project Euler #1–100 by Opus LLM (2026): Solutions to Project Euler math/programming problems by Claude Opus LLM}
  [by Kimi](Euler-Kimi.ipynb){Project Euler #1–100 by Kimi LLM (2026): Solutions to Project Euler math/programming problems by Kimi LLM}



### 🤖 Large Language Models

- **Coding with AI:**
  [AlphaCode automated programming](AlphaCode.ipynb){AlphaCode Automated Programming (2022): Analysis of AlphaCode's automated solution to a coding problem}
  [The languages of English, math, and programming](Triplets.ipynb){The Languages of English, Math, and Programming (2024): LLMs do better at producing a program to solve this puzzle than they do at solving it directly}
- **Language models:**
  [Effectiveness of language models](Goldberg.ipynb){Effectiveness of Language Models (2019): A re-implementation in Python 3 of Yoav Goldberg's unreasonably effective character-level n-gram language model.}
  [How to do things with words](How to Do Things with Words.ipynb){How to Do Things with Words: NLP in Python (2018): Spelling Correction, Secret Codes, Word Segmentation, and more}
  [One letter off](OneLetterOff.ipynb){One Letter Off (2023): Word game; use of large language model word embeddings to generate clues.}
- **See also:**
  [Project Euler by LLMs](#-project-euler-problems-from-projecteulernet) &nbsp;·&nbsp;
  [Advent of Code 2025 by LLMs](ipynb/Advent-2025-AI.ipynb "Advent of Code 2025: AI LLM Edition: Using large language coding models to solve AoC puzzles") &nbsp;·&nbsp;
  [LLMs and Cheryl's Birthday](ipynb/CherylMind.ipynb "LLMs, Theory of Mind, and Cheryl's Birthday (2024): Do LLMs have enough theory of mind to solve the Cheryl's Birthday puzzle?") &nbsp;·&nbsp;
  [Integer palindromes (human vs. LLM)](ipynb/palsum.ipynb "Integer Palindromes (2026): Finding all palindromic integers with no zero digit (human vs LLM solutions)") &nbsp;·&nbsp;
  [Provably shortest portmantout (found by AI)](ipynb/Portmantout-optimal.ipynb "Provably Shortest Portmantout Word (2026): AI found a provably shortest portmantout")

### 🎲 Probability and Uncertainty

- **Fundamentals:**
  [A concrete introduction](Probability.ipynb){A Concrete Introduction to Probability (2018): Code and examples of the basic principles of Probability Theory}
  [Paradoxes and the reasonable person principle](ProbabilityParadox.ipynb){Probability, Paradox, and the Reasonable Person Principle (2016): Some classic paradoxes in Probability Theory, and how to think about disagreements}
  [Estimating with simulations](ProbabilitySimulation.ipynb){Estimating Probabilities with Simulations (2020): When the sample space is too complex, simulations can estimate probabilities}
  [How to count things](How To Count Things.ipynb){How to Count Things (2020): Combinatorial math: how to count how many things there are, when there are a lot of them}
- **Games of chance:**
  [Poker hand ranking](poker.ipynb){Poker Hand Ranking (2012): How do we decide which poker hand wins? Several variants of poker are considered}
  [The unfinished game of Risk](risk.ipynb){The Unfinished Game .... of Risk (2020): Determining who is likely to win an interminably long game of Risk}
  [The Devil and the coin flip](Coin Flip.ipynb){The Devil and the Coin Flip Game (2019): How to beat the Devil at his own game}
  [The diamond game](Diamonds.ipynb){The Diamond Game: A Probability Puzzle (2023): Finding an optimal strategy for buying bags with unknown numbers of diamonds.}
- **Sports:**
  [Who will win the NBA title?](WWW.ipynb){WWW: Who Will Win (NBA Title)? (2019): Computing the probability of winning the NBA title, for my home town Warriors, or any other team}
  [Overtime in American football](Overtime.ipynb){Overtime in American Football (2024): In American Football, which team has the advantage in overtime?}
  [Dice baseball](Dice Baseball.ipynb){Dice Baseball (2020): Simulating baseball games}
- **Simulations:**
  [Economics simulation](Economics.ipynb){Economics Simulation (2018): A simulation of a simple economic game}
  [Pairing socks](Socks.ipynb){Pairing Socks (2019): What is the probability that you will be able to pair up socks as you randomly pull them out of the dryer?}
  [Cluster sizes in paint by numbers](Paint.ipynb){Counting Cluster Sizes in Paint by Numbers (2024): What is the average cluster size of a random grid of colored squares?}

### 🎄 Advent of Code (Problems from [adventofcode.com](https://adventofcode.com))

- **By year:**
  [2016](Advent-2016.ipynb){Advent of Code 2016: Puzzle site with a coding puzzle each day of Advent, December 2016}
  [2017](Advent-2017.ipynb){Advent of Code 2017: Puzzle site with a coding puzzle each day of Advent, December 2017}
  [2018](Advent-2018.ipynb){Advent of Code 2018: Puzzle site with a coding puzzle each day of Advent, December 2018}
  [2020](Advent-2020.ipynb){Advent of Code 2020: Puzzle site with a coding puzzle each day of Advent, December 2020}
  [2021](Advent-2021.ipynb){Advent of Code 2021: Puzzle site with a coding puzzle each day of Advent, December 2021}
  [2022](Advent-2022.ipynb){Advent of Code 2022: Puzzle site with a coding puzzle each day of Advent, December 2022}
  [2023](Advent-2023.ipynb){Advent of Code 2023: Puzzle site with a coding puzzle each day of Advent, December 2023}
  [2024](Advent-2024.ipynb){Advent of Code 2024: Puzzle site with a coding puzzle each day of Advent, December 2024}
  [2025](Advent-2025.ipynb){Advent of Code 2025: Puzzle site with a coding puzzle for 12 days of Christmas, December 2025}
- **Extras:**
  [2025: solved by AI LLMs](Advent-2025-AI.ipynb){Advent of Code 2025: AI LLM Edition: Using large language coding models to solve AoC puzzles}
  [Utility functions](AdventUtils.ipynb){Advent of Code Utilities (2022): Utility functions for Advent of Code puzzles}

### 🧮 Project Euler (Problems from [projecteuler.net](https://projecteuler.net))

- **Problems #1–100:**
  [by a human](Euler.ipynb){Project Euler #1–100 by a Human (2026): Solutions to the first 100 Project Euler math/programming problems}
  [by Claude Fable](Euler-Fable.ipynb){Project Euler #1–100 by Fable LLM (2026): Solutions to Project Euler math/programming problems by Claude Fable LLM}
  [by Claude Opus](Euler-Opus.ipynb){Project Euler #1–100 by Opus LLM (2026): Solutions to Project Euler math/programming problems by Claude Opus LLM}
  [by Kimi](Euler-Kimi.ipynb){Project Euler #1–100 by Kimi LLM (2026): Solutions to Project Euler math/programming problems by Kimi LLM}
- **For beginners:**
  [Largest prime factor (#3)](Euler3.ipynb){Largest prime factor (2026): For beginner programmers: How to find the largest prime factor of a number. Project Euler #3.}
### 🧩 Logic and Number Puzzles

- **Cheryl's Birthday:**
  [When is Cheryl's birthday?](Cheryl.ipynb){When is Cheryl's Birthday? (2020): Solving the Cheryl's Birthday logic puzzle}
  [When Cheryl met Eve](Cheryl-and-Eve.ipynb){When Cheryl Met Eve: A Birthday Story (2015): Inventing  puzzles in the Style of Cheryl's Birthday}
  [LLMs and theory of mind](CherylMind.ipynb){LLMs, Theory of Mind, and Cheryl's Birthday (2024): Do LLMs have enough theory of mind to solve the Cheryl's Birthday puzzle?}
- **Arithmetic puzzles:**
  [Four 4s, five 5s, and countdowns](Countdown.ipynb){Four 4s, Five 5s, and Countdowns (2020): Solving the equation 10 _ 9 _ 8 _ 7 _ 6 _ 5 _ 4 _ 3 _ 2 _ 1 = 2016. Originally from an Alex Bellos puzzle}
  [Cryptarithmetic](Cryptarithmetic.ipynb){Cryptarithmetic (2014): Substitute digits for letters and make NUM + BER = PLAY}
  [Square sum chains](SquareSum.ipynb){Square Sum Chain Puzzle (2020): Place the numbers from 1 to n in a chain (or a circle) such that adjacent pairs sum to a perfect square}
  [Number bracelets](NumberBracelets.ipynb){Number Bracelets Game (2024): A game involving numbered beads on a circular bracelet.}
  [Sicherman dice](Sicherman Dice.ipynb){Sicherman Dice (2018): Find a pair of dice that is like a regular pair of dice, only different}
  [Sol Golomb's rectangle puzzle](Golomb-Puzzle.ipynb){Sol Golomb's Rectangle Puzzle (2014): A Puzzle involving placing rectangles of different sizes inside a square}
- **Number theory:**
  [Approximating pi with a fraction](RationalPi.ipynb){Approximating Pi with a Fraction (2026): Using continued fractions to find fractions (like 22/7) that are close to pi.}
  [Truncatable primes](TruncatablePrimes.ipynb){Truncatable Primes (2026): Prime numbers where you can remove digits and still get primes.}
  [Stubborn number endings](Stubborn.ipynb){Stubborn number endings (2024): Any number ending in 5 has a square that also ends in 5. What other endings are like this?}
  [The Babylonian number system](Babylonian digits.ipynb){The Babylonian Number System (2022): Translating between Babylonian and traditional number systems.}
- **Famous conjectures:**
  [Beal's conjecture revisited](Beal.ipynb){Beal's Conjecture Revisited (2018): A search for counterexamples to Beal's Conjecture}
  [Euler's sum of powers conjecture](Euler's Conjecture.ipynb){Euler's Sum of Powers Conjecture (2018): Solving a 200-year-old puzzle by finding integers that satisfy a5 + b5 + c5 + d5 = e5}

### 🔲 Grid Puzzles and Board Games

- **Sudoku:**
  [in Python](Sudoku.ipynb){Sudoku (2006): Classic fill-in-the-grid puzzle solved in Python}
  [in Java: 400,000 puzzles/second](SudokuJava.ipynb){Sudoku: 400,000 puzzles/second in Java (2021): A Java version of the Sudoku solver using parallel threads and other optimizations}
- **Sudoku-like puzzles:**
  [KenKen](KenKen.ipynb){KenKen (Sudoku-like Puzzle) (2021): A Sudoku-like puzzle, but with basic arithmetic.}
  [Star Battle](StarBattle.ipynb){Star Battle (Sudoku-like Puzzle) (2021): Fill-in-the-grid puzzle similar to Sudoku}
- **Board games:**
  [Can't Stop](Cant-Stop.ipynb){Can't Stop (2018): Optimal play in a dice board game}
  [Mel's Konane board](Konane.ipynb){Mel's Konane Board (2021): Solving the game of Konane (Hawaiian checkers).}

### 🔤 Word Puzzles

- **Wordle:**
  [Wordle, Evil Wordle, Antiwordle, and Jotto](Jotto.ipynb){Wordle, Evil Wordle, Antiwordle, and Jotto (2020): The word guessing games Wordle, Evil Wordle, Antiwordle, and Jotto}
  [Winning Wordle](Wordle.ipynb){Winning Wordle (2022): A simple human-usable strategy to always win at Wordle. And an analysis of 2-guess wins}
- **Palindromes:**
  [World's longest palindrome](pal3.ipynb){World's Longest Palindrome (2017): Searching for a long Panama-style palindrome, this time letter-by-letter}
  [Integer palindromes](palsum.ipynb){Integer Palindromes (2026): Finding all palindromic integers with no zero digit (human vs LLM solutions)}
- **Portmantout:**
  [Portmantout words](Portmantout.ipynb){A Short Portmantout Word (2020): Find a word that squishes together a bunch of words}
  [AI Provably shortest](Portmantout-optimal.ipynb){Provably Shortest Portmantout Word (2026): Google Gemini Neon AI found a provably shortest portmantout}
  [Claude's Provably shortest](Portmantout-optimal.ipynb){Another version (2026): Claude AI found a provably shortest portmantout}
- **Word games:**
  [Boggle / inverse Boggle](Boggle.ipynb){Boggle / Inverse Boggle (2020): Find all the words on a Boggle board; then find a board with a lot of words}
  [Ghost](Ghost.ipynb){Ghost: A Word game (2017): The word game Ghost (add letters, try to avoid making a word)}
  [Scrabble](Scrabble.ipynb){Scrabble: Refactoring a Crossword Game Program (2017): Refactoring the Scrabble / Word with Friends game from Udacity 212}
  [NYT Spelling Bee](SpellingBee.ipynb){New York Times Spelling Bee (2020): Find the highest-scoring board}
  [Gesture typing](Gesture Typing.ipynb){Gesture Typing (2017): What word has the longest path on a gesture-typing smartphone keyboard?}
- **Wordplay:**
  [Chemical element spelling](ElementSpelling.ipynb){Chemical Element Spelling (2020): Spelling words using the chemical element symbols, like CoIn}
  [Equilength numbers: FOUR = 4](equilength-numbers.ipynb){Equilength Numbers: FOUR = 4 (2020): What number names have the same letter count as the number they name (such as FOUR)?}
  [Let's code about bike locks](Fred Buns.ipynb){Let's Code About Bike Locks (2015): A tale of a bicycle combination lock that uses letters instead of digits. Inspired by Bike Snob NYC}
  [R y clvr ngh t rd ths?](clvr.ipynb){Did you solve it? R y clvr ngh t rd ths sntnc? (2026): Guess famous phrases from letter shapes. Beginner level.}

### 🗞️ The Riddler and xkcd

- **The Riddler (FiveThirtyEight):**
  [Anigrams](Anigrams.ipynb){Anigrams: Word Chains (2022): Finding the longest chain of anagrams that each add one letter}
  [Battle Royale](Riddler Battle Royale.ipynb){Battle Royale (2017): A puzzle involving allocating your troops and going up against an opponent}
  [Climbing wall](ClimbingWall.ipynb){Climbing Wall (2021): How many holds have to be placed to make a path in each climbing event}
  [CrossProduct](CrossProduct.ipynb){CrossProduct (2021): A puzzle where digits fill a table, subject to constraints on their products}
  [Flipping cards](flipping.ipynb){Flipping Cards; A Guessing Game (2020): Can you go through a deck of cards, guessing higher or lower correctly for each card?}
  [Lottery](RiddlerLottery.ipynb){Lottery (2019): Can you find what lottery number tickets these five friends picked?}
  [The Night King](NightKing.ipynb){How Many Soldiers to Beat the Night King? (2019): A battle between the army of the dead and the army of the living}
  [Misanthropic neighbors](Mean Misanthrope Density.ipynb){Misanthropic Neighbors (2017): How crowded will this neighborhood be, if nobody wants to live next door to anyone else?}
  [Organized card hands](Orderable Cards.ipynb){Properly Organized Card Hands (2018): Can you get your hand of cards into a nice order with just one move?}
  [Race track](RaceTrack.ipynb){Race Track (2021): Race virtual cars around a circular track defined on a grid of points.}
  [Split the states](SplitStates.ipynb){Split the States (2021): Split the US states into two near-halves by area.}
  [Tour de 538](TourDe538.ipynb){Tour de 538 (2020): Solve a puzzle involving the best pace for a bicycle race.}
  [Weighing twelve balls](TwelveBalls.ipynb){Weighing Twelve Balls (2020): A puzzle where you are given some billiard balls and a balance scale, and asked to find the one ball that is heavier or lighter, in a limited number of weighings}
  [War](war.ipynb){War. What is it Good For? (2020): How likely is it to win a game of war in 26 turns?}
- **xkcd:**
  [Regex golf (#1313)](xkcd1313.ipynb){xkcd 1313: Regex Golf (2015): Find the smallest regular expression; inspired by Randall Munroe}
  [Regex golf, part 2](xkcd1313-part2.ipynb){xkcd 1313: Regex Golf (Part 2: Infinite Problems) (2015): Regex Golf: better, faster, funner (with Stefan Pochmann)}
  [Name dominoes (#1970)](xkcd-Name-Dominoes.ipynb){xkcd 1970: Name Dominoes (2018): Lay out dominoes legally; the dominoes have people names, not numbers}

### 💻 Computer Science

- **Interpreters and languages:**
  [Lisp interpreter](lispy.ipynb){(How to Write a (Lisp) Interpreter (in Python)) (2026): Tutorial on interpreters.}
  [BASIC interpreter](BASIC.ipynb){BASIC Interpreter (2017): How to write an interpreter for the BASIC programming language}
  [Symbolic algebra and differentiation](Differentiation.ipynb){Symbolic Algebra, Simplification, and Differentiation (2017): A computer algebra system, including symbolic differentiation}
  [Snobol: bad grade, good experience](Snobol.ipynb){Snobol: Bad Grade, Good Experience (2017): As a student, did you ever get a bad grade on a programming assignment?}
- **Classic algorithms:**
  [Traveling salesperson](TSP.ipynb){Traveling Salesperson Problem (2018): Another of the classics}
  [Convex hull](Convex Hull.ipynb){Convex Hull Problem (2017): A classic Computer Science Algorithm}
  [Stable matching](StableMatching.ipynb){Stable Matching Problem (2020): What is the best way to pair up two groups with each other, obeying preferences?}
  [Making mazes](Maze.ipynb){Generating and Solving Mazes (2020): Make a maze by generating a random tree superimposed on a grid and solve it}
- **Software craft:**
  [Docstring fixpoint theory](DocstringFixpoint.ipynb){Docstring Fixpoint Theory (2023): An approach to writing code and docstrings that go together.}
  [Translating English into propositional logic](PropositionalLogic.ipynb){Translating English into Propositional Logic (2017): Automatically convert informal English sentences into formal Propositional Logic}
  [Selecting names from a menu](Menu.ipynb){Selecting Names from a Menu (2022): Efficiently Selecting Names from a Menu, by typing characters and arrows}
  [Scheduling a pickleball tournament](Pickleball.ipynb){Pickleball Tournament (2018): Scheduling a doubles tournament fairly and efficiently}

### 📊 Data and Simulation

- **Data visualization:**
  [Bicycling statistics](Bike-Stats.ipynb){Bicycling Statistics (2020): Visualizing statistics about bike routes}
  [Photo focal lengths](PhotoFocalLengths.ipynb){Photo Focal Lengths (2020): Generate charts of what focal lengths were used on a photo trip}
  [Tracking polls: electoral votes](Electoral Votes.ipynb){Tracking Polls: Electoral Votes (2020): How many electoral votes would Trump get if he wins the state where he has positive net approval?}
- **Emergent patterns:**
  [Conway's Game of Life](Life.ipynb){Conway's Game of Life (2017): The cellular automata zero-player game}
  [Chaos with triangles](Sierpinski.ipynb){Chaos with Triangles (2019): A surprising appearance of the Sierpinski triangle in a random walk}

# Index of Python Files



|File|Description|Documentation|
|---|---|---|
|[beal.py](/py/beal.py)|*Search for counterexamples to Beal's Conjecture*|[documentation](http://norvig.com/beal.html)|
|[docex.py](/py/docex.py)|*An obsolete framework for running unit tests, similar to `doctest`*||
|[ibol.py](/py/ibol.py)|*An Exercise in Species Barcoding*|[documentation](http://norvig.com/ibol.html)|
|[lettercount.py](/py/lettercount.py)|*Convert Google Ngram Counts to Letter Counts*|[documentation](http://norvig.com/mayzner.html)|
|[lis.py](/py/lis.py)|*Lisp Interpreter written in Python*|[documentation](http://norvig.com/lispy.html)|
|[lispy.py](/py/lispy.py)|*Even Better Lisp Interpreter written in Python*|[documentation](http://norvig.com/lispy2.html)|
|[lispytest.py](/py/lispytest.py)|*Tests for Lisp Interpreters*||
|[pal.py](/py/pal.py)|*Find long palindromes*|[documentation](http://norvig.com/palindrome.html)|
|[pal2.py](/py/pal2.py)|*Find longer palindromes*|[documentation](http://norvig.com/palindrome.html)|
|[pal3.py](/py/pal3.py)|*Find even longer palindromes*|[documentation](http://norvig.com/palindrome.html)|
|[pytudes.py](/py/pytudes.py)|*Pre-process text to generate this README.md file.*||
|[py2html.py](/py/py2html.py)|*Pretty-printer to format Python files as html*||
|[SET.py](/py/SET.py)|*Analyze the card game SET*|[documentation](http://norvig.com/SET.html)|
|[spell.py](/py/spell.py)|*Spelling corrector*|[documentation](http://norvig.com/spell-correct.html)|
|[sudoku.py](/py/sudoku.py)|*Program to solve sudoku puzzles*|[documentation](http://norvig.com/sudoku.html)|
|[testaccum.py](/py/testaccum.py)|*Tests for my failed Python `accumulation display` proposal*|[documentation](http://norvig.com/pyacc.html)|
|[yaptu.py](/py/yaptu.py)|*Yet Another Python Templating Utility*||

# Etudes for Programmers

I got the idea for the *"etudes"* part of the name from
this [1978 book](https://books.google.com/books/about/Etudes_for_programmers.html?id=u89WAAAAMAAJ)
by [Charles Wetherell](http://demin.ws/blog/english/2012/08/25/interview-with-charles-wetherell)
that was very influential to me when I was first learning to program. I still have my copy, but
it is now easier to find a [pdf](txt/Etudes.pdf) than a hard copy.

![](https://images-na.ssl-images-amazon.com/images/I/51ZnZH29dvL._SX394_BO1,204,203,200_.jpg)

# Reviews of pytudes

Here's what some people are saying about `pytudes`:
- "What I find interesting is how Peter builds bottom-up solutions using low-level utilities... Reading his code is educational." - [Jeremey Howard](https://en.wikipedia.org/wiki/Jeremy_Howard_(entrepreneur)), co-founder of fast.ai and chief scientist at Kaggle
- "Everything I see from Peter Norvig is just always so incredibly well written and coded." — [Jonathan](https://news.ycombinator.com/user?id=jypepin), [Hacker News](https://news.ycombinator.com/item?id=27379366)
- "Peter Norvig is my go to recommendation when someone is interested in becoming better at solving day to day problems ... I feel his skill of dividing a problem into small pieces and expressing them in code in a natural way is unparalleled." — [mikevin](https://news.ycombinator.com/user?id=mikevin), [Hacker News](https://news.ycombinator.com/item?id=27379366)
- "I've never seen Peter Norvig choose anything but the most elegant and perfect data model for the problem at hand." — [spoonjim](https://news.ycombinator.com/user?id=spoonjim), [Hacker News](https://news.ycombinator.com/item?id=27379366)
- "I just find Norvig's style of "functional Python" lovely in its own way (with noted disregard of Pep8 and other "best practices")" —[raverbashing](https://news.ycombinator.com/user?id=raverbashing), [Hacker News](https://news.ycombinator.com/item?id=25654955)
- "You should check out Norvig's design of computer programs [course on Udacity](https://imp.i115008.net/c/2331964/788805/11298?u=https://www.udacity.com/course/design-of-computer-programs--cs212) where he uses these kinds of puzzle programs to teach programming design concepts. It is a hard but really rewarding course. — [nafizh](https://news.ycombinator.com/user?id=nafizh), [HN ACademy](https://yahnd.com/academy/r/udacity.com/course/design-of-computer-programs--cs212/)
- "Often enough I would think of something [a possible improvement[, but if you worked it out in detail there was some less-obvious reason the code was the way it was... All the code is pretty short, and it's not really 'production code', but it's enough to be an education in craftsmanship at every level."
- [What code samples should programmers read?] "Anything else implemented by Norvig, he's one of the best programmers that I've had the pleasure of reading code from." - [jacquesm](https://news.ycombinator.com/user?id=jacquesm) on [Hacker News](https://news.ycombinator.com/item?id=14487724)
- "Everything I see from Peter Norvig is just always so incredibly well written and coded. Every year looking at his solutions for advent of code [0] brings just so much learnings. Strongly recommend. - [jyepin](https://news.ycombinator.com/user?id=jypepin) [Hacker News](https://news.ycombinator.com/item?id=27379366)
- "I feel his skill of dividing a problem into small pieces and expressing them in code in a natural way is unparalleled." - [mikevin](https://news.ycombinator.com/user?id=mikevin) [Hacker News](https://news.ycombinator.com/item?id=27379366)
