from __future__ import print_function
import random, re, bisect, time

try:
    xrange          # Python 2
except NameError:
    xrange = range  # Python 3

"""Produce Panama-ish Palindromes. Copyright (C) 2002-2008, Peter Norvig."""

################ Checking for Palindromes

def is_panama(s):
    "Test if string s is a Panama-ish palindrome."
    return is_palindrome(s) and is_unique(phrases(s))

def is_palindrome(s):
    "Test if a string is a palindrome."
    s1 = canonical(s)
    return s1 == reversestr(s1)

def phrases(s):
    "Break a string s into comma-separated phrases."
    return [phrase.strip() for phrase in s.split(',')]

def canonical(word, sub=re.compile('''[-* \t\n\r.,;!?:()`"']''').sub):
    "The canonical form for comparing: lowercase, no blanks or punctuation."
    return sub('', word).lower()

################ Utilities

def reversestr(x):
    "Reverse a string."
    return x[::-1]

def is_unique(seq):
    "Return true if seq has no duplicate elements."
    return len(seq) == len(set(seq))

def update(obj, **entries):
    "Change attributes of obj, according to the keyword args."
    obj.__dict__.update(entries)
    return obj

################ Reading in a dictionary

class PalDict:
    """A dictionary from which you can find canonical words that start or end
    with a given canonical substring, and find the true name of a
    canonical word with d.truename[canonicalword]."""
    
    def __init__(self, k=1000, filename='npdict.txt'):
        words, rwords, truename = [], [], {'': '', 'panama': 'Panama!'}
        for tword in open(filename).read().splitlines():
            word = canonical(tword)
            words.append(word)
            rwords.append(reversestr(word))
            truename[word] = tword
        words.sort()
        rwords.sort()
        update(self, k=k, words=words, rwords=rwords, truename=truename,
               reversibles={}, rangek=range(k), tryharder=False)

    def startswith(self, prefix):
        """Return up to k canonical words that start with prefix.
        If there are more than k, choose from them at random."""
        return self._k_startingwith(self.words, prefix)

    def endswith(self, rsuffix):
        """Return up to k canonical words that end with the reversed suffix.
        If you want words ending in 'ing', ask for d.endswith('gni').
        If there are more than k, choose from them at random."""
        return map(reversestr, self._k_startingwith(self.rwords, rsuffix))

    def __contains__(self, word):
        return word in self.truename

    def reversible_words(self):
        "Find words that have a reverse in the dict, like {'Camus': 'Sumac'}"
        if not self.reversibles:
            reversibles = self.reversibles
            for rw in self.rwords:
                if rw in self:
                    w = reversestr(rw)
                    if w != rw and w not in reversibles:
                        reversibles[w] = rw
            self.reversibles = reversibles
        return self.reversibles

    def _k_startingwith(self, words, prefix):
        start = bisect.bisect_left(words, prefix)
        end = bisect.bisect(words, prefix + 'zzzz')
        n = end - start
        if self.k >= n: # get all the words that start with prefix
            results = words[start:end]
        else: # sample from words starting with prefix 
            indexes = random.sample(xrange(start, end), self.k)
            results = [words[i] for i in indexes]
        random.shuffle(results)
        ## Consider words that are prefixes of the prefix.
        ## This is very slow, so don't use it until late in the game.
        if self.tryharder:
            for i in range(3, len(prefix)):
                w = prefix[0:i]
                if ((words == self.words and w in self.truename) or
                    (words == self.rwords and reversestr(w) in self.truename)):
                    results.append(w)
        return results

paldict = PalDict() 

def anpdictshort():
    "Find the words that are valid when every phrase must start with 'a'"
    def segment(word):  return [s for s in word.split('a') if s]
    def valid(word): return all(reversestr(s) in segments for s in segment(word))
    words = map(canonical, open('anpdict.txt'))
    segments = set(s for w in words for s in segment(canonical(w)))
    valid_words = [paldict.truename[w] for w in words if valid(w)]
    open('anpdict-short.txt', 'w').write('\n'.join(valid_words))

################ Search for a palindrome

