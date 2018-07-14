import itertools
import numpy as np
import math
import sys
from graphviz import Digraph
import matplotlib.pyplot as plt

NInterviewer = 50
NInterviewPerLoop = 3
NCandidate = 20*4
Bar = 102
InterviewerDistr = (102, 6)
InterviewerInconsistentDistr = (0, 4)
CandidateDistr = (100, 7)

def main():
    # np.random.seed(1)
    interviewers = list([Interviewer() for i in range(NInterviewer)])
    candidates = [getCandidate() for i in range(NCandidate)]
    loops = []

    for c in candidates:
        loop = [ (i.n, i.interview(c))
            for i in sorted(np.random.choice(interviewers, NInterviewPerLoop, False))
        ]
        loops.append(loop)

    graph = buildGraph(comparisons)
    weightGraphUntilConverge(graph, 20)
    graph2Digraph(graph)
    graphScores(buildScoreComparison(interviewers, graph))

def weightGraphUntilConverge(graph, maxi):
    for i in range(maxi):
       avgDiff = weightGraph(graph)
       if avgDiff < .001:
           sys.stderr.write("stability achieved in %d cycles\n" % i)
           break

def graphScores(scores):
    plt.scatter(scores['rating'], scores['stddev'])
    plt.xlabel('rating')
    plt.ylabel('stddev')
    plt.show()

def buildScoreComparison(interviewers, graph):
    validCheck = [ (
            i.n,
            (i.bar - InterviewerDistr[0])/float(InterviewerDistr[1]),
            graph[i.n].v,
            len(graph[i.n].e)
        ) for i in interviewers if i.n in graph ]
    return np.array(validCheck,
            dtype=[
                ('interviewer', 'i4'),
                ('stddev', 'f4'),
                ('rating', 'f4'),
                ('interviews', 'i4'),
            ])

def printStats(loops, comparisons, candidates):
    nLoops = len(loops)
    nSplit = len([l for l in loops if l[0][1] != l[1][1] or l[1][1] != l[2][1]])
    verdicts = [verdict(l) for l in loops]
    nYes = len([v for v in verdicts if v])

    nRight = len([True for c,v in zip(candidates, verdicts) if (c > Bar) == v])
    nNo = nLoops-nYes
    print """
    yes:\t{yes} ({yes_pct})
    no:\t\t{no} ({no_pct})
    split:\t{split}

    right:\t{right}
    wrong:\t{wrong}
    """.format(
        split=nSplit,
        yes=nYes,
        no=nNo,
        yes_pct=float(nYes)/nLoops,
        no_pct=float(nNo)/nLoops,
        right=nRight,
        wrong=nLoops-nRight,
    )

def verdict(l):
    s = sum([l[0][1], l[1][1], l[2][1]])
    return s > (NInterviewPerLoop/2)

class Interviewer():
    def __init__(self):
        self.n = Interviewer.ninterviewers
        self.bar = np.random.normal(*InterviewerDistr)
        Interviewer.ninterviewers += 1
    def __str__(self):
        return str(self.n)
    def __le__(self, other):
        return self.n > other.n
    def __eq__(self, other):
        return self.n == other.n
    def __cmp__(self, other):
        return self.n.__cmp__(other.n)
    ninterviewers = 0

    def interview(self, candidate):
        barFlake = np.random.normal(*InterviewerInconsistentDistr)
        return candidate >= (self.bar + barFlake)

def getCandidate():
    return np.random.normal(*CandidateDistr)

def printDebrief(loop):
    for i,v in loop:
        print '\t%s %s' % (i, v)

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
        label = str(node.n)
        if labels is not None and node.n in labels:
            label = labels[node.n]
        rating = "%.02f" % node.v if node.v > 0 else "(%.02f)" % abs(node.v)
        dot.node(str(node.n), "%s\nr=%s, nI=%d, nC=%d" % (label, rating, node.nI, len(node.e)))
        # point toward greater
        # x<y <1
        for e in node.e:
            if e.v < 0:
                dot.edge(str(node.n), str(e.t.n))
            elif e.v == 0 and node.n < e.t.n and printEq:
                dot.edge(str(node.n), str(e.t.n), dir="none", style="dotted")
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


def printDigraph(comparisons, interviewers, printAgree=False):
    print "digraph {"
    for a, b, score in comparisons:
        # point toward greater
        # x<y <1
        if score < 0:
            print "%d -> %d" % (a, b)
        elif score > 0:
            print "%d -> %d" % (b, a)
        elif printAgree:
            print "%d -> %d [style=dotted dir=none]" % (a, b)
    for i in interviewers:
        print '%d [label="%d"]' % (i.n, i.bar)
    print "}"

if __name__ == "__main__":
    main()
