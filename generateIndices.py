#reads in files and output indices
import sys
import os, re
import math


def main():
    infolder = sys.argv[1]

    master = []

    pic_pattern = re.compile("^(\d)_(\d+).jpg$")
    counter=0
    max_0=0
    max_1=0
    max_2=0
    max_3=0
    for image_file in os.listdir(infolder):
        m = pic_pattern.match(image_file)
        if m:

            master.append((int(m.group(1)), int(m.group(2)), counter))


            if int(m.group(1))==0 and int(m.group(2)) > max_0:
                max_0=int(m.group(2))
            elif int(m.group(1))==1 and int(m.group(2))> max_1:
                max_1=int(m.group(2))
            elif int(m.group(1))==2 and int(m.group(2)) > max_2:
                max_2=int(m.group(2))
            else:
                max_3=int(m.group(2))
            counter+=1

    master = sorted(master, key=lambda x: (x[0],x[1]))

    trainIndex, testIndex = [], []
    for tuple in master:
        if tuple[0]==0 and tuple[1]<=int(math.floor(max_0/4*2/3))*4:
            trainIndex.append(tuple[2])
        elif tuple[0]==0:
            testIndex.append(tuple[2])

        if tuple[0]==1 and tuple[1]<=int(math.floor(max_1/4*2/3))*4:
            trainIndex.append(tuple[2])
        elif tuple[0]==1:
            testIndex.append(tuple[2])

        if tuple[0]==2 and tuple[1]<=int(math.floor(max_2/4*2/3))*4:
            trainIndex.append(tuple[2])
        elif tuple[0]==2:
            testIndex.append(tuple[2])

        if tuple[0]==3 and tuple[1]<=int(math.floor(max_3/4*2/3))*4:
            trainIndex.append(tuple[2])
        elif tuple[0]==3:
            testIndex.append(tuple[2])

    print trainIndex
    print ""
    print testIndex

    return trainIndex, testIndex





if __name__ == "__main__":
    main()