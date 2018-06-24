import numpy as np
import tqdm
import sys

# embd_mat = np.load("val.npy")
#
# with open("val.txt") as f1:
#     with open("fb_pre_train.emb", "w") as f2:
#         f2.write(str(embd_mat.shape[0]) + " " + str(embd_mat.shape[1]) + "\n")
#         i = 0
#         for line in tqdm.tqdm(f1):
#             f2.write(str(line.strip()) + " ")
#             for e in embd_mat[i]:
#                 f2.write(str(e) + " ")
#             f2.write("\n")
#             i += 1

embedding_file = sys.argv[1]
with open(embedding_file) as f:
    node_emb_mat = np.zeros([int(i) for i in f.readline().split()])
    for line in f:
        l = line.split()
        l = [float(i) for i in l]
        node_emb_mat[int(l[0])] = l[1:]

np.save("node_embedding.npy", np.array(node_emb_mat))