class Panama:
    def __init__(self, L='A man, a plan', R='a canal, Panama', dict=paldict):
        ## .left and .right hold lists of canonical words
        ## .diff holds the number of characters that are not matched,
        ##  positive for words on left, negative for right.
        ## .stack holds (action, side, arg) tuples
        update(self, left=[], right=[], best=0, seen={}, diff=0, stack=[],
               used_reversibles=False, starttime=time.clock(), dict=dict)
        for word in L.split(','):
            self.add('left', canonical(word))
        for rword in reversestr(R).split(','):
            self.add('right', canonical(reversestr(rword)))
        self.consider_candidates()
        
    def search(self, steps=50000000):
        "Search for palindromes."
        for _ in xrange(steps):
            if not self.stack:
                return 'done'
            action, dir, substr, arg = self.stack[-1]
            if action == 'added': # undo the last word added
                self.remove(dir, arg)
            elif action == 'trying' and arg: # try the next word if there is one
                self.add(dir, arg.pop()) and self.consider_candidates()
            elif action == 'trying' and not arg: # otherwise backtrack
                self.stack.pop()
            else:
                raise ValueError(action)

    def add(self, dir, word):
        "add a word"
        if word in self.seen:
            return False
        else:
            getattr(self, dir).append(word)
            self.diff += factor[dir] * len(word)
            self.seen[word] = True
            self.stack.append(('added', dir, '?', word))
            return True

    def remove(self, dir, word):
        "remove a word"
        oldword = getattr(self, dir).pop()
        assert word == oldword
        self.diff -= factor[dir] * len(word)
        del self.seen[word]
        self.stack.pop()
        
    def consider_candidates(self):
        """Push a new state with a set of candidate words onto stack."""
        if self.diff > 0: # Left is longer, consider adding on right
            dir = 'right'
            substr =  self.left[-1][-self.diff:]
            candidates = self.dict.endswith(substr)
        elif self.diff < 0: # Right is longer, consider adding on left
            dir = 'left'
            substr =  reversestr(self.right[-1][0:-self.diff])
            candidates = self.dict.startswith(substr)
        else: # Both sides are same size
            dir = 'left'
            if not self.used_reversibles:
                self.report()
                self.add_reversibles()
            substr = ''
            candidates = self.dict.startswith('')
        if substr == reversestr(substr):
            self.report()
        self.stack.append(('trying', dir, substr, candidates))

    def add_reversibles(self):
        "Add in reversible words."
        print('using reversibles ...')
        for (word, rword) in self.dict.reversible_words().items():
            if word not in self.seen and rword not in self.seen:
                self.add('left', word)
                self.add('right', rword)
        self.used_reversibles = True
        self.stack = []
        print('...done')
                
    def report(self):
        "Report a new palindrome to log file (if it is sufficiently big)."
        N = len(self)
        if N > 13333:
            self.dict.tryharder = True
        if N > self.best and (N > 12500 or N > self.best+500):
            self.best = len(self)
            self.bestphrase = str(self)
            print('%5d phrases (%5d words) in %3d seconds' % (
                self.best, self.bestphrase.count(' ')+1, time.clock() - self.starttime))
            assert is_panama(self.bestphrase)
            f = open('pallog%d.txt' % (id(self) % 10000), 'w')
            f.write(self.bestphrase + '\n')
            f.close()

    def __len__(self):
        return len(self.left) + len(self.right)

    def __str__(self):
        truename = self.dict.truename
        lefts = [truename[w] for w in self.left]
        rights =[truename[w] for w in self.right]
        return ', '.join(lefts + rights[::-1])

factor = {'left': +1, 'right': -1}

# Note that we only allow one truename per canonical name.  Occasionally
# this means we miss a good word (as in "a node" vs. "an ode"), but there
# are only 665 of these truename collisions, and most of them are of the
# form "a mark-up" vs. "a markup" so it seemed better to disallow them.

################ Unit Tests
 
def tests(p=Panama()):
    assert is_panama('A man, a plan, a canal, Panama.')
    assert is_panama('''A (man),     a   plan,,;, a ```canal?'' -- Panama!''')
    assert not is_panama('A man, a plan, a radar, a canal, Panama.')
    assert is_palindrome('A man, a plan, a canal, Panama.')
    assert is_palindrome('radar, radar? radar!')
    assert not is_palindrome('radars')
    assert phrases('A man, a plan, Panama') == ['A man', 'a plan', 'Panama']
    assert canonical('A man, a plan, a canal, Panama') == 'amanaplanacanalpanama'
    assert reversestr('foo') == 'oof'
    assert is_unique([1, 2, 3])
    assert not is_unique([1, 2, 2])
    d = p.dict
    def sameset(a, b): return set(a) == set(b)
    assert 'panama' in d
    assert d.words[0] in d
    assert d.words[-1] in d
    assert sameset(d.startswith('aword'), ['awording', 'awordbreak',
        'awordiness', 'awordage', 'awordplay', 'awordlore', 'awordbook',
        'awordlessness', 'aword', 'awordsmith'])
    assert sameset(d.endswith('ytisob'), ['aglobosity', 'averbosity',
        'asubglobosity', 'anonverbosity', 'agibbosity'])
    d.tryharder = True
    assert sameset(d.startswith('oklahoma'), ['oklahoma', 'okla'])
    d.tryharder = False
    assert d.startswith('oklahoma') == ['oklahoma']
    assert d.startswith('fsfdsfdsfds') == []
    print('all tests pass')

if __name__ == '__main__': 
    p = Panama();
    tests(p)
    p.search()
