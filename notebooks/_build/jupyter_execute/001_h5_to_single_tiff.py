#!/usr/bin/env python
# coding: utf-8

# # Conversion from a H5 file with a list of images and metadata to tif files
# 
# Converting all the images in a h5 file and saving them in a folder 
# 

# In[1]:



from h5_2_tiff_converter import *


# In[ ]:


master_folder = r"E:\Datasets\file.h5"
save_name = "save_name"
mode = "DEFAULT"


# In[ ]:


file = H5File(master_folder,save_name,mode)


# In[ ]:


file.mode


# In[ ]:


os.path.dirname(master_folder)


# In[ ]:


file.convert()


# In[ ]:





# In[ ]:





# In[ ]:




