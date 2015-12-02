import numpy, sys, os, caffe, re, time

caffe_root = '../caffe/'
caffe_model = "bvlc_alexnet"
output_layer = "fc7"
network_dimensions = (227, 227, 3)

def preflight_check(caffe_root, caffe_model):
    model_path = get_model_path(caffe_root, caffe_model)
    proto_path = get_proto_path(caffe_root, caffe_model)
    mean_image_path = get_mean_image_path(caffe_root, caffe_model)
    if not os.path.isfile(model_path):
        print("Pre-trained model not downloaded, please download the %s model." % (caffe_model))
        return False
    elif not os.path.isfile(proto_path):
        print("Can't find proto at %s." % (proto_path))
        return False
    elif not os.path.isfile(mean_image_path):
        print("Can't find mean image at %s." % (mean_image_path))
        return False
    else:
        return True

def get_model_path(caffe_root, caffe_model):
    return "%smodels/%s/%s.caffemodel" % (caffe_root, caffe_model, caffe_model)

def get_proto_path(caffe_root, caffe_model):
    return "%smodels/%s/deploy.prototxt" % (caffe_root, caffe_model)

def get_mean_image_path(caffe_root, caffe_model):
    return "%smodels/%s/imagenet_mean.binaryproto" % (caffe_root, caffe_model)

def get_mean_image(caffe_root, caffe_model):
    mean_image_path = get_mean_image_path(caffe_root, caffe_model)
    blob = caffe.proto.caffe_pb2.BlobProto()
    data = open(mean_image_path, 'rb' ).read()
    blob.ParseFromString(data)
    arr = numpy.array(caffe.io.blobproto_to_array(blob))
    return arr[0].transpose((1, 2, 0))

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def process_image(image_url, mean_image):
    image = caffe.io.load_image(image_url)
    # subtract the mean
    image = image - mean_image
    # resize image
    image = caffe.io.resize_image(image, network_dimensions)
    return image.transpose((2, 0, 1))

def main():
    if not preflight_check(caffe_root, caffe_model):
        return False

    pic_folder = sys.argv[1]
    feature_file = sys.argv[2]

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
    mean_image = get_mean_image(caffe_root, caffe_model)
    proto_path = get_proto_path(caffe_root, caffe_model)
    model_path = get_model_path(caffe_root, caffe_model)
    net = caffe.Net(proto_path, model_path, caffe.TEST)

    start = time.time()
    for images in batch(image_list, 50):
        np_images = numpy.array(map(lambda i: process_image(i, mean_image), images))

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