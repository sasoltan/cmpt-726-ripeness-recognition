from sklearn import svm
import sys
import numpy as np
import math

def get_num_errors(expected_results, actual_results):
    num_test = expected_results.shape[0]
    total_errors = 0
    for i in range(num_test):
        expected, actual = expected_results[i], actual_results[i]
        if expected_results[i] != actual_results[i]:
            total_errors += 1
    error_rate = total_errors / float(num_test)
    return total_errors, error_rate 

def svc(feature_file):

    features_files = np.load(feature_file)
    features = features_files['features']
    filenames = features_files['filenames']
    labels = features_files['labels']


    numberOfFeatures = features.shape[1]
    numberOfRecords = labels.shape[0]
    split = math.ceil(numberOfRecords*.33)

    allInfo = np.concatenate((features, labels.reshape(numberOfRecords, 1), filenames.reshape(numberOfRecords, 1)), axis=1)

    # shuffle the order of the records randomly
    np.random.shuffle(allInfo)

    #training data
    trainingFeatures = allInfo[0:numberOfRecords-split, 0:numberOfFeatures]
    trainingTarget = allInfo[0:numberOfRecords-split, numberOfFeatures]


    trainingFeatures = trainingFeatures.astype(np.float)
    trainingTarget = trainingTarget.astype(np.float)


    #training the model
    clf = svm.SVC(C=0.001, gamma=10.0, tol=1e-16)
    clf.fit(trainingFeatures, trainingTarget)

    #testing
    testFeatures = allInfo[numberOfRecords-split:numberOfRecords, 0:numberOfFeatures].astype(np.float)
    trainingTargetTest = allInfo[numberOfRecords-split:numberOfRecords, numberOfFeatures].astype(np.float)

    # check testing error
    train_results = clf.predict(trainingFeatures)
    total_errors, error_rate = get_num_errors(train_results, trainingTarget)
    print "Training: Number of errors: %i. Error rate: %f." % (total_errors, error_rate)
    # check training error
    test_results = clf.predict(testFeatures)
    total_errors, error_rate = get_num_errors(test_results, trainingTargetTest)
    print "Testing: Number of errors: %i. Error rate: %f." % (total_errors, error_rate)


if __name__ == '__main__':
    feature_file = sys.argv[1]
    svc(feature_file)
