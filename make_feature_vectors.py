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
                feature_dict[int(feature.split()[-1])] = '_'.join(feature.split()[1].split(';')[:-1])

no_of_features = -1
for key, value in feature_dict.items():
    if no_of_features < key:
        no_of_features = key

no_of_features = no_of_features + 1
ego_feature_vecs = defaultdict(lambda:[0]*no_of_features)

for net in tqdm.tqdm(ego_networks):
    feature_index = []
    with open(os.path.join(folder_path, net + '.' + 'featnames')) as features:
        for line in features:
            feature_index.append(int(line.split()[-1]))
    with open(os.path.join(folder_path, net + '.' + 'egofeat')) as ego_feature:
        ego_feat_vec = ego_feature.readline().split()

    for i in range(len(feature_index)):
        try:
            ego_feature_vecs[int(net)][feature_index[i]] = int(ego_feat_vec[i])
        except IndexError:
            print("i", i, "feature_index[i]", feature_index[i], "ego_feat_vec[i]", ego_feat_vec[i])

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

dataframe = pd.DataFrame(ordered_ego_feature_vec, index=list(ordered_feature_dict.values())).T
dataframe.to_csv('feature_dump.txt', sep='\t')
