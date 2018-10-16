"""
Code to support http://norvig.com/mayzner.html
Read files in the Google Books ngram format, and convert them to a simpler format.
The original format looks like this:

    word     \t year \t word_count \t book_count
    word_POS \t year \t word_count \t book_count

for example,

    accreted_VERB	1846	7	4
    accreted_VERB	1847	1	1
    accreted_VERB	1848	1	1

The function 'read_year_file' will convert a file of this form into a dict of
{WORD: count} pairs, where the WORD is uppercased, and the count is the total
over all years (you have the option to specify a starting year) and all
capitalizations.  Then 'read_dict' and 'write_dict' convert between a dict and
an external file format that looks like this:

    ACCRETED	9

"""

from __future__ import division
from __future__ import print_function
from collections import Counter, defaultdict

#### Read files in Books-Ngram format; convert to a dict

def read_year_file(filename, dic=None):
    """Read a file of 'word year word_count book_count' lines and convert to a dict
    {WORD: totalcount}. Uppercase all words, and only include all-alphabetic words."""
    if dic is None: dic = {}
    for line in open(filename):
        word, year, c1, c2 = line.split('\t')
        if '_' in word:
            word = word[:word.index('_')]
        if word.isalpha():
            word = word.upper()
            dic[word] = dic.get(word, 0) + int(c1)
    return dic

#### Read and write files of the form 'WORD \t count \n'

def write_dict(dic, filename):
    "Write a {word:count} dict as 'word \t count' lines in filename."
    out = open(filename, 'w')
    for key in sorted(dic):
        out.write('%s\t%s\n' % (key, dic[key]))
    return out.close()
        
def read_dict(filename, sep='\t'):
    "Read 'word \t count' lines from file and make them into a dict of {word:count}."
    pairs = (line.split(sep) for line in open(filename))
    return {word: int(count) for (word, count) in pairs}

#### Convert a bunch of year files into dict file format.

def convert_files(filenames, mincount=1e5):
    def report(filename, D, adj):
        import time
        N = len(D)
        W = sum(v for v in D.itervalues())
        print('%s: %s %s words (%s tokens) at %s' % (
            filename, adj, format(W, ',d'), format(N, ',d'),
            time.strftime("%H:%M:%S", time.gmtime())))
    for f in filenames:
        report(f, {}, 'starting')
        D = read_year_file(f)
        report(f, D, 'total')
        for key in list(D):
            if D[key] < mincount:
                del D[key]
        write_dict(D, 'WORD-' + f[-1].upper())
        report(f, D, 'popular')

def load(filename='top-words.txt'):
    "Load file of 'word \t count' lines into D (a dict), W (length of D) and M (total number of words)."
    global D, W, M
    D = read_dict(filename)
    W = len(D)
    M = sum(D.values())
    
#### Compute letter counts and save as HTML files.

def histogram(items):
    "Return a Counter of the number of times each key occurs in (key, val) pairs."
    C = Counter()
    for (key, val) in items:
        C[key] += val
    return C

def end(name): return '/' + name

def tag(name, **kwds): return '<' + name + keywords(kwds) + '>'

def row(cells, **kwds):
    return '<tr>' + ''
    
def ngram_tables(dic, N, pos=[0, 1, 2, 3, 4, -5, -4, -3, -2, -1]):
    """Return three dicts of letter N-grams of length N: counts, counts1, counts2.
    counts is a dict of {'AB': 123} that counts how often 'AB' occurs.
    counts1[i] is a dict of {'AB': 123} that counts how often 'AB' occurs at position i.
    counts2[i][j] is a dict of {'AB': 123} that counts how often 'AB' occurs at position i."""
    L = len(max(D, key=len))
    counts = Counter()
    counts1 = [Counter() for _ in range(L)]
    counts2 = [[Counter() for i in range(L)]]

def counter(pairs):
    "Make a Counter from an iterable of (value, count) pairs."
    c = Counter()
    for (value, count) in pairs:
        c[value] += count
    return c

def ngrams(word, N):
    return [word[i:i+N] for i in range(len(word)+1-N)]


import glob
#convert_files(glob.glob('book?'))
              
#DB = [[letter_counts() for length in range(length)] for length in range(maxlen)]
      

## Unused ???

