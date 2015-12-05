#reads in files from features.npz
# output training and testing indices
import sys, re, math, random, numpy, operator

TRAIN_TEST_RATIO = 2/3.0

def split(filenames):
    pic_pattern = re.compile("^(\d)_(\d+)_(\d+).jpg$")

    rows = filenames.shape[0]
    originals = {}
    for i in range(rows):
        # remove the directory structure
        actual_filename = filenames[i][filenames[i].rfind("/")+1:]
        m = pic_pattern.match(actual_filename)

        label, uniq_id, inclass_id = int(m.group(1)), int(m.group(2)), int(m.group(3))
        originals.setdefault(uniq_id,[]).append(i)

    unique_count = len(originals)
    cut = int(unique_count * TRAIN_TEST_RATIO)
    randomized = list(originals.keys())
    random.shuffle(randomized)
    train, test = randomized[:cut], randomized[cut:]

    total_train = reduce(operator.add, [originals[i] for i in train])
    total_test = reduce(operator.add, [originals[i] for i in test])

    return total_train, total_test

if __name__ == "__main__":
    feature_file = sys.argv[1]
    out_file = sys.argv[2]

    features_files = numpy.load(feature_file)
    filenames = features_files['filenames']
    train, test = split(filenames)

    split = { "train": train, "test": test }
    with open(out_file, 'w') as output_file:
        output_file.write(str(split))

    print train
    print test