from optparse import OptionParser
import itertools
import matplotlib.pyplot as plt
import numpy as np
import os

import ratings

def main():
    labels = getLabels()

    loops = getLoops()
    graph = ratings.buildGraph(loops)
    ratings.weightGraphUntilConverge(graph, 20)

    if options.graph:
        ratings.graph2Digraph(graph, True, labels)


    if options.plot:
        nodes = np.array([(node.v, node.nI, len(node.e)) for _, node in graph.iteritems()],
                dtype=[('ratings', 'f4'), ('interviews', 'i4'), ('comparisons', 'i4')]
            )
        plt.scatter(nodes['ratings'], nodes['comparisons'], s=nodes['interviews'])
        plt.show()

def getLabels():
    labels = {}
    with open(options.labels, 'r') as f:
        for l in f:
            name, n = l.strip().split("\t")
            labels[n] = name
    return labels

def getLoops():
    loops = []
    with open(options.loops, 'r') as f:
        l = f.readline()
        loop = []
        while l != "":
            if l == "\n":
                loops.append(loop)
                loop = []
            else:
                i, v = l.strip().split('\t')
                v = v=="Yes"
                loop.append((i,v))
            l = f.readline()
    return loops

if __name__ == "__main__":
    labelFile = os.path.join(os.path.dirname(__file__), '..', "real", "labels.tsv")
    loopFile = os.path.join(os.path.dirname(__file__), '..', "real", "anon.txt")
    parser = OptionParser()
    parser.add_option("-g", "--graph", action="store_true", dest="graph",
                      help="graph relationships")
    parser.add_option("-p", "--plot", action="store_true", dest="plot",
                      help="show plots about relationships")
    parser.add_option("--labels", dest="labels", default=labelFile,
                      help="file to pull labels from")
    parser.add_option("--loops", dest="loops", default=loopFile,
                      help="file to pull loops from")

    (options, args) = parser.parse_args()

    main()
