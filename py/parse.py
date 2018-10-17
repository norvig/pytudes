from __future__ import print_function
grammar = {
  'Noun': ['stench', 'wumpus'],
  'Verb': ['is', 'smell'],
  'Adjective': ['dead', 'smelly'],
  'Adverb': ['left', 'back'],
  'Pronoun': ['me', 'you'],
  'Name': ['John', 'Mary'],
  'Article': ['the', 'a'],
  'Preposition': ['to', 'in'],
  'Conjunction': ['and', 'or'],
  'Digit': ['0', '1'],

  'S': [['NP', 'VP'], ['S', 'Comjunction', 'S']],
  'NP': ['Pronoun', 'Noun', ['Article', 'Noun'], ['Digit', 'Digit'],
         ['NP', 'PP'], ['NP', 'RelClause']],
  'VP': ['Verb', ['VP', 'NP'], ['VP', 'Adjective'], ['VP', 'PP'],
         ['VP', 'Adverb']],
  'PP': [['Preposition', 'NP']],
  'RelClause': [['that', 'VP']]
  }


def parse(forest, grammar):
    if len(forest) == 1 and category(forest[0]) == 'S':
        return forest[0]
    for i in range(len(forest)):
        for lhs in grammar.keys():
            for rhs in grammar[lhs]:
                rhs = mklist(rhs)
                n = len(rhs)
                subsequence = forest[i:i+n]
                if match(subsequence, rhs):
                    print(subsequence, lhs, '=>', rhs)
                    forest2 = forest[:]
                    forest2[i:i+n] = [(lhs, subsequence)]
                    result = parse(forest2, grammar)
                    if result != None:
                        return result
    return None

def mklist(x):
    if type(x) == type([]): return x
    else: return [x]

def match(forest, rhs):
    for i in range(len(rhs)):
        if category(forest[i]) != rhs[i] and forest[i] != rhs[i]: return 0
    return 1

def category(forest):
    if type(forest) == type(()): return forest[0]
    else: return 'word'
