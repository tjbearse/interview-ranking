import itertools
import numpy as np
import matplotlib.pyplot as plt

import ratings

labels = {}
with open('real/labels.tsv', 'r') as f:
    for l in f:
        name, n = l.strip().split("\t")
        n = int(n)
        labels[n] = name

loops = []
with open('real/anon.txt', 'r') as f:
    l = f.readline()
    loop = []
    while l != "":
        if l == "\n":
            loops.append(loop)
            loop = []
        else:
            i, v = l.strip().split('\t')
            i = int(i)
            v = v=="Yes"
            loop.append((i,v))
        l = f.readline()
# print "\n".join(map(str, loops))
# print "\n".join(map(str, comparisons))
graph = ratings.buildGraph(loops)
ratings.weightGraphUntilConverge(graph, 20)
# ratings.graph2Digraph(graph, True, labels)


nodes = np.array([(node.v, node.nI, len(node.e)) for _, node in graph.iteritems()],
        dtype=[('ratings', 'f4'), ('interviews', 'i4'), ('comparisons', 'i4')]
    )
plt.scatter(nodes['ratings'], nodes['comparisons'], s=nodes['interviews'])
plt.show()
