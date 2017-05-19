#encoding: utf-8
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

txtimg_folder="/home/ubuntu/Documents/txtimg_r"
file_of_dict='/home/ubuntu/Documents/ipadict/merge2.csv'
path_for_save_resault="/home/ubuntu/Documents/back_img_r"
background_path = '/home/ubuntu/Documents/back'

#make a list of all files
charalist= os.listdir(txtimg_folder)
allfile = []
for char in charalist:
    filelist = [i for i in os.listdir(os.path.join(txtimg_folder,char)) if i.split('.')[1] == 'png']
    allfile.extend(filelist)

print len(allfile)

#make a list of all fonts
fontlist = []
for file in allfile:
    jis1, jis2, filefont = file.split("_")
    filefont, extention = filefont.split(".")
    fontlist.append (filefont)

fontlist = list(set(fontlist))

allback = [back for back in os.listdir(background_path)if 'png' in back]




#random chose target word
with open(file_of_dict, 'rb',) as words:
    words = csv.reader(words, delimiter=',', quotechar='|',encoding='utf-8')
    wordslist=list(words)
words = []
for i in range (0,len(wordslist)):
    words.append(wordslist[i][0])


def random_img(duck):

    #select font
    targetfont = np.random.choice(fontlist, 1)
    targetfontname = targetfont[0]
    #list all files in targetfont
    fontset = [i for i in allfile if targetfontname in i]

    #2
    targetfont2 = np.random.choice(fontlist, 1)
    targetfontname2 = targetfont2[0]
    #list all files in targetfont
    fontset2 = [i for i in allfile if targetfontname2 in i]


    u = random.choice(words)

    #2
    u2 =random.choice(words)




    #unicode for target words
    dictwords = []
    for c in u:
        dictwords.append('%04x' % ord(c))


    size = len(dictwords)

    #2
    dictwords2 = []
    for c in u2:
        dictwords2.append('%04x' % ord(c))

    size2 = len(dictwords2)



    #get imgfilename
    voc = []
    for i in dictwords:
        for j in fontset:
            j1,j2,font = j.split('_')
            if i in j1:
                voc.append(j)

    voc = np.asarray(voc)
    #2
    voc2 = []
    for i in dictwords2:
        for j in fontset2:
            j1,j2,font = j.split('_')
            if i in j1:
                voc2.append(j)

    voc2 = np.asarray(voc2)


    #single img process
    ims = []

    for ind, i in enumerate(voc):
        jis1, jis2, filefont = i.split("_")
        char = chr(int(jis1,16))
        im_folder = os.path.join(txtimg_folder,char)
        im = Image.open(os.path.join(im_folder,i))
        ims.append(im)


    if ims == []:
        return

    #2
    ims2 = []

    for ind, i in enumerate(voc2):
        jis1, jis2, filefont = i.split("_")
        char = chr(int(jis1,16))
        im_folder = os.path.join(txtimg_folder,char)
        im = Image.open(os.path.join(im_folder,i))
        ims2.append(im)

    if ims2 == []:
        return



    #creat a new image as a canvas
    widths, heights = zip(*(i.size for i in ims))
    total_width = sum(widths)
    max_height = max(heights)

    #2
    widths2, heights2 = zip(*(i.size for i in ims2))
    total_width2 = sum(widths2)
    max_height2 = max(heights2)

    #background
    backg = random.choice(allback)
    canvas = Image.open(os.path.join(background_path,backg))
    #rotate angle
    ang = np.random.randint(-20,20)

    ang2 = np.random.randint(-20,20)

    #affine
    m = np.random.uniform(-0.3,0.3)
    n = np.random.uniform(-0.3,0.3)
    if abs(m)>abs(n):
        n = 0
    else:
        m=0

    m2 = np.random.uniform(-0.3,0.3)
    n2 = np.random.uniform(-0.3,0.3)
    if abs(m2)>abs(n2):
        n2 = 0
    else:
        m2=0


    #resize rate
    if total_width>total_width2:
        if (total_width+15*size) > (max_height+10):
            rate = np.random.uniform(0.4,(500/(total_width+15*size)))
        else:
            rate = np.random.uniform(0.4,(500/(max_height+10)))
    else:
        if (total_width2+15*size) > (max_height2+10):
            rate = np.random.uniform(0.4,(500/(total_width2+15*size)))
        else:
            rate = np.random.uniform(0.4,(500/(max_height2+10)))
    if rate>1:
        rate=1

    #avoid extrame error
    if rate*min(heights)<1 :
        return
    elif rate*min(widths) <1:
        return
    if (total_width+15*size)*rate >= 500:
        return
    elif ((max_height+10)*rate)+((max_height2+10)*rate) >= 500:
        return
    elif 500- ((max_height+10)*rate)-(((max_height2+10)*rate))<((max_height2+10)*rate):
        return

    #2
    if rate*min(heights2)<1 :
        return
    elif rate*min(widths2) <1:
        return
    if (total_width2+(15*size2))*rate >= 500:
        return



    #random position
    x_p = np.random.randint(0,500-((total_width+15*size)*rate))
    y_p = np.random.randint(0, 500- ((max_height*rate)+10+(max(heights2)*rate)+10))
    x_p2 = np.random.randint(0,500-((total_width2+15*size2)*rate))
    y_p2 = y_p



    txt = []
    h1 = []
    x_offset = 0


    #combine image
    for ind, i in enumerate(ims):

        orin_w, orin_h = i.size
        new_w = orin_w + int(abs(orin_h*m))
        new_h = orin_h + int(abs(orin_w*n))
        i = i.transform((new_w,new_h),Image.AFFINE,(1,-m,
            int(orin_h*m) if m<0 else 0,
            -n, 1, int(orin_w*n)if n<0 else 0), Image.BILINEAR)



        i = i.rotate(ang,expand=True)
        #set random gap
        y_gap = np.random.randint(0,5)
        x_gap = np.random.randint(int(2*rate),int(10*rate))

        w, h = i.size

        #adjust position
        if ind > 0:
            previous = ims[ind - 1]
            wp, hp = previous.size
            if wp < (0.6*max(widths)):
                x_offset += int(wp*rate) + x_gap
            else:
                x_offset += int(max(widths)*rate) + x_gap
        else:
            x_offset += 0 + x_gap



        if orin_h<(0.4*max(heights)):
            y_b = 500- int((max_height*0.7*rate)+y_gap+(max(heights2)*rate)+10)
        else:
            y_b = 500-int((i.size[1]*rate)+y_gap+(max(heights2)*rate)+10)


        i=i.resize((int(w*rate),int(h*rate)),Image.BILINEAR)

        w, h = i.size


        canvas.paste(i, ((x_offset+x_p), (y_b-y_p)), i)

        #str(x,y,w,h)
        i_x = str(x_offset +x_p + (w/2))
        i_y = str(y_b- y_p+(h/2))
        i_w = str(w)
        i_h = str(h)

        #center of image
        jis1, jis2, filefont = voc[ind].split("_")
        char = chr(int(jis1,16))
        txt.append((char+" "+i_x+" "+i_y+" "+i_w+" "+i_h))






    txt2 = []
    x_offset2 = 0

    #2
    for ind, i in enumerate(ims2):

        orin_w, orin_h = i.size

        orin_w, orin_h = i.size
        new_w = orin_w + int(abs(orin_h*m2))
        new_h = orin_h + int(abs(orin_w*n2))
        i = i.transform((new_w,new_h),Image.AFFINE,(1,-m2,
            int(orin_h*m2) if m2<0 else 0,
            -n2, 1, int(orin_w*n2)if n2<0 else 0), Image.BILINEAR)

        i = i.rotate(ang,expand=True)
        #set random gap
        y_gap = np.random.randint(0,5)
        x_gap = np.random.randint(int(2*rate),int(10*rate))

        w, h = i.size

        #adjust position
        if ind > 0:
            previous = ims2[ind - 1]
            wp, hp = previous.size
            if wp < (0.6*max(widths2)):
                x_offset2 += int(wp*rate) + x_gap
            else:
                x_offset2 += int(max(widths2)*rate) + x_gap
        else:
            x_offset2 += 0 + x_gap

        if orin_h<(0.4*max(heights2)):
            y_b = 500- int(max_height2*0.7*rate)-y_gap
        else:
            y_b = 500-int(i.size[1]*rate)-y_gap



        i=i.resize((int(w*rate),int(h*rate)),Image.BILINEAR)

        w, h = i.size


        canvas.paste(i, ((x_offset2+x_p2), (y_b-y_p2)), i)

        #str(x,y,w,h)
        i_x = str(x_offset2 +x_p2 + (w/2))
        i_y = str(y_b- y_p2+(h/2))
        i_w = str(w)
        i_h = str(h)

        #center of image

        jis1, jis2, filefont = voc2[ind].split("_")
        char = chr(int(jis1,16))

        txt2.append((char+" "+i_x+" "+i_y+" "+i_w+" "+i_h))

    txt = txt + txt2
    txt = "\n".join(i for i in txt)

    if len(str(duck))<7:
        name = '0'*(7-len(str(duck))) + str(duck)
    else:
        name = str(duck)

    with codecs.open(os.path.join(path_for_save_resault,"%s.txt" %(name)), "w", 'utf-8') as output:
        output.write(txt)
    canvas.save(os.path.join(path_for_save_resault,"%s.png" %(name)))

start = time.time()
for duck in range(0,50):
    random_img(duck)
    print('Running', duck)

end = time.time()

print (end - start)
