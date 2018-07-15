import itertools
import numpy as np
import math
import sys
from graphviz import Digraph
import matplotlib.pyplot as plt

def weightGraphUntilConverge(graph, maxi):
    for i in range(maxi):
       avgDiff = weightGraph(graph)
       if avgDiff < .001:
           sys.stderr.write("stability achieved in %d cycles\n" % i)
           return

def buildGraph(loops):
    nodes = {}
    for loop in loops:
        # increment n_loops
        for i, v in loop:
            if not i in nodes:
                nodes[i] = Node(i)
            nodes[i].nI += 1
        # add edges for comparisons
        comparisons = [(a, b, cmp(a_s, b_s))
                for (a, a_s), (b, b_s) in itertools.combinations(loop, 2)]
        for a, b, verdict in comparisons:
            connect(nodes[a],nodes[b],verdict)
    for _, node in nodes.iteritems():
        node.v = float(sum([e.v for e in node.e])) / len(node.e)
    normalize(nodes)
    return nodes

def weightGraph(graph):
    scores = {}
    for i, node in graph.iteritems():
        weights = [e.v * abs(e.v + e.t.v) for e in node.e]
        scores[i] = math.fsum(weights) / len(node.e)
        # print i, weights, scores[i]
    diff = 0
    # normalization reimplemented so that diff can be calculated
    weight = max([abs(scores[i]) for i in scores])
    for i, score in scores.iteritems():
        score /= weight
        diff += abs(graph[i].v - score)
        graph[i].v = score
    diff / len(graph)
    return diff

def normalize(nodes):
    weight = max([abs(nodes[i].v) for i in nodes])
    for _, node in nodes.iteritems():
        node.v /= weight
    return nodes

def graph2Digraph(graph, printEq=False, labels=None):
    dot = Digraph()
    for _, node in graph.iteritems():
        label = node.n
        if labels is not None and node.n in labels:
            label = labels[node.n]
        rating = "%.02f" % node.v if node.v > 0 else "(%.02f)" % abs(node.v)
        dot.node(node.n, "%s\nr=%s, nI=%d, nC=%d" % (label, rating, node.nI, len(node.e)))
        # point toward greater
        # x<y <1
        for e in node.e:
            if e.v < 0:
                dot.edge(node.n, e.t.n)
            elif e.v == 0 and node.n < e.t.n and printEq:
                dot.edge(node.n, e.t.n, dir="none", style="dotted")
    dot.render('dot', view=True)

class Node():
    def __init__(self, n):
        self.n = n  # interviewer number
        self.e = [] # edges
        self.v = 0  # value
        self.nI = 0 # num interviews

def connect(a,b,v):
    a.e.append(Edge(v, b))
    b.e.append(Edge(-1*v, a))

class Edge():
    def __init__(self, v, t):
        self.v = v
        self.t = t

