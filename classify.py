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

if __name__ == "__main__":
    main()