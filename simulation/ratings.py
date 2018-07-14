import itertools
import numpy as np
import math
import sys

NInterviewer = 50
NInterviewPerLoop = 3
NCandidate = 20*4
Bar = 102
InterviewerDistr = (102, 6)
InterviewerInconsistentDistr = (0, 4)
CandidateDistr = (100, 7)

def main():
    np.random.seed(1)
    interviewers = list([Interviewer() for i in range(NInterviewer)])
    candidates = [getCandidate() for i in range(NCandidate)]
    comparisons = []
    loops = []

    for c in candidates:
        loop = [ (i, i.interview(c))
            for i in sorted(np.random.choice(interviewers, NInterviewPerLoop, False))
        ]
        for ((a, a_s), (b, b_s)) in itertools.combinations(loop, 2):
            comparisons.append((a.n, b.n, cmp(a_s, b_s)))
        loops.append(loop)

    graph = buildGraph(comparisons)
    for i in range(20):
       avgDiff = weightGraph(graph)
       if avgDiff < .001:
           sys.stderr.write("stability achieved in %d cycles\n" % i)
           break
    # graph2Digraph(graph)
    printScoreComparison(interviewers, graph)

def printScoreComparison(interviewers, graph):
    validCheck = [ (
            i.n,
            int(i.bar),
            graph[i.n].v,
            len(graph[i.n].e)
        ) for i in interviewers if i.n in graph ]
    validCheck = map(lambda x: "%d\t%.3f\t%.3f\t%d" % (
            x[0],
            (x[1] - InterviewerDistr[0])/float(InterviewerDistr[1]),
            x[2],
            x[3],
        ),
        sorted(validCheck, key=lambda t: t[1])
    )
    print "interv\tstddev\trating\tn\n" + "\n".join(validCheck)

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

def buildGraph(comparisons):
    nodes = {}
    for a, b, verdict in comparisons:
        if not a in nodes:
            nodes[a] = Node(a)
        if not b in nodes:
            nodes[b] = Node(b)
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

def graph2Digraph(graph, printEq=False):
    print "digraph {"
    for _, node in graph.iteritems():
        # point toward greater
        # x<y <1
        for e in node.e:
            if e.v < 0:
                print "%d -> %d" % (node.n, e.t.n)
            elif e.v == 0 and node.n < e.t.n and printEq:
                print "%d -> %d [dir=none style=dotted]" % (node.n, e.t.n)
        print '%d [label="%d (%f)"]' % (node.n, node.n, node.v)
    print "}"

class Node():
    def __init__(self, n):
        self.n = n
        self.e = []
        self.v = 0

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