def letter_counts(wc):
    """From word_counts dictionary wc, Create a dictionary of {(s, i, L): count}
    where s is a letter n-gram, i is the starting position, and L is the length
    of the word in which it appears."""
    result = defaultdict(int)
    for (word, count) in wc.iteritems():
        for p in pieces(word):
            result[p] += count
    return result

def pieces(word):
    "Yield the 1- and 2-letter grams in (s, i, L) format."
    L = len(word)
    for i in range(L):
        yield (word[i], i, L)
        if i+1 < L:
            yield (word[i:i+2], i, L)

def getcount(counts, s, pos, length):
    """The count for letter sequence s (one or two letters) starting at
    position i of words of length length.  If any argument is all, sum them up."""
    if length == all:
        return sum(getcount(counts, s, pos, L) for L in all_lengths)
    elif pos == all:
        return sum(getcount(counts, s, i, length) for i in range(length))
    else:
        return counts[s, pos, length]


print('start')
#wc = word_counts('count_100K.txt')
#counts = letter_counts(wc)
print('end')



def test():
    D = {'the': 100, 'of': 70, 'and': 60, 'to': 50, 'a': 40}

def num(ch):
    "Translate 'a' or 'A' to 0, ... 'z' or 'Z' to 25."
    return 'abcdefghijklmnopqrstuvwxyz'.index(ch.lower())
    

def stats(D, NS = (1, 2, 3, 4, 5, 6)):
    counts = {n: Counter() for n in NS}
    print('words ' + ' '.join('   %d-grams  ' % n for n in NS))
    for (i, word) in enumerate(sortedby(D), 1):
        for n in NS:
            for ng in ngrams(word, n):
                counts[n][ng] += 1
        if i % 5000 == 0 or i == len(D):
            print("%4dK" % (i/1000), end=' ')
            for n in NS:
                c = len(counts[n])
                field = "%5d (%d%%)" % (c, int(round(c*100/(26**n))))
                print('%12s' % field, end=' ')
            print()

letters = 'ETAOINSRHLDCUMFPGWYBVKXJQZ'
alphabet = ''.join(sorted(letters))

from itertools import cycle, izip

colors = 'ygobp'

def bar(text, color, count, N, pixels, height=16):
    width = int(round(pixels * count / N))
    if width < 2: width = 3
    title = '{}: {:.3f}%; {:,}'.format(text, count*100./N, count)
    return '<span title="%s"><img src="%s.jpg" height=%d width=%d><span style="position:relative; left:%d; bottom:4">%s</span></span>' % (
        title, color, height, width, -width+2, text) # -int(width/2+5)

def letter_bar(LC, N=None, factor='', pixels=700):
    if N is None: N = sum(LC.values())
    #divisor = {'':1., 'K':1e3, 'M':1e6, 'B':1e9}[factor]
    return ''.join(
        bar(L.lower(), color, LC[L], N, pixels)
        for (L, color) in izip(letters, cycle(colors)))
        

def singleton(x): return [x]

positions = [0, 1, 2, 3, 4, 5, 6, -7, -6, -5, -4, -3, -2, -1]

def substr(word, pos, length):
    """Return the substr of word of given length starting/ending at pos; or None."""
    W = len(word)
    if pos >= 0 and pos+length <= W:
        return word[pos:pos+length]
    elif pos < 0 and abs(pos)+length-1 <= W:
        return word[W+pos+1-length:W+pos+1]
    else:
        return None
        
def lettercount(D, pos):
    LC = histogram((substr(w, pos, 1), D[w]) for w in D)
    del LC[None]
    print(LC)
    pos_name = (str(pos)+'+' if isinstance(pos, tuple) else
                pos if pos < 0 else
                pos+1)
    return '\n<br>\n%-3s %s' % (pos_name, letter_bar(LC))

def ngramcount(D, n=2):
    return histogram((ng, D[w]) for w in D for ng in ngrams(w, n))

def twograms(D2):
    N = sum(D2.values())
    header = '<table cellpadding=1 cellborder=1>'
    rows = [tr([cell(A+B, D2, N) for A in alphabet]) for B in alphabet]
    return '\n'.join([header] + rows + ['</table>'])

