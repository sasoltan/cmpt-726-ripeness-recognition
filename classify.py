from sklearn import svm
import sys, numpy, test_train_split

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
    features_files = numpy.load(feature_file)
    features = features_files['features']
    filenames = features_files['filenames']
    labels = features_files['labels']

    num_records, num_features = features.shape
    all_info = numpy.concatenate((features, labels.reshape(num_records, 1), filenames.reshape(num_records, 1)), axis=1)

    # split train/test
    train_indices, test_indices = test_train_split.split(filenames)

    # training data
    train_features, train_targets = [], []
    for train_index in train_indices:
        train_features.append(all_info[train_index, 0:num_features])
        train_targets.append(all_info[train_index, num_features])
    train_features = numpy.array(train_features).astype(numpy.float)
    train_targets = numpy.array(train_targets).astype(numpy.float)

    # test data
    test_features, test_targets = [], []
    for test_index in test_indices:
        test_features.append(all_info[test_index, 0:num_features])
        test_targets.append(all_info[test_index, num_features])
    test_features = numpy.array(test_features).astype(numpy.float)
    test_targets = numpy.array(test_targets).astype(numpy.float)

    #training the model
    clf = svm.SVC(C=500, gamma=10.0)
    clf.fit(train_features, train_targets)

    # check testing error
    train_results = clf.predict(train_features)
    total_errors, error_rate = get_num_errors(train_results, train_targets)
    print "Training: Number of errors: %i. Error rate: %f." % (total_errors, error_rate)
    # check training error
    test_results = clf.predict(test_features)
    total_errors, error_rate = get_num_errors(test_results, test_targets)
    print "Testing: Number of errors: %i. Error rate: %f." % (total_errors, error_rate)


if __name__ == '__main__':
    feature_file = sys.argv[1]
    svc(feature_file)
