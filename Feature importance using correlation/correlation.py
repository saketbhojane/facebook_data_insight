import sys
import os
import pandas as pd
from collections import defaultdict, OrderedDict
import tqdm
from scipy.stats.stats import pearsonr

folder_path = sys.argv[1]
feature_dict = {}
ego_networks = []

print("Reading Features Names")
for filename in tqdm.tqdm(os.listdir(folder_path)):
    if filename.endswith(".featnames"):
        with open(os.path.join(folder_path, filename)) as features:
            ego_networks.append(filename.split('.')[0])
            for feature in tqdm.tqdm(features):
                # print "Feature: Key", int(feature.split()[-1]), "Value", '_'.join(feature.split()[1].split(';')[:-1])
                feature_dict[int(feature.split()[-1])] = '_'.join(feature.split()[1].split(';')[:-1])

ordered_feature_dict = OrderedDict(sorted(feature_dict.items(), key=lambda t: t[0]))

print("Dumping Feature Names")
with open('all_features_combined.txt', 'w') as f:
    for key, value in ordered_feature_dict.items():
        f.write(str(key) + "\t\t" + str(value) + "\n")

no_of_features = -1
for key, value in feature_dict.items():
    if no_of_features < key:
        no_of_features = key

no_of_features = no_of_features + 1
ego_feature_vecs = defaultdict(lambda:[0]*no_of_features)


print("Reading and Writing Features Values")
for net in tqdm.tqdm(ego_networks):
    # print("net", net)
    feature_index = []
    with open(os.path.join(folder_path, net + '.' + 'featnames')) as features:
        for line in features:
            feature_index.append(int(line.split()[-1]))
    # print(feature_index)
    with open(os.path.join(folder_path, net + '.' + 'egofeat')) as ego_feature:
        ego_feat_vec = ego_feature.readline().split()

    for i in range(len(feature_index)):
        try:
            ego_feature_vecs[int(net)][feature_index[i]] = int(ego_feat_vec[i])
        except IndexError:
            print("i", i, "feature_index[i]", feature_index[i], "ego_feat_vec[i]", ego_feat_vec[i])


    # print(ego_feature_vecs[int(net)])

    with open(os.path.join(folder_path, net + '.' + 'feat')) as alter_feature:
        for line in alter_feature:
            node = int(line.split()[0])
            line = list(map(int, line.split()[1:]))

            for i in range(len(feature_index)):
                try:
                    ego_feature_vecs[int(node)][feature_index[i]] = int(line[i])
                except IndexError:
                    print("i", i, "feature_index[i]", feature_index[i], "line[i]", line[i])

ordered_ego_feature_vec = OrderedDict(sorted(ego_feature_vecs.items(), key=lambda t: t[0]))

adjacency_list = defaultdict(list)

with open('/'.join(folder_path.rstrip('/').split('/')[:-1]) + '/facebook_combined.txt', 'r') as f:
    for line in f:
        line =list(map(int, line.split()))
        adjacency_list[line[0]].append(line[1])
        adjacency_list[line[1]].append(line[0])

print("Adjacency list made")

# for key, value in ordered_ego_feature_vec.items():
#     print(len(value))
#     break

# print("Finding Correlation between each pair of nodes")
# with open('feature_correlation.txt', 'w') as f:
#     for i in tqdm.tqdm(range(no_of_features)):
#         for key1, value1 in ordered_ego_feature_vec.items():
#             omega1 = omega2 = 0
#             for key2, value2 in ordered_ego_feature_vec.items():
#                 if key1 < key2:
#                     if value1[i] == value2[i]:
#                         omega1 = omega1 + 1
#                         if key2 in adjacency_list[key1]:
#                             omega2 = omega2 + 1
#         if omega1 != 0:
#             string = "feature " + str(i) + " : " + str(omega2/omega1)
#         else:
#             string = "feature " + str(i) + " : Divide by zero issue : omega1 = " + str(omega1) + " omega2 = " + str(omega2) + "\n"
#         f.write(string)

print("Finding correlation matrix")
correlation_matrix = defaultdict(list)

for key1, value1 in tqdm.tqdm(ordered_ego_feature_vec.items()):
    for key2, value2 in ordered_ego_feature_vec.items():
        if key1 < key2:
            if key2 in adjacency_list[key1]:
                for i in range(no_of_features):
                    if value1[i] == 1 and value2[i] == 1:
                        correlation_matrix[(key1, key2)].append(1)
                    else:
                        correlation_matrix[(key1, key2)].append(0)
