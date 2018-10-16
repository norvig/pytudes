from __future__ import division
from __future__ import print_function
import re
from accum import *


acc_re = re.compile("[[](.+):(.+) for (.+) in (.+)[]]")

def expand_accumulations(program_text):
    """Replace any accumulation displays in program_text with calls to
    accumulation.  Used to simulate a hypothetical Python interpreter that
    actually handles accumlation displays. This one is rather poor: it
    won't match across lines, it won't match nested accumulation displays,
    and it doesn't handle multiple 'for' clauses; nor 'if' clauses."""
    def _(matchobj):
        (acc, exp, x, it) = matchobj.groups()
        return "accumulation(%s, lambda %s: (%s), %s)" % (acc, x, exp, it)
    return acc_re.sub(_, program_text)

def test1(acc_display, expected):
    "Eval an accumulation display and see if it gets the expected answer."
    print(acc_display)
    result = eval(expand_accumulations(acc_display))
    assert result == expected, ('Got %s; expected %s' % (result, expected))
    print('    ==>  %s' % result)

#### Initialize some data
temp = [70, 70, 71, 74, 76, 76, 72, 76, 77, 77, 77, 78,
        78, 79, 79, 79, 78, 80, 82, 83, 83, 81, 84, 83]
data = temp
def f(x): return 2 * x
votes = {'Arnie': 48, 'Gray': 45, 'Tom': 13, 'Cruz': 32, 'Peter': 3}
candidates = votes.keys()

def test():

    print('temp = ', temp)
    print('data = temp')
    print('votes = ', votes)
    print('candidates = ', candidates)
    print()
    
    #### Test some accumulation displays
    test1("[Max: temp[hour] for hour in range(24)]",
          max([temp[hour] for hour in range(24)]))
    test1("[Min: temp[hour] for hour in range(24)]",
          min([temp[hour] for hour in range(24)]))
    test1("[Sum: x*x for x in data]",
          sum([x*x for x in data]))
    test1("[Mean: f(x) for x in data]",
          sum([f(x) for x in data])/len(data))
    test1("[Median: f(x) for x in data]",
          156.0)
    test1("[Mode: f(x) for x in data]",
          166)
    test1("[Argmax: votes[c] for c in candidates]",
          'Arnie')
    test1("[Argmin: votes[c] for c in candidates]",
          'Peter')
    test1("[Some: temp[hour] > 75 for hour in range(24)]",
          len([hour for four in range(24) if temp[hour] > 75])>0)
    test1("[Every: temp[hour] > 75 for hour in range(24)]",
          len([h for h in range(24) if temp[h] > 75]) == 24)
    test1("[Top(10): temp[hour] for hour in range(24)]",
          [84, 83, 83, 83, 82, 81, 80, 79, 79, 79])
    test1("[Join(', '): votes[c] for c in candidates]",
                       ', '.join([str(votes[c]) for c in candidates]))
    test1("[SortBy: abs(x) for x in (-2, -4, 3, 1)]",
          [1, -2, 3, -4])
    test1("[SortBy(reverse=True): abs(x) for x in (-2, -4, 3, 1)]",
          [-4, 3, -2, 1])

if __name__ == "__main__":
    test()
