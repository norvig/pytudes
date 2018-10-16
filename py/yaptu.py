"""Yet Another Python Templating Utility, Version 1.2, by Alex Martelli.
   http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52305
   (Specialized to HTML and modified by Peter Norvig.)

Copies input to output, with some substitutions. There are three types
of substitutions: lexical, expression, and statement. 

LEXICAL SUBSTITUTIONS:

& < >
        These characters, if surrounded by whitespace, are replaced by
        the corresonding HTML entities: &amp;, &lt;, &gt;.

EXPRESSION SUBSTITUTIONS:

<<exp>>     
        Replace <<exp>> by eval(exp), where exp is a Python expression.
        The most common use is when exp is just a variable name.
        Example: <<green>>
        Special case 1: If exp starts with '/', replace '/' by '_'.
        Example: <</green>> becomes <<_green>
        Special case 2: If exp evals to a callable, call it.
        Example: <<random.random>> is the same as <<random.random()>>
        Special case 3: If exp evals to None, replace it with ''.
        Example: <<list.append(item)>> generates no text.

STATEMENT SUBSTITUTIONS:

All statement substitutions start with a #[ in column 1, and end with
a #] in column 1 of a subsequent line.  Nesting is allowed, and
works like you would expect. There are two variants:

#[
stmts
#]
        Any number of lines of Python stmts are executed.
        The first line must be empty, except for the #[

#[ stmt-header:
lines
#]
        The lines are interpreted as HTML with embedded expressions,
        and are sent to output, once for each execution of stmt-header.
        stmt-header is usually a for or if; This is hard to explain, 
        but easy to see with an example:

        <table><tr><th> Number <th> Number squared
        #[ for i in range(10):
              <tr><td> <<i>> <td> <<i**2>>
        #]        
        </table>
        
        This produces one line of the table for each value of i in [0 .. 9].
        If your compound statement has multiple stmt-headers, you use #| to
        introduce the subsequent stmt-headers (such as else: or except:). 
        Another example:

        #[ if time.localtime()[6] in [5, 6]: 
        Have a good weekend!
        #| else:
        Time for work.
        #]
"""
from __future__ import print_function

import sys, re, os, os.path

class Copier:
    "Smart-copier (YAPTU) class"

    def copyblock(self, i=0, last=None):
        "Main copy method: process lines [i,last) of block"

        def repl(match, self=self):
            "Replace the match with its value as a Python expression."
            expr = self.preproc(match.group(1), 'eval')
            if self.verbose: print('=== eval{%s}' % expr, end=' ')
            try:
                val = eval(expr, self.globals)
            except:
                self.oops('eval', expr)
            if callable(val): val = val()
            if val == None: val = ''
            if self.verbose: print('========>', val)
            return str(val)

        block = self.globals['_bl']
        if last is None: last = len(block)
        while i < last:
            line = block[i]
            if line.startswith("#["):   # a statement starts at line block[i]
                # i is the last line to _not_ process
                stmt = line[2:].strip()
                j = i+1   # look for 'finish' from here onwards
                nest = 1  # count nesting levels of statements
                while j<last and not stmt.endswith("#]"):
                    line = block[j]
                    # first look for nested statements or 'finish' lines
                    if line.startswith("#]"):    # found a statement-end
                        nest = nest - 1     
                        if nest == 0: break  # j is first line to _not_ process
                    elif line.startswith("#["):   # found a nested statement
                        nest = nest + 1     
                    elif nest == 1 and line.startswith("#|"):
                        # look for continuation only at this nesting
                        nestat = line[2:].strip()
                        stmt = '%s _cb(%s,%s)\n%s' % (stmt,i+1,j,nestat)
                        i=j     # again, i is the last line to _not_ process
                    j = j+1
                if stmt == '': ## A multi-line python suite
                    self.execute(''.join(block[i+1:j]))
                    i = j+1
                else:  ## The header of a for loop (etc.) is on this line
                    self.execute("%s _cb(%s,%s)" % (stmt,i+1,j))
                    i = j+1
            else:       # normal line, just copy with substitution
                self.outf.write(self.regex.sub(repl,self.preproc(line,'copy')))
                i = i+1

    def __init__(self, globals):
        "Create a Copier."
        self.regex   = re.compile("<<(.*?)>>")
        self.globals = globals
        self.globals['_cb'] = self.copyblock
        self.outf = sys.stdout
        self.verbose = 0

    def execute(self, stmt):
        stmt = self.preproc(stmt, 'exec') + '\n'
        if self.verbose: 
            print("******* executing {%s} in %s" % (stmt, self.globals.keys()))
        try:
            exec(stmt, self.globals)
        except:
            self.oops('exec', stmt)

    def oops(self, why, what):
        print('Something went wrong in %sing {%s}' % (why, what))
        print('Globals:', self.globals.keys(), \
            self.globals.get('SECTIONS', '???'))
        raise

    def preproc(self, string, why, reg=re.compile(r"\s([<>&])\s"), 
                table={'&':' &amp; ', '<':' &lt; ', '>':' &gt; '}):
        # If it starts with '/', change to '_'
        if why in ('exec', 'eval'):
            string = string.strip()
            if string[0] == '/':
                string = '_' + string[1:]
            return string
        elif why == 'copy':
            # Expand & < > into entitites if surrounded by whitespace
            return reg.sub(lambda match: table[match.group(1)], string)

    def copyfile(self, filename, ext="html"):
        "Convert filename.* to filename.ext, where ext defaults to html."
        global yaptu_filename
        outname = re.sub('[.][a-zA-Z0-9]+?$', '', filename) + '.'+ext
        print('Transforming', filename, 'to', outname)
        self.globals['_bl'] = open(filename).readlines()
        yaptu_filename = filename
        self.outf = open(outname, 'w')
        self.copyblock()

if __name__ == '__main__':
    copier = Copier(globals())
    for filename in sys.argv[1:]:
        if filename == '-v':
            copier.verbose = 1
        else:
            copier.copyfile(filename)