def cell(text, D2, N, height=16, maxwidth=25, scale=27):
    count = D2.get(text, 0)
    width = int(round(maxwidth * count * scale * 1. / N))
    if width < 1: width = 1
    title = '{}: {:.3f}%; {:,}'.format(text, count*100./N, count)
    return '<td title="%s"><img src="o.jpg" height=%d width=%d><span style="position:relative; left:%d; bottom:4">%s</span></span>' % (
        title, height, width, -width+2, text)

def cell(text, D2, N, height=16, maxwidth=25, scale=27):
    count = D2.get(text, 0)
    width = int(round(maxwidth * count * scale * 1. / N))
    if width < 1: width = 1
    title = '{}: {:.3f}%; {:,}'.format(text, count*100./N, count)
    return '<td title="%s" background="o.jpg" height=%d width=%d>%s' % (
        title, height, width, text) 

def tr(cells):
    return '<tr>' + ''.join(cells)

def comma(n): return '{:,}'.format(n)

def ngram_stats(D, n, k=5):
    DN = ngramcount(D, n)
    topk = ', '.join(sortedby(DN)[:k])
    return '<tr><td>%d-grams<td align=right>%s<td align=right>%s<td><a href="counts-%d.csv">counts-%d.csv</a><td><a href="counts-%d.html">counts-%d.html</a><td>%s' % (
        n, comma(len(DN)), comma(sum(DN.values())), n, n, n, n, topk)

#### Tables

def sortedby(D):
    return sorted(D, key=lambda x: -D[x])

ANY = '*'

wordlengths = range(1, 10)

def col(*args): return args

def columns(n, wordlengths=wordlengths):
    lengths = [k for k in wordlengths if k >= n]
    return ([col(ANY, ANY)]
            + [col(k, ANY) for k in lengths]
            + [col(k, start, start+n-1) for k in lengths for start in range(1, 2+k-n)]
            + [col(ANY, start, start+n-1) for start in wordlengths]
            + [col(ANY, -k, -k+n-1) for k in reversed(lengths) if -k+n-1 < 0])

def colname(col):
    fmt = '%s/%s' if (len(col) == 2) else '%s/%d:%d'
    return  fmt % col

def csvline(first, rest):
    return '\t'.join([first] + map(str, rest))

def makecsv(n, D=D):
    out = open('ngrams%d.csv' % n, 'w')
    cols = columns(n)
    Dng = defaultdict(lambda: defaultdict(int))
    for w in D:
        for (start, ng) in enumerate(ngrams(w, n), 1):
            entry = Dng[ng]
            N = D[w]
            wlen = len(w)
            entry[ANY, ANY] += N
            entry[wlen, ANY] += N
            if start <= 9:
                entry[wlen, start, start+n-1] += N
                entry[ANY, start, start+n-1] += N
            from_end = wlen-start+1
            if from_end <= 9:
                entry[ANY, -from_end, -from_end+n-1] += N
        # enumerate ngrams from word and increment counts for each one
    print(csvline('%d-gram' % n,  map(colname, cols)), file=out)
    for ng in sorted(Dng, key=lambda ng: -Dng[ng][(ANY, ANY)]):
        print(csvline(ng, [Dng[ng].get(col, 0) for col in cols]), file=out)
    out.close()
    return Dng

### Tests

