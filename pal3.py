from collections import Counter, deque
import re

class PhraseDict(dict):
    """A dictionary of {letters: phrase}, such as {'donaldeknuth': 'Donald E. Knuth'}, with:
    .prefixes: Counter of {'pre': n} where n is the number of keys that start with 'pre'
    .suffixes: Counter of {'xes': n} where n is the number of keys that end with 'xes'"""
    def __init__(self, phrases):
        for phrase in phrases:
            phrase = phrase.strip()
            self[letters(phrase)] = phrase
        self.prefixes = Counter(x for p in self for x in prefixes(p))
        self.suffixes = Counter(x for p in self for x in suffixes(p))
        
def prefixes(phrase): return [phrase[:i] for i in range(1, len(phrase) + 1)]

def suffixes(phrase): return [phrase[-i:] for i in range(1, len(phrase) + 1)]

def letters(phrase, sub=re.compile(r'[\W]+').sub):
    "Remove all the non-letters from phrase; return lowercase version."
    return sub('', phrase).lower()

DICT = PhraseDict(open('npdict.txt'))

class Panama:
    """Panama represents a palindrome, or a state in searching for one.
    It has .left and .right to hold the phrases that are chosen,
    and .L and .R to hold the current partial phrases in the middle (still working on these).
    Also, a .set of all complete phrases, and the .dict of allowable phrases to choose from."""
    
    def __init__(self, left=['aman', 'aplan'], L='aca', R='', right=['acanal', 'panama'], dict=DICT):
        assert cat(left + [L]) == cat([R] + right)[::-1]
        self.left   = list(left)        # list of complete phrases on left
        self.L      = L                 # an incomplete phrase on left
        self.R      = R                 # an incomplete phrase on right
        self.right  = deque(right)      # deque of complete phrases on right
        self.dict   = dict              # a {letters: actual_phrase} mapping
        self.set    = set(left + right) # a set of all complete phrases in palindrome
        self.best   = []                # list of phrases in longest palindrome found
        self.Nshown = 0                 # the number of phrases shown in the previous printout
        self.i      = 0                 # the number of steps taken in the search
        self.check()

    def __str__(self): return self.original_phrases(self.best)
    
    def original_phrases(self, phrases): return ', '.join(self.dict[phrase] for phrase in phrases)

    def search(self, steps=10**5):
        """Depth-first search for palindromes. From the current state, find all applicable actions.
        Do the first one, and put on the stack reminders to undo it and try the others,
        but first search deeper from the result of the first action."""
        stack = [self.applicable_actions()]
        for self.i in range(steps):
            if not stack: 
                return
            command = stack.pop()
            if isinstance(command, UndoCommand):
                self.undo(command)
            elif command:
                act = command.pop()
                self.do(act)
                self.check()
                stack.extend([command, UndoCommand(act), self.applicable_actions()])
                
    def do(self, act):
        "Modify the current state by adding a letter, or finishing a phrase."
        if act == ',': # finish phrase on left
            self.set.add(self.L)
            self.left.append(self.L)
            self.L = ''
        elif act == ';': # finish phrase on right
            self.set.add(self.R)
            self.right.appendleft(self.R)
            self.R = ''
        else: # add a letter
            self.L = self.L + act 
            self.R = act + self.R
    
    def undo(self, act):
        "Modify the current state by undoing an action that was previously done."
        if act == ',': # unfinish phrase on left
            assert self.L == ''
            self.L = self.left.pop()
            self.set.remove(self.L)
        elif act == ';': # unfinish phrase on right
            assert self.R == ''
            self.R = self.right.popleft()
            self.set.remove(self.R)
        else: # remove a letter
            self.L = self.L[:-1]
            self.R = self.R[1:]
            
    def check(self):
        "Check to see if current state is a palindrome, and if so, record it and maybe print."
        if not self.is_palindrome(): return
        N = len(self.left) + len(self.right) 
        if N > len(self.best):
            self.best = self.left + list(self.right)
            if N - self.Nshown > 1000 or (N > 14000 and N - self.Nshown > 100) or N > 14500:
                self.Nshown = N
                print(self.report())
            
    def report(self):
        N = len(self.best)
        nwords = N + sum(self.dict[p].count(' ') for p in self.best)
        nletters = sum(len(p) for p in self.best)
        return ('Pal: {:6,d} phrases, {:6,d} words, {:6,d} letters (at step {:,d})'
                .format(N, nwords, nletters, self.i+1))
        
    def applicable_actions(self):
        L, R, D = self.L, self.R, self.dict
        actions = []

        def score(A): return D.prefixes[L+A] * D.suffixes[A+R]
        if self.is_allowed(L):
            actions.append(',')
        if self.is_allowed(R):
            actions.append(';')
        for A in sorted(alphabet, key=score):
            if score(A) > 0:
                actions.append(A)    

        return actions
 
    def is_allowed(self, phrase): return phrase in self.dict and phrase not in self.set
        
    def is_palindrome(self): 
        "Is this a palindrome? (Does any extra .L or .R match the other side?)"
        return ((self.L == '' and self.left[-1].endswith(self.R)) or 
                (self.R == '' and self.right[0].startswith(self.L)))

alphabet    = 'abcdefghijklmnopqrstuvwxyz'
cat         = ''.join
UndoCommand = str
DoCommand   = list
                      
################ Unit Tests

def test1():
    assert prefixes('hello') == ['h', 'he', 'hel', 'hell', 'hello']
    assert suffixes('hello') == ['o', 'lo', 'llo', 'ello', 'hello']
    assert letters('a man') == 'aman'
    assert letters('an elk') == 'anelk'
    assert letters('Mr. T') == 'mrt'
    assert letters('Donald E. Knuth') == 'donaldeknuth'
    assert len(DICT) == 125512
    assert 'panama' in DICT
    assert 'aman' in DICT
    assert 'threemen' not in DICT
    assert DICT['acanal'] == 'a canal'
    return 'ok'

def test2():
    p1 = Panama()
    assert p1.is_palindrome()
    assert str(p1) == 'a man, a plan, a canal, Panama'
    p2 = Panama(['aman','aplan'], 'acadd','dd', ['acanal', 'panama'])
    assert not p2.is_palindrome()
    p3 = Panama(['maya'], '', '', ['ayam'])
    assert p3.is_palindrome()
    assert str(p3) == 'Maya, a yam'
    return 'ok'

if __name__ == '__main__': 
    p = Panama();
    test1()
    test2()
    p.search(10**6)
    print(p.report())
    print(str(p))
