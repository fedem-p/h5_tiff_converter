# Getting Started


## Installation

You can easily install the package with [pypi](https://pypi.org/project/h5tiff/):

```
    pip install h5tiff
```

or you can install it with:

```
    pip install -e path_to_h5tiff/h5tiff
```

which allows you to customize the converter to your needs (see an example [here](#-adding-your-own-mode)).



## Using and Customizing

This package was specifically written to be customized in order to process correctly differente h5 file strurctures:

At the moment there're only two modes:

- default
- LFM

 


> **<font color='blue'>⚠  WARNING! </font>**
> <font color='blue'>The data used as input is supposed to be a list of images/stack which will be separated in single Tiff files. </font>



### Default mode
This is a very crude mode that tries to accept various cases underneath it.

The h5 file is opened expeting to find the data in a dictionary format, where the 'Data'  key is where the data is stored.

```Python
    yourdata = h5file['Data'] 
```
Any other key is instead considered as metadata and inserted in a single dictionary.
When the pictures are saved as Tiff files the metadata is added to each one.

### LFM mode
This a specific mode which expects the data in the following format:

```Python
    yourdata = {
                'Data': list_of_images,
                'motorData' = motorData,
                'metadata' = metadata,
                'img_time' = img_time,
                }
```
- where `motorData` is a list of information regarding the position of the stage motors of the light field microscope. When the tiff file is saved only the correct position is attached as metadata.
- `metadata` is general information and specifics about the whole set of images. This information is attached to every tiff file.
- Finally, `img_time` is a 2D list of time stamps (one before the picture was taken, one after).  
Only the times corresponding to a specific image are attached in the metadata of that image.


### Adding your own mode

To add a different mode to the code there are four modifications to be made:

1. You need to add the name of your mode [here](https://github.com/fedem-p/h5_tiff_converter/blob/fd29d512683deaa8c37f982b3f865ff652a7a370/h5tiff/h5tiff.py#L14):
    ```python
    MODES = ("LFM", "DEFAULT", "ADD_HERE_YOUR_MODE_NAME")
    ```

2. Then, you need to write a specific function to call for loading and converting the images.  You can add it at the end and use some of the previous code as a reference.
    - [Load]() function:
        - The funtion to load does't need any input beause the path to the h5 file is requested when creating the converter object.
        - It has to return the data (**list of images**) and metadata (**dictionary**)
    - [Convert]() function:
        - It doesn't need any inputs, and it returns nothing
        - We suggest to make use of the `save_tiff` function, which requires an image, a metadata dictionary, a saving name, and a saving path.

3. Finally, you need to connect the functions you wrote with the main processing pipeline.  Just copy the examples that you find commented [here]() (load), and [here]() (convert)





