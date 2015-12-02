from sklearn import svm
import sys
import numpy as np

feature_file = sys.argv[1]

features_files = np.load(feature_file)

features = features_files['features']
filenames = features_files['filenames']
labels = features_files['labels']

dim = labels.shape[0]
#two labels only
# 0 is banana, 1 is non-banana
twoLabels = labels
for i in xrange(0, dim):
    if labels[i] == 1 or labels[i] == 2:
        twoLabels[i] = 0
    elif labels[i] == 3:
        twoLabels[i] = 1

featuresAndLabels = np.concatenate((features, twoLabels.reshape(dim, 1)), axis=1)
allInfo = np.concatenate((featuresAndLabels, filenames.reshape(dim, 1)), axis=1)

# shuffle the order of the records randomly
# print allInfo
# print ""
np.random.shuffle(allInfo)
# print allInfo

#training data
X = allInfo[0:dim-100, 0:4095]
y = allInfo[0:dim-100, 4096]

X = X.astype(np.float)
y = y.astype(np.float)


#training the model
clf = svm.SVC()
clf.fit(X, y)

#testing
xTest = allInfo[dim-100:dim, 0:4095].astype(np.float)
yTest = allInfo[dim-100:dim, 4096].astype(np.float)


results = clf.predict(xTest)
print results
print yTest
print np.count_nonzero(results - yTest)


# print xTest
# python svmExample.py features.npz