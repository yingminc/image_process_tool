from __future__ import division
from PIL import Image
from PIL import ImageDraw
import random, os, glob
import numpy as np
from multiprocessing import Pool
import collections, os, shutil
from skimage import img_as_ubyte
import cv2
import skimage
import fileinput
import sys
import time
import unicodedata
import unicodecsv as csv
from builtins import bytes,chr
import time
import codecs

txtimg_folder="/home/ubuntu/Documents/txtimg"
path_for_save_resault="/home/ubuntu/Documents/txtimg_r"


#make a list of all files
allfile = [filename for filename in os.listdir(txtimg_folder) if filename.split('.')[1] == 'png']

#make a list of all fonts
fontlist = []
charalist = []
for file in allfile:
    jis1, jis2, filefont = file.split("_")
    filefont, extention = filefont.split(".")
    charalist.append (jis1)
    fontlist.append (filefont)

charalist = list(set(charalist))
fontlist = list(set(fontlist))


for char in charalist:
    ji = chr(int(char,16))
    os.makedirs(os.path.join("/home/ubuntu/Documents/txtimg_r",ji))


for i in allfile:

    jis1, jis2, filefont = i.split("_")
    char = chr(int(jis1,16))
    charfolder = os.path.join(path_for_save_resault, char)

    im = cv2.imread(os.path.join(txtimg_folder,i))
    img_p = im.copy()
    img_p = cv2.cvtColor(img_p, cv2.COLOR_RGB2GRAY)
    ret,thresh = cv2.threshold(img_p,127,255,cv2.THRESH_BINARY_INV)
    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)


    im = im[y:y+h, x:x+w]
    img=Image.fromarray(im)

    im = img.convert("RGBA")
    datas = im.getdata()
    newdata = []
    for item in datas:
        if item[0] == 255 and item[1] ==255 and item[2] ==255: #white
            newdata.append((255,255,255,0)) #transparent
        else:
            newdata.append(item)
    im.putdata(newdata)
    im.save(os.path.join(charfolder,i))
