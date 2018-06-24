# Create your first MLP in Keras
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
import numpy
# fix random seed for reproducibility
numpy.random.seed(7)
# load pima indians dataset
# dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
X = numpy.load("node_embedding.npy")
Y = numpy.load("node_circle_matrix.npy")
# split into input (X) and output (Y) variables
# X = dataset[:,0:8]
# Y = dataset[:,8]
# create model

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=50)
# print("X_train", X_train.shape)
# print("X_test", X_test.shape)
# print("y_train", y_train.shape)
# print("y_test", y_test.shape)

# exit()
model = Sequential()
model.add(Dense(50, input_dim=32, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(193, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam')
# Fit the model
model.fit(X_train, y_train, epochs=1000, batch_size=50)
# evaluate the model
# scores = model.evaluate(X_test, y_test)
# print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
preds = model.predict(X_test)
preds[preds>=0.5] = 1
preds[preds<0.5] = 0
numpy.save("test_pred_1000e", preds)
numpy.save("y_test_1000e", y_test)

and_array = numpy.logical_and(y_test, preds)
and_array = numpy.sum(and_array, axis=1)

sum_array = numpy.sum(y_test, axis=1)

result = 0
count = 0
for a, b in zip(and_array, sum_array):
    if b != 0:
        result += 1.0*a/b
        count += 1

print(result*1.0/count)
