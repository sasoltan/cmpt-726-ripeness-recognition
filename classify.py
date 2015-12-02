import sys, numpy

def main():
    feature_file = sys.argv[1]

    features_files = numpy.load(feature_file)

    features = features_files['features']
    filenames = features_files['filenames']
    labels = features_files['labels']

    print("Features size: %s" % (str(features.shape)))
    print("Filenames size: %s" % (str(filenames.shape)))
    print("Labels size: %s" % (str(labels.shape)))

    rows, dim = features.shape

    num_zero = 0
    with open("feature-stats.txt", 'w') as output_file:
        for i in range(dim):
            t = (numpy.mean(features[:,i]), numpy.std(features[:,i]))
            if t == (0.0, 0.0):
                num_zero += 1
            else:
                output_file.write("%s\n" % str(t))

    print("Num zeros: %i" % (num_zero))

if __name__ == "__main__":
    main()