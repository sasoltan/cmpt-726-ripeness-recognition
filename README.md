# cmpt-726-ripeness-recognition

## Processing Images

To process raw images (i.e. crop, rotate, and label), run this command:
```
python process_raw_images.py raw_images/ processed_images/
```
Raw images should be in the ```raw_images/``` folder. Within that folder there should be a folder for each class containing all the images belonging to that class. Processed images will be saved in the second argument, ```processed_images/``` in this case, along with a ```classes.txt`` file (dictionary containing the index to class mapping), as well as an ```items.txt``` file (another dictionary containing the image filename to class index mapping).