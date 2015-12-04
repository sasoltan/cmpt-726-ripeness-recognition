import sys, numpy, test_train_split
from sklearn import svm, cross_validation, grid_search

BANANA_CLASS = [0, 1, 2]
NONBANANA_CLASS = [3]

def get_num_errors(predicted_results, actual_results, filenames=None, print_failed=False, print_additional=False):
    num_test = predicted_results.shape[0]
    total_errors = 0
    banana = [0, 0]
    ripe = [0, 0]
    non_banana = [0, 0]
    fail = []
    for i in range(num_test):
        expected, actual = predicted_results[i], actual_results[i]
        if predicted_results[i] != actual_results[i]:
            total_errors += 1
            if filenames:
                fail.append("%s %i" % (filenames[i], predicted_results[i]))

        if actual_results[i] in BANANA_CLASS:
            banana[1] += 1
            if predicted_results[i] in BANANA_CLASS:
                banana[0] += 1

        if actual_results[i] in BANANA_CLASS and predicted_results[i] in BANANA_CLASS:
            ripe[1] += 1
            if predicted_results[i] == actual_results[i]:
                ripe[0] += 1

        if actual_results[i] in NONBANANA_CLASS:
            non_banana[1] += 1
            if predicted_results[i] in NONBANANA_CLASS:
                non_banana[0] += 1


    if print_additional:
        print("Percent of bananas correctly classified as a banana: %f" % (banana[0] / float(banana[1])))
        print("Percent of bananas classified as banas, percent correctly predicted ripeness: %f" % (ripe[0] / float(ripe[1])))
        print("Percent of other correctly classified as others: %f" % (non_banana[0] / float(non_banana[1])))

    if print_failed:
        for f in sorted(fail):
            print f

    error_rate = total_errors / float(num_test)
    return total_errors, error_rate

def optimize_params(training_features, training_target):
    param_grid = [
        #{'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000], 'gamma': [0.001, 0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['rbf', 'linear']},
        # result: {'kernel': 'rbf', 'C': 100, 'gamma': 10}
        #{'C': [100, 200, 300, 400, 500, 600, 700, 800], 'gamma': [10], 'kernel': ['rbf']},
        # result: {'kernel': 'rbf', 'C': 100, 'gamma': 10}
        {'C': [100], 'gamma': [10], 'kernel': ['rbf', 'linear', 'poly', 'sigmoid']},
        # result: {'kernel': 'rbf', 'C': 100, 'gamma': 10}
    ]
    clf = grid_search.GridSearchCV(svm.SVC(C=1), param_grid, cv=10, n_jobs=-1, verbose=3,  pre_dispatch=4)
    clf.fit(training_features, training_target)
    return clf.best_params_

def main(feature_file, do_optimization=True):
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

    # get parameters for classification
    if do_optimization:
        classification_params = optimize_params(train_features, train_targets)
        print "Optimized params: %s" % (str(classification_params))
    else:
        classification_params = {"C": 100, "gamma": 10.0}

    # test data
    test_features, test_targets, test_filenames = [], [], []
    for test_index in test_indices:
        test_features.append(all_info[test_index, 0:num_features])
        test_targets.append(all_info[test_index, num_features])
        test_filenames.append(all_info[test_index, num_features+1])
    test_features = numpy.array(test_features).astype(numpy.float)
    test_targets = numpy.array(test_targets).astype(numpy.float)

    #training the model
    clf = svm.SVC(**classification_params)
    clf.fit(train_features, train_targets)

    # check testing error
    train_results = clf.predict(train_features)
    total_errors, error_rate = get_num_errors(train_results, train_targets)
    print "Training: Number of errors: %i. Error rate: %f." % (total_errors, error_rate)
    # check training error
    test_results = clf.predict(test_features)
    total_errors, error_rate = get_num_errors(test_results, test_targets, filenames=test_filenames, print_failed=False, print_additional=True)
    print "Testing: Number of errors: %i. Error rate: %f." % (total_errors, error_rate)


if __name__ == '__main__':
    feature_file = sys.argv[1]
    do_optimization = sys.argv[2] != "noop" if len(sys.argv) >= 3 else True
    main(feature_file, do_optimization=do_optimization)
