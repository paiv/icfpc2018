#!/usr/bin/env python
import graphviz

g = graphviz.Graph('Demo', filename='graph.gv', engine='neato')
g.edge('Hello', 'World')
g.view()
