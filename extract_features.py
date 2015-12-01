import numpy, sys, os, caffe, re, time
from os.path import join

caffe_root = '../caffe/'
caffe_model = "bvlc_alexnet"
output_layer = "fc7"

def model_precheck(caffe_root, caffe_model):
    if os.path.isfile(get_model_path(caffe_root, caffe_model)):
        return True
    else:
        print("Pre-trained model not downloaded, please download the %s model." % (caffe_model))
        return False

def get_model_path(caffe_root, caffe_model):
    return "%smodels/%s/%s.caffemodel" % (caffe_root, caffe_model, caffe_model)

def get_proto_path(caffe_root, caffe_model):
    return "%smodels/%s/deploy.prototxt" % (caffe_root, caffe_model)

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def main():
    if not model_precheck(caffe_root, caffe_model):
        return False

    pic_folder = sys.argv[1]
    feature_file = sys.argv[2]

    # get and load the list of images. There's only ~800 images totalling ~2.5mb so don't worry about batching
    image_list, labels = [], []
    pic_pattern = re.compile("^(\d)_(\d)+.jpg$")
    for image_file in os.listdir(pic_folder):
        m = pic_pattern.match(image_file)
        if m:
            image_list.append(os.path.join(pic_folder, image_file))
            labels.append(int(m.group(1)))

    filenames = numpy.array(image_list)
    labels = numpy.array(labels)
    layer_outputs = []

    caffe.set_mode_cpu()
    proto_path = get_proto_path(caffe_root, caffe_model)
    model_path = get_model_path(caffe_root, caffe_model)
    net = caffe.Net(proto_path, model_path, caffe.TEST)

    start = time.time()
    for images in batch(image_list, 50):
        np_images = numpy.array(map(lambda i: caffe.io.load_image(i).transpose((2, 0, 1)), images))

        net.blobs['data'].reshape(len(images),3,227,227)
        net.blobs['data'].data[...] = np_images
        out = net.forward()

        print("Processd batch. Time so far: %f" % (time.time() - start))
        layer_outputs.append(net.blobs[output_layer].data)

    features = numpy.concatenate(tuple(layer_outputs), axis=0)
    numpy.savez(feature_file, features=features, filenames=filenames, labels=labels)
    print("Finished. Total time: %f" % (time.time() - start))

if __name__ == "__main__":
    main()