"""
>>> for w in words:
    print '%-6s %6.2f B (%4.2f%%) <img src="s.jpg" height=12 width=%d>' % (w.lower(), D[w]/1e9, D[w]*100./N, int(round(D[w]*4000./N)))
... 
the     53.10 B (7.14%) <img src="s.jpg" height=12 width=286>
of      30.97 B (4.16%) <img src="s.jpg" height=12 width=167>
and     22.63 B (3.04%) <img src="s.jpg" height=12 width=122>
to      19.35 B (2.60%) <img src="s.jpg" height=12 width=104>
in      16.89 B (2.27%) <img src="s.jpg" height=12 width=91>
a       15.31 B (2.06%) <img src="s.jpg" height=12 width=82>
is       8.38 B (1.13%) <img src="s.jpg" height=12 width=45>
that     8.00 B (1.08%) <img src="s.jpg" height=12 width=43>
for      6.55 B (0.88%) <img src="s.jpg" height=12 width=35>
it       5.74 B (0.77%) <img src="s.jpg" height=12 width=31>
as       5.70 B (0.77%) <img src="s.jpg" height=12 width=31>
was      5.50 B (0.74%) <img src="s.jpg" height=12 width=30>
with     5.18 B (0.70%) <img src="s.jpg" height=12 width=28>
be       4.82 B (0.65%) <img src="s.jpg" height=12 width=26>
by       4.70 B (0.63%) <img src="s.jpg" height=12 width=25>
on       4.59 B (0.62%) <img src="s.jpg" height=12 width=25>
not      4.52 B (0.61%) <img src="s.jpg" height=12 width=24>
he       4.11 B (0.55%) <img src="s.jpg" height=12 width=22>
i        3.88 B (0.52%) <img src="s.jpg" height=12 width=21>
this     3.83 B (0.51%) <img src="s.jpg" height=12 width=21>
are      3.70 B (0.50%) <img src="s.jpg" height=12 width=20>
or       3.67 B (0.49%) <img src="s.jpg" height=12 width=20>
his      3.61 B (0.49%) <img src="s.jpg" height=12 width=19>
from     3.47 B (0.47%) <img src="s.jpg" height=12 width=19>
at       3.41 B (0.46%) <img src="s.jpg" height=12 width=18>
which    3.14 B (0.42%) <img src="s.jpg" height=12 width=17>
but      2.79 B (0.38%) <img src="s.jpg" height=12 width=15>
have     2.78 B (0.37%) <img src="s.jpg" height=12 width=15>
an       2.73 B (0.37%) <img src="s.jpg" height=12 width=15>
had      2.62 B (0.35%) <img src="s.jpg" height=12 width=14>
they     2.46 B (0.33%) <img src="s.jpg" height=12 width=13>
you      2.34 B (0.31%) <img src="s.jpg" height=12 width=13>
were     2.27 B (0.31%) <img src="s.jpg" height=12 width=12>
their    2.15 B (0.29%) <img src="s.jpg" height=12 width=12>
one      2.15 B (0.29%) <img src="s.jpg" height=12 width=12>
all      2.06 B (0.28%) <img src="s.jpg" height=12 width=11>
we       2.06 B (0.28%) <img src="s.jpg" height=12 width=11>
can      1.67 B (0.22%) <img src="s.jpg" height=12 width=9>
her      1.63 B (0.22%) <img src="s.jpg" height=12 width=9>
has      1.63 B (0.22%) <img src="s.jpg" height=12 width=9>
there    1.62 B (0.22%) <img src="s.jpg" height=12 width=9>
been     1.62 B (0.22%) <img src="s.jpg" height=12 width=9>
if       1.56 B (0.21%) <img src="s.jpg" height=12 width=8>
more     1.55 B (0.21%) <img src="s.jpg" height=12 width=8>
when     1.52 B (0.20%) <img src="s.jpg" height=12 width=8>
will     1.49 B (0.20%) <img src="s.jpg" height=12 width=8>
would    1.47 B (0.20%) <img src="s.jpg" height=12 width=8>
who      1.46 B (0.20%) <img src="s.jpg" height=12 width=8>
so       1.45 B (0.19%) <img src="s.jpg" height=12 width=8>
no       1.40 B (0.19%) <img src="s.jpg" height=12 width=8>

>>> for n in sorted(H):
    print '%2d %9.2f M (%6.3f%%) <img src="s.jpg" height=12 width=%d> %d' % (n, H[n]/1e6, H[n]*100./NN, H[n]*3000./NN, n)
... 
 1  22301.22 M ( 2.998%) <img src="s.jpg" height=12 width=89> 1
 2 131293.85 M (17.651%) <img src="s.jpg" height=12 width=529> 2
 3 152568.38 M (20.511%) <img src="s.jpg" height=12 width=615> 3
 4 109988.33 M (14.787%) <img src="s.jpg" height=12 width=443> 4
 5  79589.32 M (10.700%) <img src="s.jpg" height=12 width=320> 5
 6  62391.21 M ( 8.388%) <img src="s.jpg" height=12 width=251> 6
 7  59052.66 M ( 7.939%) <img src="s.jpg" height=12 width=238> 7
 8  44207.29 M ( 5.943%) <img src="s.jpg" height=12 width=178> 8
 9  33006.93 M ( 4.437%) <img src="s.jpg" height=12 width=133> 9
10  22883.84 M ( 3.076%) <img src="s.jpg" height=12 width=92> 10
11  13098.06 M ( 1.761%) <img src="s.jpg" height=12 width=52> 11
12   7124.15 M ( 0.958%) <img src="s.jpg" height=12 width=28> 12
13   3850.58 M ( 0.518%) <img src="s.jpg" height=12 width=15> 13
14   1653.08 M ( 0.222%) <img src="s.jpg" height=12 width=6> 14
15    565.24 M ( 0.076%) <img src="s.jpg" height=12 width=2> 15
16    151.22 M ( 0.020%) <img src="s.jpg" height=12 width=0> 16
17     72.81 M ( 0.010%) <img src="s.jpg" height=12 width=0> 17
18     28.62 M ( 0.004%) <img src="s.jpg" height=12 width=0> 18
19      8.51 M ( 0.001%) <img src="s.jpg" height=12 width=0> 19
20      6.35 M ( 0.001%) <img src="s.jpg" height=12 width=0> 20
21      0.13 M ( 0.000%) <img src="s.jpg" height=12 width=0> 21
22      0.81 M ( 0.000%) <img src="s.jpg" height=12 width=0> 22
23      0.32 M ( 0.000%) <img src="s.jpg" height=12 width=0> 23

>>> NL = sum(LC.values())

>>> for L in sorted(LC, key=lambda L: -LC[L]):
    print '%s %8.1f B (%5.2f%%) <img src="s.jpg" height=12 width=%d>' % (L, LC[L]/1e9, LC[L]*100./NL, LC[L]*3000./NL)
...
E    445.2 B (12.49%) <img src="s.jpg" height=12 width=374>
T    330.5 B ( 9.28%) <img src="s.jpg" height=12 width=278>
A    286.5 B ( 8.04%) <img src="s.jpg" height=12 width=241>
O    272.3 B ( 7.64%) <img src="s.jpg" height=12 width=229>
I    269.7 B ( 7.57%) <img src="s.jpg" height=12 width=227>
N    257.8 B ( 7.23%) <img src="s.jpg" height=12 width=217>
S    232.1 B ( 6.51%) <img src="s.jpg" height=12 width=195>
R    223.8 B ( 6.28%) <img src="s.jpg" height=12 width=188>
H    180.1 B ( 5.05%) <img src="s.jpg" height=12 width=151>
L    145.0 B ( 4.07%) <img src="s.jpg" height=12 width=122>
D    136.0 B ( 3.82%) <img src="s.jpg" height=12 width=114>
C    119.2 B ( 3.34%) <img src="s.jpg" height=12 width=100>
U     97.3 B ( 2.73%) <img src="s.jpg" height=12 width=81>
M     89.5 B ( 2.51%) <img src="s.jpg" height=12 width=75>
F     85.6 B ( 2.40%) <img src="s.jpg" height=12 width=72>
P     76.1 B ( 2.14%) <img src="s.jpg" height=12 width=64>
G     66.6 B ( 1.87%) <img src="s.jpg" height=12 width=56>
W     59.7 B ( 1.68%) <img src="s.jpg" height=12 width=50>
Y     59.3 B ( 1.66%) <img src="s.jpg" height=12 width=49>
B     52.9 B ( 1.48%) <img src="s.jpg" height=12 width=44>
V     37.5 B ( 1.05%) <img src="s.jpg" height=12 width=31>
K     19.3 B ( 0.54%) <img src="s.jpg" height=12 width=16>
X      8.4 B ( 0.23%) <img src="s.jpg" height=12 width=7>
J      5.7 B ( 0.16%) <img src="s.jpg" height=12 width=4>
Q      4.3 B ( 0.12%) <img src="s.jpg" height=12 width=3>
Z      3.2 B ( 0.09%) <img src="s.jpg" height=12 width=2>

>>> D2 = ngramcount(D, 2)

>>> for ng in sorted(D2, key=lambda L: -D2[L])[:50]: print '%s %8.1f B (%5.2f%%) <img src="o.jpg" height=12 width=%d>' % (ng, D2[ng]/1e9, D2[ng]*100./N2, D2[ng]*15000./N2)

def doit(k=25):
    counts = [sortedby(ngramcount(D, n))[:k] for n in range(2, 10)]
    for i in range(k):
        print ('     '.join(count[i] for count in counts)).lower()
"""
