Parsing Stages Illustrated
==========================

<dl>
  <dt>Author:</dt>
  <dd class="vcard">
    <a class="fn url" href="http://claimid.com/vlasovskikh">Andrey Vlasovskikh</a>
  </dd>
  <dt>License:</dt>
  <dd>
    <a href="https://creativecommons.org/licenses/by-nc-sa/3.0/">
      Creative Commons Attribution-Noncommercial-Share Alike 3.0
    </a>
  </dd>
  <dt>Library Homepage:</dt>
  <dd>
    <a href="https://github.com/vlasovskikh/funcparserlib">
      https://github.com/vlasovskikh/funcparserlib
    </a>
  </dd>
  <dt>Library Version:</dt>
  <dd>0.3.6</dd>
</dl>

Given some language, for example, the [GraphViz DOT][dot] graph language (see
[its grammar][dot-grammar]), you can *easily write your own parser* for it in
Python using `funcpaserlib`.

Then you can:

1. Take a piece of source code in this DOT language:

        >>> s = '''\
        ... digraph g1 {
        ...     n1 -> n2 ->
        ...     subgraph n3 {
        ...         nn1 -> nn2 -> nn3;
        ...         nn3 -> nn1;
        ...     };
        ...     subgraph n3 {} -> n1;
        ... }
        ... '''

    that stands for the graph:

    ![The picture of the graph above](test-connected-subgraph.png)

2. Import your small parser (we use one shipped as an example with
    `funcparserlib` here):

        >>> import sys, os
        >>> sys.path.append(os.path.join(os.getcwd(), 'tests'))
        >>> import dot as dotparser

3. Transform the source code into a sequence of tokens:

        >>> toks = dotparser.tokenize(s)

        >>> print('\n'.join(str(tok) for tok in toks))
        1,1-1,7: Name 'digraph'
        1,9-1,10: Name 'g1'
        1,12-1,12: Op '{'
        2,5-2,6: Name 'n1'
        2,8-2,9: Op '->'
        2,11-2,12: Name 'n2'
        2,14-2,15: Op '->'
        3,5-3,12: Name 'subgraph'
        3,14-3,15: Name 'n3'
        3,17-3,17: Op '{'
        4,9-4,11: Name 'nn1'
        4,13-4,14: Op '->'
        4,16-4,18: Name 'nn2'
        4,20-4,21: Op '->'
        4,23-4,25: Name 'nn3'
        4,26-4,26: Op ';'
        5,9-5,11: Name 'nn3'
        5,13-5,14: Op '->'
        5,16-5,18: Name 'nn1'
        5,19-5,19: Op ';'
        6,5-6,5: Op '}'
        6,6-6,6: Op ';'
        7,5-7,12: Name 'subgraph'
        7,14-7,15: Name 'n3'
        7,17-7,17: Op '{'
        7,18-7,18: Op '}'
        7,20-7,21: Op '->'
        7,23-7,24: Name 'n1'
        7,25-7,25: Op ';'
        8,1-8,1: Op '}'

4. Parse the sequence of tokens into a parse tree:

        >>> tree = dotparser.parse(toks)

        >>> from textwrap import fill
        >>> print(fill(repr(tree), 70))
        Graph(strict=None, type='digraph', id='g1', stmts=[Edge(nodes=['n1',
        'n2', SubGraph(id='n3', stmts=[Edge(nodes=['nn1', 'nn2', 'nn3'],
        attrs=[]), Edge(nodes=['nn3', 'nn1'], attrs=[])])], attrs=[]),
        Edge(nodes=[SubGraph(id='n3', stmts=[]), 'n1'], attrs=[])])

5. Pretty-print the parse tree:

        >>> print(dotparser.pretty_parse_tree(tree))
        Graph [id=g1, strict=False, type=digraph]
        `-- stmts
            |-- Edge
            |   |-- nodes
            |   |   |-- n1
            |   |   |-- n2
            |   |   `-- SubGraph [id=n3]
            |   |       `-- stmts
            |   |           |-- Edge
            |   |           |   |-- nodes
            |   |           |   |   |-- nn1
            |   |           |   |   |-- nn2
            |   |           |   |   `-- nn3
            |   |           |   `-- attrs
            |   |           `-- Edge
            |   |               |-- nodes
            |   |               |   |-- nn3
            |   |               |   `-- nn1
            |   |               `-- attrs
            |   `-- attrs
            `-- Edge
                |-- nodes
                |   |-- SubGraph [id=n3]
                |   |   `-- stmts
                |   `-- n1
                `-- attrs

6. And so on. Basically, you got full access to the tree-like structure of the
   DOT file

See [the source code][dot-py] of the DOT parser and the docs at [the funcparserlib
homepage][funcparserlib] for details.

  [dot]: https://www.graphviz.org/
  [dot-grammar]: https://www.graphviz.org/doc/info/lang.html
  [funcparserlib]: https://github.com/vlasovskikh/funcparserlib
  [dot-py]: https://github.com/vlasovskikh/funcparserlib
