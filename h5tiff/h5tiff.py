import sys
import os
import flammkuchen as fl
import tifffile as tiff
import numpy as np
import tqdm
from pathlib import Path




MODES = ("LFM", "DEFAULT")  #add here any mode you'd like to create





class H5File:
    def __init__(self, path, save_name, mode ="LFM", save_folder = "tiff"):
        
        # checks for the data
        if not os.path.exists(Path(path)):
            raise FileNotFoundError("Location doesn't seem to exist: ", Path(path))
        
        if "h5" not in path:
            raise FileNotFoundError("No h5 file found, update file location: ", Path(path))
        
        if not isinstance(save_name, str):
            raise ValueError("Save name must be a string and not: ", type(save_name))
            
        if mode not in MODES:
            raise ValueError("Mode not found! Here's the list of supported modes: ", MODES)

            
        # save attributes
        self.path = Path(path)
        
        self.save_name = save_name
        
        self.mode = mode

        self.save_folder = save_folder
        
        self.data, self.metadata  = self.load_data()
        
        
        
        
    def load_data(self):
        """
        loads only the data from the H5 file
        it calls different functions depending on the mode:
        in this way it can be customized for any kind of h5 structure
        
        """
        if self.mode == "DEFAULT":
            try:
                data = fl.load(self.path)

            except: 
                raise SystemError("Couldn't load file!")
            
            
            metadata = {}

            if len(data.keys()) > 1:
                
                for key in data:
                    if key != "Data":
                        try:
                            metadata[key] = str(data[key])
                        except:
                            print("couldn't interpret {} as metadata".format(key))
                
                return data['Data'], metadata

            elif len(data.keys()) == 1:
                return data[list(data.keys())[0]], metadata
            else:
                raise ValueError("file is empty!")
       
        ### LFM mode ###
        
        if self.mode == "LFM":
            
            try:
                return self.load_LFM()
            except: 
                raise SystemError("Couldn't load file in LFM mode!")
            
            
############### add here any custom call to a mode specific function ##################
#         if self.mode == "<your mode>":
#             try:
#                 return <your loading function>()
#             except: 
#                 raise SystemError("Couldn't load file in <your mode> mode!")
        
        
    
       
        
    def load_LFM(self):
        """
        specific load function to load the h5 file data
        """
        data = fl.load(self.path)
        
        metadata = {}
        
        try:
            metadata['motorData'] = data['motorData']
            metadata['metadata'] = data['metadata']
            metadata['img_time'] = data['img_time']

            #fix - not writable in json
            metadata['metadata']['ranges'] = str(metadata['metadata']['ranges'])
            metadata['metadata']['steps'] = str(metadata['metadata']['steps'])
            metadata['metadata']['fish_n'] = str(metadata['metadata']['fish_n'])
            
            
        except: 
            print("Couldn't load metadata correctly!")
            
        return data['Data'],metadata
    
    
    def convert(self):
        """
        Saves each picture in a single tiff file with metadata
        """
        

        if self.mode == "DEFAULT":
                
            try:
                L = len(self.data)

            except: 
                raise ValueError("Data doesn't have length!")
            
            try:
                pbar = tqdm.tqdm(total = L, desc = "Saving: ")
                for i, im in enumerate(self.data):

                    name = self.save_name + "_Pic" +  str(i) +'.tif'

                    save_tiff(im, self.metadata, self.path, name, self.save_folder)   
                    pbar.update(1)

                pbar.close()
                print("Conversion completed")

                
            except: 
                raise ValueError("Couldn't save files!")
    
    
        if self.mode == "LFM":
            try:
                self.convert_LFM()
                print("Conversion completed")
            except: 
                raise ValueError("Couldn't save LFM files!")   

          

 ############### add here any custom call to a mode specific function ################## 
        # if self.mode == "your_mode":
        #     try:
        #         self.your_convert_function()
        #         print("Conversion completed")
        #     except: 
        #         raise ValueError("Couldn't save the files!")     

                
                
    def convert_LFM(self):
        """
        Specific function to convert the lfm pictures
        """
        try:
            L = len(self.data)

        except: 
            raise ValueError("Data doesn't have length!")
            
        try:
            
            pbar = tqdm.tqdm(total = L, desc = "Saving: ")
            
            for i, im in enumerate(self.data):

                name = self.save_name + "_Pic" +  str(i) +'.tif'
                   
                meta =  {'setup': self.metadata['metadata'],
                            'motors': self.metadata['motorData'][i],
                            'stamps': [self.metadata['img_time'][0][i],self.metadata['img_time'][1][i]]
                            } 
                    
                    
                save_tiff(im, meta, self.path, name, self.save_folder)  
                pbar.update(1)
            pbar.close()
            
            
        except: 
            raise ValueError("Couldn't save files!")
    

                
    
    ### UTILS ###
    
    
    
def save_tiff(image, metadata, path, name, save_folder):
    """
    Generate save name and save tiff file
    """
    if isinstance(save_folder, pathlib.Path):
        save_location = save_folder
    else:
        save_location = os.path.join(os.path.dirname(path), save_folder)

    if not os.path.exists(save_location):
        os.mkdir(save_location)

    save_location = os.path.join(save_location, name)

    tiff.imwrite(save_location, image, bigtiff=False, compression='zlib',metadata=metadata)
        



def get_args():
    """
    unpack the arguments passed to the script
    """
    args = sys.argv

    if len(args) <3:
        raise FileNotFoundError("Input missing: save_prefix, location, (optional) mode")
    else:
        if args[2] == ".":
            path = os.getcwd()
        else:
            path = args[2]
        
        if len(args) == 3:
            return  args[1], path
        
        if len(args) == 4:
            return   path, args[1], args[3]

        

# if __name__ == "__main__":

#     try:
#         arg_list = get_args()

#         print("Loading")
#         file = H5File(*arg_list)
        
#         print("Start Converting")
#         file.convert()

#     except:
#         raise ValueError("Coudln't save pictures!")

