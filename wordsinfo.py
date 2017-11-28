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


txtimg_folder="/home/ubuntu/Documents/txtimg"
file_of_dict='/home/ubuntu/Documents/ipadict/merge2.csv'
path_for_save_resault="/home/ubuntu/Documents/back_img"
background_path = '/home/ubuntu/Documents/back'

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

allback = [back for back in os.listdir(background_path)if 'png' in back]



#make a list of all vocabuary in dict
with open(file_of_dict, 'rb',) as words:
    words = csv.reader(words, delimiter=',', quotechar='|',encoding='utf-8')
    wordslist=list(words)
words = []
for i in range (0,len(wordslist)):
    words.append(wordslist[i][0])

chs = []
for i in words:
	for j in i:
		chs.append(j)

print(len(set(words)))
