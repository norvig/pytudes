"""A framework for running unit tests and examples, written in docstrings.

This lets you write "Ex: sqrt(4) ==> 2; sqrt(-1) raises ValueError" in a
docstring, and then execute the examples as unit tests.

This functionality is similar to the doctest module.  The major
differences between docex and doctest are:

(1) Brevity.  With docex you write the one-line comment
    "Ex: len('abc') ==> 3; len([]) ==> 0; len(5) raises TypeError"
    With doctest you would need 9 lines for the same thing:
    '''>>> len('abc')
    3
    >>> len([])
    0
    >>> len(5))
    Traceback (most recent call last):
      ...
    TypeError: len() of unsized object
    '''

(2) Docex handles both examples and unit tests.
    It took me a while to recognize this distinction: when I write
    "sqrt(4) ==> 2" it has two purposes -- to serve as a unit test
    and to serve as an example of how to use the sqrt function.
    When I write "random.choice('abc')" it serves as an example of
    how to use the choice function, but it is not a unit test.
    docex lets you do both; doctest only supports tests.  Of course
    you can coerce this into a test in doctest, with something like
    >>> random.choice('abc') in 'abc'
    True

(3) Eval-based rather than string-comparison based.  The docex string
    "dict(zip([1,4,9], [1,2,3])) ==> {1: 1, 4: 2, 9: 3}" works even
    when a different version of Python decides to print the dict as
    "{9: 3, 4: 2, 1: 1}" because docex evals the right-hand-side and
    checks to see if it is equal.  That's good for dicts, its good for
    writing "1+1==2 ==> True" and having it work in versions of Python
    where True prints as "1" rather than as "True", and so on,
    but doctest has the edge if you want to compare against something
    that doesn't have an eval-able output, or if you want to test
    printed output.

(4) Doctest has many more features, and is better supported.
    I wrote docex before doctest was an official part of Python, but
    with the refactoring of doctest in Python 2.4, I decided to switch
    my code over to doctest, even though I prefer the brevity of docex.
    I still offer docex for those who want it.

From Python, when you want to test modules m1, m2, ... do:
    docex.Docex([m1, m2, ...])
From the shell, when you want to test files *.py, do:
    python docex.py [log-file] *.py
If log file ends in .htm or .html, it will be written in HTML.
If log file is -, or if it is missing, then standard output is used.

For each module, Docex looks at the __doc__ and _docex strings of the
module itself, and of each member, and recursively for each member
class.  If a line in a docstring starts with r'^\s*Ex: ' (a line with
blanks, then 'Ex: '), then the remainder of the string after the colon
is treated as examples. Each line of the examples should conform to
one of the following formats:

    (1) Blank line or a comment; these just get echoed verbatim to the log.
    (2) Of the form example1 ; example2 ; ...
    (3) Of the form 'x ==> y' for any expressions x and y.
            x is evaled and assigned to _, then y is evaled.
            If x != y, an error message is printed.
    (4) Of the form 'x raises y', for any statement x and expression y.
            First y is evaled to yield an exception type, then x is execed.
            If x doesn't raise the right exception, an error msg is printed.
    (5) Of the form 'statement'. Statement is execed for side effect.
    (6) Of the form 'expression'. Expression is evaled for side effect.
"""
from __future__ import print_function

import re, sys, types

