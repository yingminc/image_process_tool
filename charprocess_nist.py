from __future__ import division
from PIL import Image
from PIL import ImageDraw
import random, os, glob
import numpy as np
import collections, os, shutil
from skimage import img_as_ubyte
import cv2
import skimage
import fileinput
#from builtins import bytes,chr


txtimg_folder = '/home/mehdi/Documents/handwritting_project/data/latin_hw_characters/by_class'  #/home/yingminc/Documents/by_class'
path_for_save_result = '/home/mehdi/Documents/handwritting_project/data/character_extraction/nist_etl_processed/'  #'/home/yingminc/Documents/by_class_r'

os.mkdir(path_for_save_resault)

#make a list of all files
allhex = [filename for filename in os.listdir(txtimg_folder)]
charlist = []

for hexchar in allhex:
    char = hexchar.decode('hex')
    print char
    charlist.append(char)
    # make folders for save
    if not os.path.isdir(path_for_save_result+char):
        os.makedirs(os.path.join(path_for_save_result, char))

    #get all the folders of char
    charfolder = os.path.join(txtimg_folder,hexchar)
    hsf = [folders for folders in os.listdir(charfolder) if (folders.split('_')[0]== 'hsf') and (('.') not in folders)]

    charallfile=[]
    #process each hsf folder
    for hsffolder in hsf:
        charallfile = os.listdir(os.path.join(charfolder,hsffolder))
        #process each img
        for i in charallfile:

            im = cv2.imread(os.path.join(os.path.join(charfolder,hsffolder),i))
            img_p = im.copy()
            img_p = cv2.cvtColor(img_p, cv2.COLOR_RGB2GRAY)
            ret,thresh = cv2.threshold(img_p,127,255,cv2.THRESH_BINARY_INV)
            # #remove noise
            # kernel = np.ones((2,2), np.uint8)
            # thresh= cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            contours, hier= cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #include all contours in the boundingRect
            xall = []
            yall = []
            wall = []
            hall = []
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)
                xall.append(x)
                yall.append(y)
                wall.append(w+x)
                hall.append(h+y)


            x = min(xall)
            y = min(yall)
            h = max(hall)-min(yall)
            w = max(wall)-min(xall)

            im_c = im[y:y+h, x:x+w]
            img=Image.fromarray(im_c)

            im = img.convert("RGBA")
            datas = im.getdata()
            newdata = []
            for item in datas:
                if item[0] == 255 and item[1] ==255 and item[2] ==255: #white
                    newdata.append((255,255,255,0)) #transparent
                else:
                    newdata.append(item)
            im.putdata(newdata)
            im.save(os.path.join(os.path.join(path_for_save_resault,char),char+'_'+i))
