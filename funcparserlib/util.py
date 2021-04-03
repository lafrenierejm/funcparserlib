# -*- coding: utf-8 -*-

# Copyright (c) 2008/2013 Andrey Vlasovskikh
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import unicode_literals


def pretty_tree(x, kids, show):
    """(a, (a -> list(a)), (a -> str)) -> str

    Returns a pseudographic tree representation of x similar to the tree command
    in Unix.
    """
    (MID, END, CONT, LAST, ROOT) = ('|-- ', '`-- ', '|   ', '    ', '')

    def rec(obj, indent, sym):
        line = indent + sym + show(obj)
        obj_kids = kids(obj)
        if len(obj_kids) == 0:
            return line
        else:
            if sym == MID:
                next_indent = indent + CONT
            elif sym == ROOT:
                next_indent = indent + ROOT
            else:
                next_indent = indent + LAST
            syms = [MID] * (len(obj_kids) - 1) + [END]
            lines = [rec(kid, next_indent, sym) for kid, sym in zip(obj_kids, syms)]
            return '\n'.join([line] + lines)

    return rec(x, '', ROOT)
