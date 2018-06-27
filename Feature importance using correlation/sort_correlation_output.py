from collections import defaultdict, OrderedDict

feature_1_0 = defaultdict(list)
with open('feature_correlation_1_0.txt', 'r') as f:
    for line in f:
        line = line.split(':')

        feat_name = ' '.join(line[:-1])
        corr_coeff = float(line[-1])
        feature_1_0[feat_name] = corr_coeff

ordered_feature_1_0 = OrderedDict(sorted(feature_1_0.items(), key=lambda t: t[1], reverse=True))

with open('ordered_feature_correlation_1_0.txt', 'w') as f:
    for key, value in ordered_feature_1_0.items():
        f.write(key + " " + str(value) + "\n")

feature_0_1 = defaultdict(list)
with open('feature_correlation_0_1.txt', 'r') as f:
    for line in f:
        line = line.split(':')

        feat_name = ' '.join(line[:-1])
        corr_coeff = float(line[-1])
        feature_0_1[feat_name] = corr_coeff

ordered_feature_0_1 = OrderedDict(sorted(feature_0_1.items(), key=lambda t: t[1], reverse=True))

with open('ordered_feature_correlation_0_1.txt', 'w') as f:
    for key, value in ordered_feature_0_1.items():
        f.write(key + " " + str(value) + "\n")

feature_0_0 = defaultdict(list)
with open('feature_correlation_0_0.txt', 'r') as f:
    for line in f:
        line = line.split(':')

        feat_name = ' '.join(line[:-1])
        corr_coeff = float(line[-1])
        feature_0_0[feat_name] = corr_coeff

ordered_feature_0_0 = OrderedDict(sorted(feature_0_0.items(), key=lambda t: t[1], reverse=True))

with open('ordered_feature_correlation_0_0.txt', 'w') as f:
    for key, value in ordered_feature_0_0.items():
        f.write(key + " " + str(value) + "\n")

feature_1_1 = defaultdict(list)
with open('feature_correlation_1_1.txt', 'r') as f:
    for line in f:
        line = line.split(':')

        feat_name = ' '.join(line[:-1])
        corr_coeff = float(line[-1])
        feature_1_1[feat_name] = corr_coeff

ordered_feature_1_1 = OrderedDict(sorted(feature_1_1.items(), key=lambda t: t[1], reverse=True))

with open('ordered_feature_correlation_1_1.txt', 'w') as f:
    for key, value in ordered_feature_1_1.items():
        f.write(key + " " + str(value) + "\n")
