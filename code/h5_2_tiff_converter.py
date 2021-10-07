#!/usr/bin/python

import sys
import os
import flammkuchen as fl
import tifffile as tiff
import numpy as np
from progress.bar import Bar


"""
To use as a script insert the arguments in the following order:

    1 - file name to be used for saving    <save_name>_PIC#

    2 - path to the folder containing the h5 file to convert (there must me only on h5 file!)
"""



def get_h5_file(path):

    """
    Inputs: file location
    
    Returns: h5 file path
    """

    file = None
    for filename in os.listdir(path):
        if "h5" in filename:
            file = os.path.join(path,filename)
            
    if file is None:
        raise FileNotFoundError("Couldn't find any h5 file"\
            " in the given location: {}", path)
    else:
        return file
    
def load_h5(file):

    """
    Gets the location and loads the data correctly (changes some dictionary)
    """

    if os.path.exists(file):
        data = fl.load(file)

        imgs = data['Data']
        motor_meta = data['motorData']
        meta = data['metadata']
        t_stamps = data['img_time']

        #fix - not writable in json
        meta['ranges'] = str(meta['ranges'])
        meta['steps'] = str(meta['steps'])
        meta['fish_n'] = str(meta['fish_n'])

        return imgs,motor_meta,t_stamps,meta

    else:
        raise FileNotFoundError("Locarion doesn't seem to exist: {}", file)



def get_args():
    """
    unpack the arguments passed to the script
    """
    args = sys.argv

    if len(args) <3:
        raise FileNotFoundError("Input missing: save_prefix, location")
    else:
        if args[2] == ".":
            path = os.getcwd()
        else:
            path = args[2]

        return  args[1], path


def save_tiff(image, metadata, path, name):
    """
    Generate save name and save tiff file
    """
    
    save_location = os.path.join(path, "single_tiff")
    if not os.path.exists(save_location):
        os.mkdir(save_location)


    save_location = os.path.join(save_location, name)

    tiff.imwrite(save_location, image, bigtiff=False, compression='zlib',metadata=metadata)
                


def process_h5(imgs,motor_meta,t_stamps,meta, path, save_pre):
    """
    inputs:
        - imgs = list of images
        - motor_meta = stage motors metadata
        - t_stamps = time stamps before and after the picture
        - meta = general settings
        - path = location where to save
        - save_pre = save name

    Saves each picture in a single tiff file with metadata
    """
    bar = Bar('Saving Pic:', max = len(imgs))

    for i, im in enumerate(imgs):

        #get metadata
        metadata =  {'setup': meta,
                    'motors': motor_meta[i],
                    'stamps': [t_stamps[0][i],t_stamps[1][i]]
                    }

        name = save_pre + "_Pic" +  str(i) +'.tif'

        save_tiff(im, metadata, path, name)   
        bar.next()





if __name__ == "__main__":

    try:
        save_pre, path = get_args()

        print("Getting file location")
        file = get_h5_file(path)

        print("Loading")
        imgs,motor_meta,t_stamps,meta = load_h5(file)

        print("Start Processing Images:")
        process_h5(imgs,motor_meta,t_stamps,meta, path, save_pre)

    except:
        raise ValueError("Coudln't save pictures!")
