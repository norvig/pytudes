"""
Code to accompany the chapter "Natural Language Corpus Data"
from the book "Beautiful Data" (Segaran and Hammerbacher, 2009)
http://oreilly.com/catalog/9780596157111/

Code copyright (c) 2008-2009 by Peter Norvig

You are free to use this code under the MIT licencse: 
http://www.opensource.org/licenses/mit-license.php
"""
from __future__ import print_function

import re, string, random, glob, operator, heapq
from collections import defaultdict
from math import log10

def memo(f):
    "Memoize function f."
    table = {}
    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]
    fmemo.memo = table
    return fmemo

def test(verbose=None):
    """Run some tests, taken from the chapter.
    Since the hillclimbing algorithm is randomized, some tests may fail."""
    import doctest
    print('Running tests...')
    doctest.testfile('ngrams-test.txt', verbose=verbose)

################ Word Segmentation (p. 223)

@memo
def segment(text):
    "Return a list of words that is the best segmentation of text."
    if not text: return []
    candidates = ([first]+segment(rem) for first,rem in splits(text))
    return max(candidates, key=Pwords)

def splits(text, L=20):
    "Return a list of all possible (first, rem) pairs, len(first)<=L."
    return [(text[:i+1], text[i+1:]) 
            for i in range(min(len(text), L))]

def Pwords(words): 
    "The Naive Bayes probability of a sequence of words."
    return product(Pw(w) for w in words)

#### Support functions (p. 224)

def product(nums):
    "Return the product of a sequence of numbers."
    return reduce(operator.mul, nums, 1)

class Pdist(dict):
    "A probability distribution estimated from counts in datafile."
    def __init__(self, data=[], N=None, missingfn=None):
        for key,count in data:
            self[key] = self.get(key, 0) + int(count)
        self.N = float(N or sum(self.itervalues()))
        self.missingfn = missingfn or (lambda k, N: 1./N)
    def __call__(self, key): 
        if key in self: return self[key]/self.N  
        else: return self.missingfn(key, self.N)

def datafile(name, sep='\t'):
    "Read key,value pairs from file."
    for line in file(name):
        yield line.split(sep)

def avoid_long_words(key, N):
    "Estimate the probability of an unknown word."
    return 10./(N * 10**len(key))

N = 1024908267229 ## Number of tokens

Pw  = Pdist(datafile('count_1w.txt'), N, avoid_long_words)

#### segment2: second version, with bigram counts, (p. 226-227)

def cPw(word, prev):
    "Conditional probability of word, given previous word."
    try:
        return P2w[prev + ' ' + word]/float(Pw[prev])
    except KeyError:
        return Pw(word)

P2w = Pdist(datafile('count_2w.txt'), N)

@memo 
def segment2(text, prev='<S>'): 
    "Return (log P(words), words), where words is the best segmentation." 
    if not text: return 0.0, [] 
    candidates = [combine(log10(cPw(first, prev)), first, segment2(rem, first)) 
                  for first,rem in splits(text)] 
    return max(candidates) 

def combine(Pfirst, first, Prem__rem): 
    "Combine first and rem results into one (probability, words) pair."
    (Prem, rem) = Prem__rem
    return Pfirst+Prem, [first]+rem

################ Secret Codes (p. 228-230)

def encode(msg, key): 
    "Encode a message with a substitution cipher." 
    return msg.translate(string.maketrans(ul(alphabet), ul(key))) 

def ul(text): return text.upper() + text.lower() 

alphabet = 'abcdefghijklmnopqrstuvwxyz' 

def shift(msg, n=13): 
    "Encode a message with a shift (Caesar) cipher." 
    return encode(msg, alphabet[n:]+alphabet[:n]) 

def logPwords(words): 
    "The Naive Bayes probability of a string or sequence of words." 
    if isinstance(words, str): words = allwords(words) 
    return sum(log10(Pw(w)) for w in words) 

def allwords(text): 
    "Return a list of alphabetic words in text, lowercase." 
    return re.findall('[a-z]+', text.lower()) 

def decode_shift(msg): 
    "Find the best decoding of a message encoded with a shift cipher." 
    candidates = [shift(msg, n) for n in range(len(alphabet))] 
    return max(candidates, key=logPwords) 

def shift2(msg, n=13): 
    "Encode with a shift (Caesar) cipher, yielding only letters [a-z]." 
    return shift(just_letters(msg), n) 

def just_letters(text): 
    "Lowercase text and remove all characters except [a-z]." 
    return re.sub('[^a-z]', '', text.lower()) 

def decode_shift2(msg): 
    "Decode a message encoded with a shift cipher, with no spaces." 
    candidates = [segment2(shift(msg, n)) for n in range(len(alphabet))] 
    p, words = max(candidates) 
    return ' '.join(words) 

