from sklearn import svm
import sys
import numpy as np
import math

def svc(feature_file):

    features_files = np.load(feature_file)
    features = features_files['features']
    filenames = features_files['filenames']
    labels = features_files['labels']


    numberOfFeatures = features.shape[1]
    numberOfRecords = labels.shape[0]
    split = math.ceil(numberOfRecords*.33)
    #two labels only
    # 0 is banana, 1 is non-banana
    twoLabels = labels
    for i in xrange(0, numberOfRecords):
        if labels[i] == 1 or labels[i] == 2:
            twoLabels[i] = 0
        elif labels[i] == 3:
            twoLabels[i] = 1

    allInfo = np.concatenate((features, twoLabels.reshape(numberOfRecords, 1), filenames.reshape(numberOfRecords, 1)), axis=1)

    # shuffle the order of the records randomly
    np.random.shuffle(allInfo)

    #training data
    trainingFeatures = allInfo[0:numberOfRecords-split, 0:numberOfFeatures]
    trainingTarget = allInfo[0:numberOfRecords-split, numberOfFeatures]


    trainingFeatures = trainingFeatures.astype(np.float)
    trainingTarget = trainingTarget.astype(np.float)


    #training the model
    clf = svm.SVC()
    clf.fit(trainingFeatures, trainingTarget)

    #testing
    testFeatures = allInfo[numberOfRecords-split:numberOfRecords, 0:numberOfFeatures].astype(np.float)
    trainingTargetTest = allInfo[numberOfRecords-split:numberOfRecords, 4096].astype(np.float)

    results = clf.predict(testFeatures)
    print results
    print trainingTargetTest
    print np.count_nonzero(results - trainingTargetTest)


if __name__ == '__main__':
    feature_file = sys.argv[1]
    svc(feature_file)
