from __future__ import print_function
import string, random, os, re, bisect

"""Produce Panama-ish Palindromes. Copyright (C) 2002, Peter Norvig.
See http://www.norvig.com/license.html and http://www.norvig.com/pal-alg.html"""

def is_panama(p):
    "Test if p is a Panama-ish palindrome."
    def is_unique(seq): return len(seq) == len(dict(zip(seq, seq)))
    return (p.endswith('Panama') and is_palindrome(p)
	    and is_unique([s.strip() for s in p.split(',')]))

def is_palindrome(phrase):
    "Test if a phrase is a palindrome."
    cphrase = canonical(phrase)
    return cphrase == reverse(cphrase)

def canonical(word, sub=re.compile('[^A-Za-z0-9]').sub):
    "The canonical form for comparing: lowercase alphanumerics."
    return sub('', word).lower()

def read_dict(filename='npdict.txt'):
    "Read the file into global variables _fw and _bw and _truename."
    global _fw, _bw, _truename
    _fw, _bw, _truename = [], [], {'': ''}
    for word in open(filename).read().splitlines():
        w = canonical(word)
        _fw.append(w)
        _bw.append(reverse(w))
        _truename[w] = word
    _fw.sort(); _bw.sort()
    return len(_fw), len(_bw), len(_truename)

def update(obj, **entries): obj.__dict__.update(entries); return obj

class PalDict:
    """A dictionary from which you can find canonical words that start or end
    with a given canonical substring, and find the true name of a
    canonical word."""
    def __init__(self, fw=None, bw=None, truename=None):
        update(self, fw=fw or _fw, bw=bw or _bw, truename=truename or _truename)

    def startswith(self, prefix, k=100):
        """Return up to k canonical words that start with prefix.
        If there are more than k, choose from them at random."""
        return k_startingwith(k, self.fw, prefix)

    def endswith(self, suffix, k=100):
        """Return up to k canonical words that end with suffix.
        If there are more than k, choose from them at random.
        Both the suffix and the word returned are reversed."""
        return k_startingwith(k, self.bw, suffix)

def k_startingwith(k, words, prefix):
    """Choose up to k words that match the prefix (choose randomly if > k)."""
    start = bisect.bisect(words, prefix)
    end = bisect.bisect(words, prefix + 'zzzz')
    n = end - start
    if k >= n:
        results = words[start:end]
        random.shuffle(results)
    else: # Should really try to avoid duplicates
        results = [words[random.randrange(start, end)] for i in range(k)]
    return results

class Panama:
    def __init__(self, L='A man, a plan', R='a canal, Panama', dict=None):
        left = [canonical(w) for w in L.split(', ')]
        right = [canonical(reverse(w)) for w in reverse(R.split(', '))]
        update(self, left=left, right=right, dict=dict or PalDict(), best=0, 
               seen={}, diff=len(''.join(left)) - len(''.join(right)))
        for word in left + map(reverse, right):
            self.seen[word] = 1

    def missing(self, k=20):
        """Return the substring that is missing, and candidate words."""
        if self.diff >= 0: # Left is longer, missing on right
            substr =  self.left[-1][-self.diff:]
            return substr, self.dict.endswith(substr, k)
        else: # Right is longer, missing on left
            substr =  self.right[-1][self.diff:]
            return substr, self.dict.startswith(substr, k)

    def search(self, k=200):
        "Search for palindromes; consider at most k words at each level."
        self.stack = [self.missing(k)]
        while self.stack:
            substr, words = self.stack[-1]
            if is_palindrome(substr):
                self.report()
            if words:
                self.extend(words.pop(), k)
            elif not self.backtrack():
                return

    def extend(self, word, k):
        "Add a new word (unless we've already seen it)."
        if self.diff >= 0: # Left is longer, add to right
            fword = reverse(word)
            if fword in self.seen: return
            self.diff -= len(fword)
            self.seen[fword] = 1
            self.right.append(word)
            self.stack.append(self.missing(k))
        else: # Right is longer, add to left
            if word in self.seen: return
            self.diff += len(word)
            self.seen[word] = 1
            self.left.append(word)
            self.stack.append(self.missing(k))

    def backtrack(self):
        "Remove the last word added; return 0 if can't backtrack"
        if self.diff >= 0: # Left is longer, pop from left
            if not self.left: return 0
            word = self.left.pop()
            self.diff -= len(word)
            del self.seen[word]
        else: # Right is longer, pop from right
            if not self.right: return 0
            word = self.right.pop()
            self.diff += len(word)
            del self.seen[reverse(word)]
        self.stack.pop()
        return 1

    def report(self):
        "Write current state to log file."
        if len(self) > self.best + 200:
            self.best = len(self)
            print(self.best)
            self.bestphrase = str(self)
            assert is_panama(self.bestphrase)
            f = open('pallog%d.txt' % os.getpid(), 'w')
            f.write(self.bestphrase + '\n')
            f.close()

    def __len__(self):
        return len(self.left) + len(self.right)

    def __str__(self):
        truename = self.dict.truename
        lefts = [truename[w] for w in self.left]
        rights = [truename[reverse(w)] for w in reverse(self.right[:])]
        return ', '.join(lefts + ['*****'] + rights)

def reverse(x):
    "Reverse a list or string."
    if type(x) == type(''):
        return ''.join(reverse(list(x)))
    else:
        x.reverse()
        return x

if __name__ == '__main__': read_dict(); p = Panama(); p.search()
