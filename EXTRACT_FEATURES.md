Make a directory to store features:
```
mkdir caffe/examples/_temp
```
Generate list of files to process:
```
find `pwd`/cmpt-726-ripeness-recognition/processed_images -type f -exec echo {} \; > caffe/examples/_temp/temp.txt
```
Use nano/vim to remove the label files. Add null labels to each image:
```
sed "s/$/ 0/" caffe/examples/_temp/temp.txt > caffe/examples/_temp/file_list.txt
```
Download some thing:
```
./caffe/data/ilsvrc12/get_ilsvrc_aux.sh
```
Copy the proto:
```
cp caffe/examples/feature_extraction/imagenet_val.prototxt caffe/examples/_temp/
```
Extract Features (you may need to download the model here):
```
./build/tools/extract_features.bin models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel examples/_temp/imagenet_val.prototxt fc7 examples/_temp/features 10 lmdb
```
Features are now stored in the ```examples/_temp/features``` directory as an ```lmdb``` file. To process them into text, use ```read_features.py```:
```
python read_features.py
```
You can look into the ```read_features.py``` file to see exactly what it's doing.
