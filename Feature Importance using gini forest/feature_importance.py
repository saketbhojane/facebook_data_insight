import numpy as np
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier
import sys
import os
import pandas as pd
from collections import defaultdict, OrderedDict
import tqdm

folder_path = sys.argv[1]
feature_dict = {}
ego_networks = []

for filename in tqdm.tqdm(os.listdir(folder_path)):
    if filename.endswith(".featnames"):
        with open(os.path.join(folder_path, filename)) as features:
            ego_networks.append(filename.split('.')[0])
            for feature in features:
                # print "Feature: Key", int(feature.split()[-1]), "Value", '_'.join(feature.split()[1].split(';')[:-1])
                feature_dict[int(feature.split()[-1])] = '_'.join(feature.split()[1].split(';')[:-1])

no_of_features = -1
for key, value in feature_dict.items():
    if no_of_features < key:
        no_of_features = key

no_of_features = no_of_features + 1
ego_feature_vecs = defaultdict(lambda:[0]*no_of_features)

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

ordered_feature_dict = OrderedDict(sorted(feature_dict.items(), key=lambda t: t[0]))
ordered_ego_feature_vec = OrderedDict(sorted(ego_feature_vecs.items(), key=lambda t: t[0]))

print("Making adjacency list")
adj_list = defaultdict(list)
with open('facebook_combined.txt') as f:
    for line in f:
        line = line.split()
        line = [int(i) for i in line]
        adj_list[line[0]].append(line[1])
        adj_list[line[1]].append(line[0])

print("Done.")

train_X = []
train_Y = []

print("Making training data")

# debug
# news_feat = [0]*no_of_features
'''
for key1, val1 in tqdm.tqdm(ordered_ego_feature_vec.items()):
    for key2, val2 in ordered_ego_feature_vec.items():
        if key1 < key2:

            news_feat = []
            for i in range(no_of_features):
                if val1[i] == 1 and val2[i] == 1:
                    news_feat.append(1)
                else:
                    news_feat.append(0)
            train_X.append(news_feat)
            if key1 in adj_list[key2]:
                train_Y.append(1)
            else:
                train_Y.append(0)

# debug
            # train_X.append(news_feat)
            # train_Y.append(1)

print("Converting the data into numpy array")
np_train_X = np.array(train_X, dtype=np.uint8)
np_train_Y = np.array(train_Y, dtype=np.uint8)
print("Done")
print("np_train_X", np_train_X.shape)
print("np_train_Y", np_train_Y.shape)

print("Saving numpy arrays")
np.savez_compressed('./train_and_label',a=np_train_X, b=np_train_Y)
'''

data = np.load('./train_and_label.npz')
np_train_X = data['a']
np_train_Y = data['b']

# loaded = np.load('./train_and_label')
# np_train_X = loaded['a']
# np_train_Y = loaded['b']

# print("Saving new features to file")
# with open('new_features_train.txt', 'w') as f:
#     for line in tqdm.tqdm(train_X):
#         line = [str(i) for i in line]
#         line = " ".join(line) + "\n"
#         f.write(line)
#         f.flush()
#
# with open('new_features_labels.txt', 'w') as f:
#     for line in tqdm.tqdm(train_Y):
#         line = str(line)
#         line = " ".join(line) + "\n"
#         f.write(line)
#         f.flush()

# Build a forest and compute the feature importances
forest = ExtraTreesClassifier(n_estimators=50,
                              random_state=0)

print("Fitting in different forests")
forest.fit(np_train_X, np_train_Y)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

with open('feature_importance_index_50', 'w') as file:
    for f in range(np_train_X.shape[1]):
        print("%d. feature %d (%f) feature name is %s" % (f + 1, indices[f], importances[indices[f]], feature_dict[indices[f]]))
        file.write("%d. feature %d (%f) feature name is %s\n" % (f + 1, indices[f], importances[indices[f]], feature_dict[indices[f]]))

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(np_train_X.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(np_train_X.shape[1]), indices)
plt.xlim([-1, np_train_X.shape[1]])
plt.show()
plt.savefig('foo.png')
