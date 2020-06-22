# Generate a portmantout word 
# Peter Norvig
# See https://github.com/norvig/pytudes/blob/master/ipynb/Portmantout.ipynb

from collections import defaultdict, Counter
from typing import List, Tuple, Set, Dict, Any

Word = str
class Wordset(set): """A set of words."""
Step = Tuple[int, str] # An (overlap, word) pair.
OVERLAP, WORD = 0, 1 # Indexes of the two parts of a Step.
Path = List[Step] # A list of steps.
Bridge = (int, Step,...) # An excess letter count and step(s), e.g. (1, (2, 'arrow')).
EXCESS, STEPS = 0, slice(1, None) # Indexes of the two parts of a bridge.

W = Wordset(open('wordlist.asc').read().split()) 

def portman(P: Path) -> Word:
    """Compute the portmantout string S from the path P."""
    return ''.join(word[overlap:] for (overlap, word) in P)

def natalie(W: Wordset, start=None) -> Path:
    """Return a portmantout path containing all words in W."""
    precompute(W)
    word = start or first(W.unused)
    used(W, word)
    P = [(0, word)]
    while W.unused:
        steps = unused_step(W, word) or bridging_steps(W, word)
        for (overlap, word) in steps:
            P.append((overlap, word))
            used(W, word)
    return P

def unused_step(W: Wordset, prev_word: Word) -> List[Step]:
    """Return [(overlap, unused_word)] or []."""
    for suf in suffixes(prev_word):
        for unused_word in W.startswith.get(suf, ()):
            overlap = len(suf)
            return [(overlap, unused_word)]
    return []

def bridging_steps(W: Wordset, prev_word: Word) -> List[Step]:
    """The steps from the shortest bridge that bridges 
    from a suffix of prev_word to a prefix of an unused word."""
    bridge = min(W.bridges[suf][pre] 
                 for suf in suffixes(prev_word) if suf in W.bridges
                 for pre in W.bridges[suf] if W.startswith[pre])
    return bridge[STEPS]

def precompute(W):
    """Precompute and cache data structures for W. The .subwords and .bridges
    data structures are static and only need to be computed once; .unused and
    .startswith are dynamic and must be recomputed on each call to `natalie`."""
    if not hasattr(W, 'subwords') or not hasattr(W, 'bridges'): 
        W.subwords = subwords(W)
        W.bridges  = build_bridges(W)
    W.unused       = W - W.subwords
    W.startswith   = compute_startswith(W.unused)
    
def used(W, word):
    """Remove word from `W.unused` and, for each prefix, from `W.startswith[pre]`."""
    assert word in W, f'used "{word}", which is not in the word set'
    if word in W.unused:
        W.unused.remove(word)
        for pre in prefixes(word):
            W.startswith[pre].remove(word)
            if not W.startswith[pre]:
                del W.startswith[pre]
                
def first(iterable, default=None): return next(iter(iterable), default)

def multimap(pairs) -> Dict[Any, set]:
    """Given (key, val) pairs, make a dict of {key: {val,...}}."""
    result = defaultdict(set)
    for key, val in pairs:
        result[key].add(val)
    return result

def compute_startswith(words) -> Dict[str, Set[Word]]: 
    """A dict mapping a prefix to all the words it starts:
    {'somet': {'something', 'sometimes'},...}."""
    return multimap((pre, w) for w in words for pre in prefixes(w))

def subwords(W: Wordset) -> Set[str]:
    """All the words in W that are subparts of some other word."""
    return {subword for w in W for subword in subparts(w) & W}              
    
def suffixes(word) -> List[str]:
    """All non-empty proper suffixes of word, longest first."""
    return [word[i:] for i in range(1, len(word))]

def prefixes(word) -> List[str]:
    """All non-empty proper prefixes of word."""
    return [word[:i] for i in range(1, len(word))]

def subparts(word) -> Set[str]:
    """All non-empty proper substrings of word"""
    return {word[i:j] 
            for i in range(len(word)) 
            for j in range(i + 1, len(word) + (i > 0))}

def splits(word) -> List[Tuple[int, str, str]]: 
    """A sequence of (excess, pre, suf) tuples."""
    return [(excess, word[:i], word[i+excess:])
            for excess in range(len(word) - 1)
            for i in range(1, len(word) - excess)]

def try_bridge(bridges, pre, suf, excess, word, step2=None):
    """Store a new bridge if it has less excess than the previous bridges[pre][suf]."""
    if suf not in bridges[pre] or excess < bridges[pre][suf][EXCESS]:
        bridge = (excess, (len(pre), word))
        if step2: bridge +=  (step2,)
        bridges[pre][suf] = bridge

def build_bridges(W: Wordset, maxlen=5, end='qujvz'):
    """A table of bridges[pre][suf] == (excess, (overlap, word)), e.g.
    bridges['ar']['c'] == (0, (2, 'arc'))."""
    bridges         = defaultdict(dict)
    shortwords      = [w for w in W if len(w) <= maxlen + (w[-1] in end)]
    shortstartswith = compute_startswith(shortwords)
    # One-word bridges
    for word in shortwords: 
        for excess, pre, suf, in splits(word):
            try_bridge(bridges, pre, suf, excess, word)
    # Two-word bridges
    for word1 in shortwords:
        for suf in suffixes(word1): 
            for word2 in shortstartswith[suf]: 
                excess = len(word1) + len(word2) - len(suf) - 2
                A, B = word1[0], word2[-1]
                if A != B:
                    step2 = (len(suf), word2)
                    try_bridge(bridges, A, B, excess, word1, step2)
    return bridges

if __name__ == "__main__":
    W = Wordset(open('wordlist.asc').read().split())
    print(portman(natalie(W)))