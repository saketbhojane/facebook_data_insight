import os
from collections import defaultdict
import numpy as np

node_circle = defaultdict(list)
egonets = []
for fn in os.listdir("./facebook"):
     if os.path.isfile(os.path.join("./facebook", fn)) and fn.endswith(".circles"):
         egonets.append(int(fn.split(".")[0]))
egonets.sort()

circle_no = 0
hits = 0
for ego in egonets:
    with open("./facebook/" + str(ego) + ".circles", "r") as f:
        for line in f:
            node_circle[ego].append(circle_no)
            line = list(map(int, line.split()[1:]))
            for member in line:
                node_circle[member].append(circle_no)
            circle_no += 1

no_grp = range(4039) - node_circle.keys()
print(len(no_grp))
exit()

node_circle_matrix = np.zeros((4039, 193), dtype=int)

for key, value in node_circle.items():
    for node in value:
        node_circle_matrix[key][value] = 1
