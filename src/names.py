import numpy as np
import os

Names = []
filepath = os.path.join(os.path.dirname(__file__), 'names.txt')
with open(filepath, 'r') as f:
    Names = list(n.strip() for n in f)

def genNames():
    for n in np.random.choice(Names, len(Names), False):
        yield n
    num = 1
    while True:
        for n in np.random.choice(Names, len(Names), False):
            yield n + str(num)
        num += 1

