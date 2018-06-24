import numpy as np

# node_mat = np.zeros((4039, 32))
#
# with open("fb_dis_92524.emb") as f:
#     f.readline()
#     for line in f:
#         l = list(map(float, line.split()))
#         node_mat[int(l[0])] = l[1:]
#
# np.save("node_embedding", node_mat)

y_test = np.load("test_pred_1000e.npy")
test_pred = np.load("y_test_1000e.npy")

and_array = np.logical_and(y_test, test_pred)
and_array = np.sum(and_array, axis=1)

sum_array = np.sum(y_test, axis=1)

result = 0
count = 0
for a, b in zip(and_array, sum_array):
    if b != 0:
        result += 1.0*a/b
        count += 1

print(result*1.0/count)
