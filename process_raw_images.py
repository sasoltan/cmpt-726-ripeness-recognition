import sys, Image
from os import listdir
from os.path import isfile, isdir, join

# assumes image width is greater than height
def square_crop(image):
    width, height = image.size
    half_diff = (width - height) / 2
    return image.crop((half_diff, 0, height + half_diff, height))

def main():
    infolder = sys.argv[1]
    outfolder = sys.argv[2]

    classes = []
    for classdir in listdir(infolder):
        full_dir = join(infolder, classdir)
        if isdir(full_dir):
            classes.append(classdir)
            pic_count = 1
            for filename in listdir(full_dir):
                filepath = join(full_dir, filename)
                if isfile(filepath):
                    out_filename = join(outfolder, "%s_%i.jpg" % (classdir, pic_count))
                    square_crop(Image.open(filepath)).save(out_filename)
                    pic_count += 1

if __name__ == "__main__":
    main()