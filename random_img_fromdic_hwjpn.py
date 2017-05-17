#encoding: utf-8
from __future__ import division, print_function
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
from random import shuffle

txtimg_folder="/home/ubuntu/Documents/JPN_test_r"
file_of_dict='/home/ubuntu/Documents/ipadict/merge2.csv'
path_for_save_resault="/home/ubuntu/Documents/JPN_test_r_img"
background_path = '/home/ubuntu/Documents/back'

#


htjhyr5tseyjhrt5jik
#make a list of all char
charalist = os.listdir(txtimg_folder)

charlist = list(set(charalist))

charlist = [g.decod


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
            y_b = 500- int((max_height*0.7*rate)+y_gap+(max_height2*rate)+(max_height3*rate)+10)
        else:
            y_b = 500-int((i.size[1]*rate)+y_gap+(max_height2*rate)+(max_height3*rate)+10)


        i=i.resize((int(w*rate),int(h*rate)),Image.BILINEAR)

        w, h = i.size


        canvas.paste(i, ((x_offset+x_p), (y_b-y_p)), i)

        #str(x,y,w,h)
        i_x = str(x_offset +x_p + (w/2))
        i_y = str(y_b- y_p+(h/2))
        i_w = str(w)
        i_h = str(h)

        #center of image
        txt.append((dictwords[ind]+" "+i_x+" "+i_y+" "+i_w+" "+i_h))

        charcolist[dictwords[ind]] +=1





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
            y_b = 500- int((max_height2*0.7*rate)+(max_height3*rate)+10+y_gap)
        else:
            y_b = 500-int((i.size[1]*rate)+(max_height3*rate)+10+y_gap)



        i=i.resize((int(w*rate),int(h*rate)),Image.BILINEAR)

        w, h = i.size


        canvas.paste(i, ((x_offset2+x_p2), (y_b-y_p2)), i)

        #str(x,y,w,h)
        i_x = str(x_offset2 +x_p2 + (w/2))
        i_y = str(y_b- y_p2+(h/2))
        i_w = str(w)
        i_h = str(h)

        #center of image
        txt2.append((dictwords2[ind]+" "+i_x+" "+i_y+" "+i_w+" "+i_h))


        charcolist[dictwords2[ind]] +=1

    #3
    txt3 = []
    x_offset3 = 0
    for ind, i in enumerate(ims3):

        orin_w, orin_h = i.size

        orin_w, orin_h = i.size
        new_w = orin_w + int(abs(orin_h*m3))
        new_h = orin_h + int(abs(orin_w*n3))
        i = i.transform((new_w,new_h),Image.AFFINE,(1,-m3,
            int(orin_h*m3) if m3<0 else 0,
            -n3, 1, int(orin_w*n3)if n3<0 else 0), Image.BILINEAR)

        i = i.rotate(ang,expand=True)
        #set random gap
        y_gap = np.random.randint(0,5)
        x_gap = np.random.randint(int(2*rate),int(10*rate))

        w, h = i.size

        #adjust position
        if ind > 0:
            previous = ims3[ind - 1]
            wp, hp = previous.size
            if wp < (0.6*max(widths3)):
                x_offset3 += int(wp*rate) + x_gap
            else:
                x_offset3 += int(max(widths3)*rate) + x_gap
        else:
            x_offset2 += 0 + x_gap

        if orin_h<(0.4*max(heights3)):
            y_b = 500- int(max_height3*0.7*rate)-y_gap
        else:
            y_b = 500-int(i.size[1]*rate)-y_gap



        i=i.resize((int(w*rate),int(h*rate)),Image.BILINEAR)

        w, h = i.size


        canvas.paste(i, ((x_offset3+x_p3), (y_b-y_p3)), i)

        #str(x,y,w,h)
        i_x = str(x_offset3 +x_p3 + (w/2))
        i_y = str(y_b- y_p3+(h/2))
        i_w = str(w)
        i_h = str(h)

        #center of image
        txt3.append((dictwords3[ind]+" "+i_x+" "+i_y+" "+i_w+" "+i_h))


        charcolist[dictwords3[ind]] +=1



    txt = txt + txt2 +txt3
    txt = "\n".join(i for i in txt)

    if len(str(duck))<7:
        name = '0'*(7-len(str(duck))) + str(duck)
    else:
        name = str(duck)

    with codecs.open(os.path.join(path_for_save_resault,"%s.txt" %(name)), "w" ,'utf-8') as output:
        output.write(txt)
    canvas.save(os.path.join(path_for_save_resault,"%s.png" %(name)))


def shuffle_words_img(goose):
    shuffle(words)
    for duck in range(0,int(len(words)/3)):
        random_img(duck)
        print('Running', duck)





start = time.time()

for goose in range(0,1):
    shuffle_words_img(goose)

end = time.time()

print (end - start)

charcolisttxt = u""
for (i,j) in charcolist.items():
    charcolisttxt = charcolisttxt + i + str(j) + u"\n"

with codecs.open(os.path.join(path_for_save_resault,"charlist.txt") , "w" ,'utf-8') as output:
    output.write(charcolisttxt)