class Docex:
    """A class to run test examples written in docstrings or in _docex."""

    def __init__(self, modules=None, html=0, out=None,
                 title='Docex Example Output'):
        if modules is None:
            modules = sys.modules.values()
        self.passed = self.failed = 0;
        self.dictionary = {}
        self.already_seen = {}
        self.html = html
        try:
            if out: sys.stdout = out
            self.writeln(title, '<h1>', '</h1><pre>')
            for module in modules:
                self.run_module(module)
            self.writeln(str(self), '</pre>\n<hr><h1>', '</h1>\n')
        finally:
            if out:
                sys.stdout = sys.__stdout__
                out.close()

    def __repr__(self):
        if self.failed:
            return ('<Test: #### failed %d, passed %d>'
                    % (self.failed, self.passed))
        else:
            return '<Test: passed all %d>' % self.passed

    def run_module(self, object):
        """Run the docstrings, and then all members of the module."""
        if not self.seen(object):
            self.dictionary.update(vars(object)) # import module into self
            name = object.__name__
            self.writeln('## Module %s ' % name,
             '\n</pre><a name=%s><h1>' % name,
             '</h1><pre>')
            self.run_docstring(object)
            names = object.__dict__.keys()
            names.sort()
            for name in names:
                val = object.__dict__[name]
                if isinstance(val, types.ClassType):
                    self.run_class(val)
                elif isinstance(val, types.ModuleType):
                    pass
                elif not self.seen(val):
                    self.run_docstring(val)

    def run_class(self, object):
        """Run the docstrings, and then all members of the class."""
        if not self.seen(object):
            self.run_docstring(object)
            names = object.__dict__.keys()
            names.sort()
            for name in names:
                self.run_docstring(object.__dict__[name])

    def run_docstring(self, object, search=re.compile(r'(?m)^\s*Ex: ').search):
        "Run the __doc__ and _docex attributes, if the object has them."
        if hasattr(object, '__doc__'):
            s = object.__doc__
            if isinstance(s, str):
                match = search(s)
                if match: self.run_string(s[match.end():])
        if hasattr(object, '_docex'):
            self.run_string(object._docex)

    def run_string(self, teststr):
        """Run a test string, printing inputs and results."""
        if not teststr: return
        teststr = teststr.strip()
        if teststr.find('\n') > -1:
            map(self.run_string, teststr.split('\n'))
        elif teststr == '' or teststr.startswith('#'):
            self.writeln(teststr)
        elif teststr.find('; ') > -1:
            for substr in teststr.split('; '): self.run_string(substr)
        elif teststr.find('==>') > -1:
            teststr, result = teststr.split('==>')
            self.evaluate(teststr, result)
        elif teststr.find(' raises ') > -1:
            teststr, exception = teststr.split(' raises ')
            self.raises(teststr, exception)
        else: ## Try to eval, but if it is a statement, exec
            try:
                self.evaluate(teststr)
            except SyntaxError:
                exec(teststr, self.dictionary)

    def evaluate(self, teststr, resultstr=None):
        "Eval teststr and check if resultstr (if given) evals to the same."
        self.writeln('>>> ' +  teststr.strip())
        result = eval(teststr, self.dictionary)
        self.dictionary['_'] = result
        self.writeln(repr(result))
        if resultstr == None:
            return
        elif result == eval(resultstr, self.dictionary):
            self.passed += 1
        else:
            self.fail(teststr, resultstr)

    def raises(self, teststr, exceptionstr):
        teststr = teststr.strip()
        self.writeln('>>> ' + teststr)
        except_class = eval(exceptionstr, self.dictionary)
        try:
            exec(teststr, self.dictionary)
        except except_class:
            self.writeln('# raises %s as expected' % exceptionstr)
            self.passed += 1
            return
        self.fail(teststr, exceptionstr)

    def fail(self, teststr, resultstr):
        self.writeln('###### ERROR, TEST FAILED: expected %s for %s'
                     % (resultstr, teststr),
                     '<font color=red><b>', '</b></font>')
        self.failed += 1

    def writeln(self, s, before='', after=''):
        "Write s, html escaped, and wrapped with html code before and after."
        s = str(s)
        if self.html:
            s = s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            print('%s%s%s' % (before, s, after))
        else:
            print(s)

    def seen(self, object):
        """Return true if this object has been seen before.
        In any case, record that we have seen it."""
        result = self.already_seen.has_key(id(object))
        self.already_seen[id(object)] = 1
        return result

def main(args):
    """Run Docex.  args should be a list of python filenames.
    If the first arg is a non-python filename, it is taken as the
    name of a log file to which output is written.  If it ends in
    ".htm" or ".html", then the output is written as html.  If the
    first arg is "-", then standard output is used as the log file."""
    import glob
    out = None
    html = 0
    if args[0] != "-" and not args[0].endswith(".py"):
        out = open(args[0], 'w')
        if args[0].endswith(".html") or args[0].endswith(".htm"):
            html = 1
    modules = []
    for arg in args:
        for file in glob.glob(arg):
            if file.endswith('.py'):
                modules.append(__import__(file[:-3]))
    print(Docex(modules, html=html, out=out))

if __name__ == '__main__':
    main(sys.argv[1:])
