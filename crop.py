import sys, Image
from os import listdir
from os.path import isfile, join

# assumes image width is greater than height
def square_crop(image):
    width, height = image.size
    half_diff = (width - height) / 2
    return image.crop((half_diff, 0, height + half_diff, height))

def main():
    infolder = sys.argv[1]
    outfolder = sys.argv[2]

    for filename in listdir(infolder):
        filepath = join(infolder, filename)
        if isfile(filepath):
            square_crop(Image.open(filepath)).save(join(outfolder, filename))

if __name__ == "__main__":
    main()