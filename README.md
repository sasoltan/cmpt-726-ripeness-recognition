# cmpt-726-ripeness-recognition

Note: Extracted features files can be found in ```extracted_features/```, classification can be done directly on those.

## Processing Images

To process raw images (i.e. crop, rotate, and label), run this command:
```
python process_raw_images.py raw_images/ processed_images/
```
Raw images should be in the ```raw_images/``` folder. Within that folder there should be a folder for each class containing all the images belonging to that class. Processed images will be saved in the second argument, ```processed_images/``` in this case, along with a ```classes.txt`` file (dictionary containing the index to class mapping), as well as an ```item-labels.txt``` file (another dictionary containing the image filename to class index mapping).

## Extracting Features

To extract features using a neural network, make sure you have the alexnet model installed and in a ```caffe/``` directory adjacent to this project folder. You can customize that info in the ```extract_features.py``` file. If you don't have the necessary model, the file will tell you what you're missing. run this command:
```
python extract_features.py fc8 processed_images/ features_fc8.npz
```
First command is where to get the features from the neural net. Second is directory of processed images, and third is where to save the result. Make sure the last file ends in ```.npz```

## Classification

To run classification on the extracted features call:
```
python svc.py features_fc8.npz
```
The file you pass in is the features from the previous step (or use one of the pre-extracted ones in ```extracted_features/```).