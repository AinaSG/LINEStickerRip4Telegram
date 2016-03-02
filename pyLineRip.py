import urllib
import os
import urllib2
import fnmatch
from pylab import *
from scipy.misc import imresize


URL = "null"

SETNAME = "default"

BASE_URL = "null"

FORMAT = ".png"

ID = "null"



def make_dir():
    os.makedirs("./"+SETNAME)

def download_stickers():
    for img_id in ID:
        my_url = BASE_URL+str(img_id)+FORMAT
        saveurl = "./"+SETNAME+"/"+str(img_id)+FORMAT
        urllib.urlretrieve(my_url, saveurl)
        print "Saved" + saveurl + " from " + my_url
        
print "Enter desired sticker pack URL"
print "Example: https://store.line.me/stickershop/product/1252/en"

URL = raw_input("Sticker Pack URL: ")
response = urllib2.urlopen(URL)
page_source = response.read()

#print page_source

for line in page_source.splitlines():
    line = str(line).strip()
    if line.startswith("baseURL:"):
        line = line.replace("baseURL: '", "")
        line = line.replace("',", "")
        BASE_URL = line + "stickers/"
        print BASE_URL
    
    if line.startswith("ids: "):
        line = line.replace("ids: [", "")
        line = line.replace("]", "")
        ID = line.split(",")
        ID = [int(i) for i in ID]
        print ID
        
if BASE_URL == "null" :
    print "Sorry, I can't recognize this page"
    sys.exit()
    
if ID == "null" :
    print "Sorry, I can't recognize this page"
    sys.exit()
    
print "Everything seems alright!"
SETNAME = raw_input("Choose a name for this pack [default]:") or "default"

make_dir()
download_stickers()

print "Done!"
resize = raw_input("Do you want me to resize it? Y/N: ") or "N"

if resize == "Y":
    print "Resizing the stickers!... Thanks to isman7 on GitHub for the resizing script!"
    # -*- coding: utf-8 -*-
    """
    Created on Sun May 24 01:00:37 2015

    @author: isman7
    """

    #### Folder scanning ####

    matches = []
    dirname = "./"+SETNAME
    try: 
        for root, dirnames, filenames in os.walk(dirname):
            for filename in fnmatch.filter(filenames, '*.png'):
                matches.append(os.path.join(root, filename))
                
    except IOError: 
        print "Folder not found. Using current directory: " + os.curdir 
        for root, dirnames, filenames in os.walk(os.curdir):
            for filename in fnmatch.filter(filenames, '*.png'):
                matches.append(os.path.join(root, filename))
                
    for stickers in matches:     
        sticker = imread(stickers)     
        #print sticker.shape       
        stshape = sticker.shape    
           
        if stshape[0] > stshape[1]:           
            new_width = int(512*stshape[1]/stshape[0])                 
            new_stshape = ( 512, new_width, stshape[2])                            
            new_sticker = imresize(sticker, new_stshape)          
            imsave(stickers, new_sticker )  
                    
        elif stshape[0] < stshape[1]:            
            new_height = int(512*stshape[0]/stshape[1])                  
            new_stshape = ( new_height, 512, stshape[2])                          
            new_sticker = imresize(sticker, new_stshape)         
            imsave(stickers, new_sticker ) 
                  
        elif stshape[0] == stshape[1]:           
            new_stshape = (512, 512, stshape[2])                          
            new_sticker = imresize(sticker, new_stshape)          
            imsave(stickers, new_sticker )
        
print "DONE! you will find your stickers at " + "./"+SETNAME

