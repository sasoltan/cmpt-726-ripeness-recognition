#reads in files from features.npz
# output training and testing indices
import sys
import re
import math
import numpy as np

def generateIndex():

    feature_file = sys.argv[1]

    features_files = np.load(feature_file)
    filenames = features_files['filenames']

    #master list to hold information
    master = []
    #number of files in each pile
    numberOfFiles_0=0
    numberOfFiles_1=0
    numberOfFiles_2=0
    numberOfFiles_3=0


    pic_pattern = re.compile("^(\d)_(\d+).jpg$")

    for i in range(filenames.shape[0]):
        wholeFileName = filenames[i].split("/")[1]

        m = pic_pattern.match(wholeFileName)
        if m:
            # label, number within group, index in the feature vector/matrix
            master.append((int(m.group(1)), int(m.group(2)), i))

            if int(m.group(1)) == 0 and int(m.group(2)) > numberOfFiles_0:
                numberOfFiles_0=int(m.group(2))
            elif int(m.group(1)) == 1 and int(m.group(2))> numberOfFiles_1:
                numberOfFiles_1=int(m.group(2))
            elif int(m.group(1)) == 2 and int(m.group(2)) > numberOfFiles_2:
                numberOfFiles_2=int(m.group(2))
            elif int(m.group(1)) == 3 and int(m.group(2)) > numberOfFiles_3:
                numberOfFiles_3=int(m.group(2))

    sortedMaster = sorted(master, key=lambda x: (x[0],x[1]))

    trainIndex, testIndex = [], []
    trainingShare = .8
    #number of training data points
    limit_0=int(math.floor(numberOfFiles_0/4*trainingShare))*4
    limit_1=int(math.floor(numberOfFiles_1/4*trainingShare))*4
    limit_2=int(math.floor(numberOfFiles_2/4*trainingShare))*4
    limit_3=int(math.floor(numberOfFiles_3/4*trainingShare))*4

    for tuple in sortedMaster:
        if tuple[0]==0 and tuple[1]<=limit_0:
            trainIndex.append(tuple[2])
        elif tuple[0]==0:
            testIndex.append(tuple[2])

        if tuple[0]==1 and tuple[1]<=limit_1:
            trainIndex.append(tuple[2])
        elif tuple[0]==1:
            testIndex.append(tuple[2])

        if tuple[0]==2 and tuple[1]<=limit_2:
            trainIndex.append(tuple[2])
        elif tuple[0]==2:
            testIndex.append(tuple[2])

        if tuple[0]==3 and tuple[1]<=limit_3:
            trainIndex.append(tuple[2])
        elif tuple[0]==3:
            testIndex.append(tuple[2])


    return trainIndex, testIndex




if __name__ == "__main__":
    generateIndex()