#### General substitution cipher (p. 231-233)

def logP3letters(text): 
    "The log-probability of text using a letter 3-gram model." 
    return sum(log10(P3l(g)) for g in ngrams(text, 3)) 

def ngrams(seq, n):
    "List all the (overlapping) ngrams in a sequence."
    return [seq[i:i+n] for i in range(1+len(seq)-n)]

P3l = Pdist(datafile('count_3l.txt')) 
P2l = Pdist(datafile('count_2l.txt')) ## We'll need it later 

def hillclimb(x, f, neighbors, steps=10000): 
    "Search for an x that maximizes f(x), considering neighbors(x)." 
    fx = f(x) 
    neighborhood = iter(neighbors(x)) 
    for i in range(steps): 
        x2 = neighborhood.next() 
        fx2 = f(x2) 
        if fx2 > fx: 
            x, fx = x2, fx2 
            neighborhood = iter(neighbors(x)) 
    if debugging: print('hillclimb:', x, int(fx)) 
    return x 

debugging = False 

def decode_subst(msg, steps=4000, restarts=90): 
    "Decode a substitution cipher with random restart hillclimbing." 
    msg = cat(allwords(msg)) 
    candidates = [hillclimb(encode(msg, key=cat(shuffled(alphabet))), 
                            logP3letters, neighboring_msgs, steps) 
                  for _ in range(restarts)] 
    p, words = max(segment2(c) for c in candidates) 
    return ' '.join(words) 

def shuffled(seq): 
    "Return a randomly shuffled copy of the input sequence." 
    seq = list(seq) 
    random.shuffle(seq) 
    return seq 

cat = ''.join 

def neighboring_msgs(msg): 
    "Generate nearby keys, hopefully better ones." 
    def swap(a,b): return msg.translate(string.maketrans(a+b, b+a)) 
    for bigram in heapq.nsmallest(20, set(ngrams(msg, 2)), P2l): 
        b1,b2 = bigram 
        for c in alphabet: 
            if b1==b2: 
                if P2l(c+c) > P2l(bigram): yield swap(c,b1) 
            else: 
                if P2l(c+b2) > P2l(bigram): yield swap(c,b1) 
                if P2l(b1+c) > P2l(bigram): yield swap(c,b2) 
    while True: 
        yield swap(random.choice(alphabet), random.choice(alphabet)) 

################ Spelling Correction (p. 236-)

def corrections(text): 
    "Spell-correct all words in text." 
    return re.sub('[a-zA-Z]+', lambda m: correct(m.group(0)), text) 

def correct(w): 
    "Return the word that is the most likely spell correction of w." 
    candidates = edits(w).items() 
    c, edit = max(candidates, key=lambda (c,e): Pedit(e) * Pw(c)) 
    return c 

def Pedit(edit): 
    "The probability of an edit; can be '' or 'a|b' or 'a|b+c|d'." 
    if edit == '': return (1. - p_spell_error) 
    return p_spell_error*product(P1edit(e) for e in edit.split('+')) 

p_spell_error = 1./20. 

P1edit = Pdist(datafile('count_1edit.txt')) ## Probabilities of single edits 

def edits(word, d=2): 
    "Return a dict of {correct: edit} pairs within d edits of word." 
    results = {} 
    def editsR(hd, tl, d, edits): 
        def ed(L,R): return edits+[R+'|'+L] 
        C = hd+tl 
        if C in Pw: 
            e = '+'.join(edits) 
            if C not in results: results[C] = e 
            else: results[C] = max(results[C], e, key=Pedit) 
        if d <= 0: return 
        extensions = [hd+c for c in alphabet if hd+c in PREFIXES] 
        p = (hd[-1] if hd else '<') ## previous character 
        ## Insertion 
        for h in extensions: 
            editsR(h, tl, d-1, ed(p+h[-1], p)) 
        if not tl: return 
        ## Deletion 
        editsR(hd, tl[1:], d-1, ed(p, p+tl[0])) 
        for h in extensions: 
            if h[-1] == tl[0]: ## Match 
                editsR(h, tl[1:], d, edits) 
            else: ## Replacement 
                editsR(h, tl[1:], d-1, ed(h[-1], tl[0])) 
        ## Transpose 
        if len(tl)>=2 and tl[0]!=tl[1] and hd+tl[1] in PREFIXES: 
            editsR(hd+tl[1], tl[0]+tl[2:], d-1, 
                   ed(tl[1]+tl[0], tl[0:2])) 
    ## Body of edits: 
    editsR('', word, d, []) 
    return results 

PREFIXES = set(w[:i] for w in Pw for i in range(len(w) + 1)) 
