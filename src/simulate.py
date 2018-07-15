from graphviz import Digraph
import itertools
import math
import matplotlib.pyplot as plt
import numpy as np
import sys

import ratings
import names

NInterviewer = 250
NInterviewPerLoop = 3
NCandidate = 20*14
Bar = 102
InterviewerDistr = (102, 6)
InterviewerInconsistentDistr = (0, 4)
CandidateDistr = (100, 7)

def main():
    np.random.seed(1)
    interviewers = list([Interviewer() for i in range(NInterviewer)])
    candidates = [getCandidate() for i in range(NCandidate)]

    # Note that loop references interviewer not an id like ratings does
    loops = []
    for c in candidates:
        loop = [ (i, i.interview(c))
            for i in sorted(np.random.choice(interviewers, NInterviewPerLoop, False))
        ]
        loops.append(loop)

    # print debrief (anon)
    print "\n\n".join([ # separate loops by empty line
            "\n".join( # join verdicts into a loop string
            map( # verdicts to strings
                lambda (i, v):
                    "%s\t%s" % (i.name, "Yes" if v else "No"),
                loop
            ))
        for loop in loops])

    # We have to turn interviewer reference into a string
    # strLoops = list(([(i.name,v) for (i,v) in loop] for loop in loops))
    # graph = ratings.buildGraph(strLoops)
    # ratings.weightGraphUntilConverge(graph, 20)
    # ratings.graph2Digraph(graph)
    # graphScores(buildScoreComparison(interviewers, graph))

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

def verdict(l):
    s = sum([l[0][1], l[1][1], l[2][1]])
    return s > (NInterviewPerLoop/2)

class Interviewer():
    def __init__(self):
        self.n = next(Interviewer.iNum)
        self.name = next(Interviewer.Names)
        self.bar = np.random.normal(*InterviewerDistr)
    def __str__(self):
        return str(self.n)
    def __le__(self, other):
        return self.n > other.n
    def __eq__(self, other):
        return self.n == other.n
    def __cmp__(self, other):
        return self.n.__cmp__(other.n)
    iNum = itertools.count(1)
    Names = names.genNames()

    def interview(self, candidate):
        barFlake = np.random.normal(*InterviewerInconsistentDistr)
        return candidate >= (self.bar + barFlake)

def getCandidate():
    return np.random.normal(*CandidateDistr)

if __name__ == "__main__":
    main()
