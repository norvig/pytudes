import random
import collections 
import itertools 

"""
Game of Set                (Peter Norvig 2010-2015)

How often do sets appear when we deal an array of cards?
How often in the course of playing out the game?

Here are the data types we will use:

    card:    A string, such as '3R=0', meaning "three red striped ovals".
    deck:    A list of cards, initially of length 81.
    layout:  A list of cards, initially of length 12.
    set:     A tuple of 3 cards.
    Tallies: A dict: {12: {True: 33, False: 1}}} means a layout of size 12
             tallied 33 sets and 1 non-set.
"""

#### Cards, dealing cards, and defining the notion of sets.

CARDS = [number + color + shade + symbol 
         for number in '123' 
         for color  in 'RGP' 
         for shade  in '@O=' 
         for symbol in '0SD']

def deal(n, deck): 
    "Deal n cards from the deck."
    return [deck.pop() for _ in range(n)]

def is_set(cards):
    "Are these 3 cards a set? No if any feature has 2 values."
    for f in range(4):
        values = {card[f] for card in cards}
        if len(values) == 2: 
            return False
    return True

def find_set(layout):
    "Return a set found from this layout, if there is one."
    for cards in itertools.combinations(layout, 3):
        if is_set(cards):
            return cards
    return ()

#### Tallying set:no-set ratio

def Tallies(): 
    "A data structure to keep track, for each size, the number of sets and no-sets."
    return collections.defaultdict(lambda: {True: 0, False: 0})

def tally(tallies, layout):
    "Record that a set was found or not found in a layout of given size; return the set."
    s = find_set(layout)
    tallies[len(layout)][bool(s)] += 1
    return s
            
#### Three experiments

def tally_initial_layout(N, sizes=(12, 15)):
    "Record tallies for N initial deals."
    tallies = Tallies()
    deck = list(CARDS)
    for deal in range(N):
        random.shuffle(deck)
        for size in sizes:
            tally(tallies, deck[:size])
    return tallies

def tally_initial_layout_no_prior_sets(N, sizes=(12, 15)):
    """Simulate N initial deals for each size, keeping tallies for Sets and NoSets,
    but only when there was no set with 3 fewer cards."""
    tallies = Tallies()
    deck = list(CARDS)
    for deal in range(N):
        random.shuffle(deck)
        for size in sizes:
            if not find_set(deck[:size-3]):
                tally(tallies, deck[:size])
    return tallies

def tally_game_play(N):
    "Record tallies for the play of N complete games."
    tallies = Tallies()
    for game in range(N):
        deck = list(CARDS)
        random.shuffle(deck)
        layout = deal(12, deck)
        while deck:
            s = tally(tallies, layout)
            # Pick up the cards in the set, if any
            for card in s: layout.remove(card)
            # Deal new cards
            if len(layout) < 12 or not s:
                layout += deal(3, deck)    
    return tallies

def experiments(N):
    show({12: [1, 33], 15: [1, 2500]}, 
         'the instruction booklet')
    show(tally_initial_layout(N), 
         'initial layout')
    show(tally_game_play(N // 25), 
         'game play')
    show(tally_initial_layout_no_prior_sets(N), 
         'initial layout, but no sets before dealing last 3 cards')


def show(tallies, label):
    "Print out the counts."
    print()
    print('Size |  Sets  | NoSets | Set:NoSet ratio for', label)
    print('-----+--------+--------+----------------')
    for size in sorted(tallies):
        y, n = tallies[size][True], tallies[size][False]
        ratio = ('inft' if n==0 else int(round(float(y)/n)))
        print('{:4d} |{:7,d} |{:7,d} | {:4}:1'
              .format(size, y, n, ratio))

def test():
    assert len(CARDS) == 81 == len(set(CARDS))
    assert is_set(('3R=O', '2R=S', '1R=D'))
    assert not is_set(('3R=0', '2R=S', '1R@D'))
    assert find_set(['1PO0', '2G=D', '3R=0', '2R=S', '1R=D']) == ('3R=0', '2R=S', '1R=D')
    assert not find_set(['1PO0', '2G=D', '3R=0', '2R=S', '1R@D'])
    photo = '2P=0 3P=D 2R=0 3GO0 2POD 3R@D 2RO0 2ROS 1P@S 2P@0 3ROS 2GOD 2P@D 1GOD 3GOS'.split()
    assert not find_set(photo)
    assert set(itertools.combinations([1, 2, 3, 4], 3)) == {(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)}
    print('All tests pass.')

test()
experiments(100000)
