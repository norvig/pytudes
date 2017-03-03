"""Search for  counterexamples to Beal's conjecture
See http://norvig.com/beal.html and http://www.bealconjecture.com"""

from __future__  import division, print_function
from math        import log
from itertools   import combinations, product
from collections import defaultdict
try:
    from math import gcd      # For Python 3.6 and up
except ImportError:
    from fractions import gcd # For older versions (works in 2.7 as well)

def beal(max_A, max_x):
    """See if any A ** x + B ** y equals some C ** z, with gcd(A, B) == 1.
    Consider any 1 <= A,B <= max_A and x,y <= max_x, with x,y prime or 4."""
    Apowers = make_Apowers(max_A, max_x)
    Czroots = make_Czroots(Apowers)
    for (A, B) in combinations(Apowers, 2):
        if gcd(A, B) == 1:
            for (Ax, By) in product(Apowers[A], Apowers[B]):       
                Cz = Ax + By
                if Cz in Czroots:
                    C = Czroots[Cz]
                    x, y, z = exponent(Ax, A), exponent(By, B), exponent(Cz, C)
                    print('{} ** {} + {} ** {} == {} ** {} == {}'
                          .format(A, x, B, y, C, z, C ** z))

def make_Apowers(max_A, max_x): 
    "A dict of {A: [A**3, A**4, ...], ...}."
    exponents = exponents_upto(max_x)
    return {A: [A ** x for x in (exponents if (A != 1) else [3])]
            for A in range(1, max_A+1)}

def make_Czroots(Apowers): return {Cz: C for C in Apowers for Cz in Apowers[C]}            
    
def exponents_upto(max_x):
    "Return all odd primes up to max_x, as well as 4."
    exponents = [3, 4] if max_x >= 4 else [3] if max_x == 3 else []
    for x in range(5, max_x, 2):
        if not any(x % p == 0 for p in exponents):
            exponents.append(x)
    return exponents

def exponent(Cz, C): 
    """Recover z such that C ** z == Cz (or equivalently z = log Cz base C).
    For exponent(1, 1), arbitrarily choose to return 3."""
    return 3 if (Cz == C == 1) else int(round(log(Cz, C)))

##############################################################################

def tests():
    assert make_Apowers(6, 10) == {
         1: [1],
         2: [8, 16, 32, 128],
         3: [27, 81, 243, 2187],
         4: [64, 256, 1024, 16384],
         5: [125, 625, 3125, 78125],
         6: [216, 1296, 7776, 279936]}
    
    assert make_Czroots(make_Apowers(5, 8)) == {
        1: 1, 8: 2, 16: 2, 27: 3, 32: 2, 64: 4, 81: 3,
        125: 5, 128: 2, 243: 3, 256: 4, 625: 5, 1024: 4,
        2187: 3, 3125: 5, 16384: 4, 78125: 5}
    Czroots = make_Czroots(make_Apowers(100, 100))
    assert 3 ** 3 + 6 ** 3 in Czroots
    assert 99 ** 97 in Czroots
    assert 101 ** 100 not in Czroots
    assert Czroots[99 ** 97] == 99
    
    assert exponent(10 ** 5, 10) == 5
    assert exponent(7 ** 3, 7) == 3
    assert exponent(1234 ** 999, 1234) == 999
    assert exponent(12345 ** 6789, 12345) == 6789
    assert exponent(3 ** 10000, 3) == 10000
    assert exponent(1, 1) == 3
    
    assert exponents_upto(2) == []
    assert exponents_upto(3) == [3]
    assert exponents_upto(4) == [3, 4]
    assert exponents_upto(40) == [3, 4, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    assert exponents_upto(100) == [
        3, 4, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
        67, 71, 73, 79, 83, 89, 97]
    
    assert gcd(3, 6) == 3
    assert gcd(3, 7) == 1
    assert gcd(861591083269373931, 94815872265407) == 97
    assert gcd(2*3*5*(7**10)*(11**12), 3*(7**5)*(11**13)*17) == 3*(7**5)*(11**12)
    return 'tests pass'

##############################################################################

def beal_modp(max_A, max_x, p=2**31-1):
    """See if any A ** x + B ** y equals some C ** z (mod p), with gcd(A, B) == 1.
    If so, verify that the equation works without the (mod p).
    Consider any 1 <= A,B <= max_A and x,y <= max_x, with x,y prime or 4."""
    assert p >= max_A
    Apowers = make_Apowers_modp(max_A, max_x, p)
    Czroots = make_Czroots_modp(Apowers)
    for (A, B) in combinations(Apowers, 2):
        if gcd(A, B) == 1:
            for (Axp, x), (Byp, y) in product(Apowers[A], Apowers[B]):  
                Czp = (Axp + Byp) % p
                if Czp in Czroots:
                    lhs = A ** x + B ** y
                    for (C, z) in Czroots[Czp]:
                        if lhs == C ** z:
                            print('{} ** {} + {} ** {} == {} ** {} == {}'
                                  .format(A, x, B, y, C, z, C ** z))                        
                    

def make_Apowers_modp(max_A, max_x, p): 
    "A dict of {A: [(A**3 (mod p), 3), (A**4 (mod p), 4), ...]}."
    exponents = exponents_upto(max_x)
    return {A: [(pow(A, x, p), x) for x in (exponents if (A != 1) else [3])]
            for A in range(1, max_A+1)}

def make_Czroots_modp(Apowers): 
    "A dict of {C**z (mod p): [(C, z),...]}"
    Czroots = defaultdict(list)
    for A in Apowers:
        for (Axp, x) in Apowers[A]:
            Czroots[Axp].append((A, x))
    return Czroots

##############################################################################

def simpsons(bases, powers):
    """Find the integers (A, B, C, n) that come closest to solving 
    Fermat's equation, A ** n + B ** n == C ** n. 
    Let A, B range over all pairs of bases and n over all powers."""
    equations = ((A, B, iroot(A ** n + B ** n, n), n)
                 for A, B in combinations(bases, 2)
                 for n in powers)
    return min(equations, key=relative_error)

def iroot(i, n): 
    "The integer closest to the nth root of i."
    return int(round(i ** (1./n)))

def relative_error(equation):
    "Error between LHS and RHS of equation, relative to RHS." 
    (A, B, C, n) = equation
    LHS = A ** n + B ** n
    RHS = C ** n
    return abs(LHS - RHS) / RHS

if __name__ == '__main__':
    print(tests())
    print("Searching beal(500, 100)")
    print(beal(500, 100))
    print("Finding Simpson-esque near-solutions to Fermat's Equation")
    def s(b, p):  print('{0}^{3} + {1}^{3} = {2}^{3}'.format(*simpsons(b, p)))
    s(range(1000, 2000), [11, 12, 13])
    s(range(3000, 5000), [12])
    print("Searching beal_modp(500, 100)")
    print(beal_modp(500, 100))


