import sys, Image
from os import listdir
from os.path import isfile, isdir, join

image_dimensions = (256, 256)

# assumes image width is greater than height
def square_crop(image):
    width, height = image.size
    half_diff = (width - height) / 2
    return image.crop((half_diff, 0, height + half_diff, height))

def main():
    infolder = sys.argv[1]
    outfolder = sys.argv[2]

    classes = []
    item_mapping = {}
    unique_pic_count = 1
    for classdir in listdir(infolder):
        full_dir = join(infolder, classdir)
        if isdir(full_dir):
            classes.append(classdir)
            pic_count = 1
            for filename in listdir(full_dir):
                filepath = join(full_dir, filename)
                if isfile(filepath):
                    cropped_image = square_crop(Image.open(filepath))
                    cropped_image.thumbnail(image_dimensions, Image.ANTIALIAS)
                    # rotate image four ways
                    for i in range(4):
                        out_filename = "%s_%i_%i.jpg" % (classes.index(classdir), unique_pic_count, pic_count)
                        cropped_image.rotate(i * 90).save(join(outfolder, out_filename))
                        item_mapping[out_filename] = classes.index(classdir)
                        pic_count += 1
                    unique_pic_count += 1

    class_mapping = {}
    for i, c in enumerate(classes):
        class_mapping[i] = c

    with open(join(outfolder, "classes.txt"), 'w') as output_file:
        output_file.write(str(class_mapping))

    with open(join(outfolder, "item-labels.txt"), 'w') as output_file:
        output_file.write(str(item_mapping))

if __name__ == "__main__":
    main()