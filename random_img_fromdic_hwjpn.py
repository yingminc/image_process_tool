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

#TODO: change from absolute path to relative path
txtimg_folder="/home/ubuntu/Documents/JPN_test_r"
file_of_dict='/home/ubuntu/Documents/ipadict/merge2.csv'
path_for_save_resault="/home/ubuntu/Documents/JPN_test_r_img"
background_path = '/home/ubuntu/Documents/back'

#make a list of all char
charalist = os.listdir(txtimg_folder)

charlist = list(set(charalist))

charlist = [g.decode('utf-8') for g in charlist]

#make a dir for counting the uses of chars
charcolist={}
for g in charlist:
    charcolist[g] = 0


#load the background
allback = [back for back in os.listdir(background_path)if 'png' in back]

#make a list of dictionary vocabuary
with open(file_of_dict, 'rb',) as words:
    words = csv.reader(words, delimiter=',', quotechar='|',encoding='utf-8')
    wordslist=list(words)
words = []
for i in range (0,len(wordslist)):
    words.append(wordslist[i][0])



def random_img(duck):


    #select target word
    u = words[(duck)*3]
    #2
    u2 =words[(duck)*3+1]

    #3
    u3 = words[(duck)*3+2]


    #list char for target words
    dictwords = []
    for i, c in enumerate(u):
        dictwords.append(c)


    #return if the char is not in dataset
    for i in dictwords:
        if i not in charlist:
            return

    size = len(dictwords)

    #2
    dictwords2 = []

    for i, c in enumerate(u2):
        dictwords2.append(c)

    for i in dictwords2:
        if i not in charlist:
            return

    size2 = len(dictwords2)

    #3
    dictwords3 = []

    for i, c in enumerate(u3):
        dictwords3.append(c)

    for i in dictwords3:
        if i not in charlist:
            return

    size3 = len(dictwords3)




    #get img file
    ims = []

    for ind, i in enumerate(dictwords):
        charfolder = os.listdir(os.path.join(txtimg_folder,i))
        target_img = np.random.choice(charfolder, 1)
        im_folder = os.path.join(txtimg_folder,i)
        im = Image.open(os.path.join(im_folder,target_img[0]))
        ims.append(im)

    if ims == []:
        return

    #2
    ims2 = []

    for ind, i in enumerate(dictwords2):
        charfolder = os.listdir(os.path.join(txtimg_folder,i))
        target_img = np.random.choice(charfolder, 1)
        im_folder = os.path.join(txtimg_folder,i)
        im = Image.open(os.path.join(im_folder,target_img[0]))

        ims2.append(im)

    if ims2 == []:
        return

    #3
    ims3 = []

    for ind, i in enumerate(dictwords3):
        charfolder = os.listdir(os.path.join(txtimg_folder,i))
        target_img = np.random.choice(charfolder, 1)
        im_folder = os.path.join(txtimg_folder,i)
        im = Image.open(os.path.join(im_folder,target_img[0]))

        ims3.append(im)

    if ims3 == []:
        return

    #get size info of imgs
    widths, heights = zip(*(i.size for i in ims))
    total_width = sum(widths)
    max_height = max(heights)

    #2
    widths2, heights2 = zip(*(i.size for i in ims2))
    total_width2 = sum(widths2)
    max_height2 = max(heights2)

    #3
    widths3, heights3 = zip(*(i.size for i in ims3))
    total_width3 = sum(widths3)
    max_height3 = max(heights3)

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

    #2
    m2 = np.random.uniform(-0.3,0.3)
    n2 = np.random.uniform(-0.3,0.3)
    if abs(m2)>abs(n2):
        n2 = 0
    else:
        m2=0

    #3
    m3 = np.random.uniform(-0.3,0.3)
    n3 = np.random.uniform(-0.3,0.3)
    if abs(m3)>abs(n3):
        n3 = 0
    else:
        m3=0


    #resize rate

    max_total_width = max(total_width, total_width2, total_width3)
    max_max_height = max(max_height, max_height2, max_height3)


    if (max_total_width+20*size) > (max_max_height+10):
        rate = np.random.uniform(0.4,(500/(max_total_width+20*size)))
    else:
        rate = np.random.uniform(0.4,(500/(max_max_height+10)))


    if rate>1:
        rate=1

    #avoid extrame size error
    if rate*min(heights + heights2 + heights3)<1 :
        return
    elif rate*min(total_width , total_width2 , total_width3) <1:
        return
    if (max(total_width+20*size , total_width2+20*size2 , total_width3+20*size3))*rate >= 500:
        return
    elif (((max_height + max_height2 + max_height3)+30) *rate) >= 500:
        return
    elif 500- (((max_height + max_height2 + max_height3)+30) *rate)<((max_height3+10)*rate):
        return




    #random position
    x_p = np.random.randint(0,500-((total_width+15*size)*rate))
    y_p = np.random.randint(0, 500- (((max_height + max_height2 + max_height3)*rate)+30))

    x_p2 = np.random.randint(0,500-((total_width2+15*size2)*rate))
    y_p2 = y_p

    x_p3 = np.random.randint(0,500-((total_width3+15*size3)*rate))
    y_p3 = y_p


    #combine image
    txt = []
    h1 = []
    x_offset = 0

    for ind, i in enumerate(ims):

        #affine
        orin_w, orin_h = i.size
        new_w = orin_w + int(abs(orin_h*m))
        new_h = orin_h + int(abs(orin_w*n))
        i = i.transform((new_w,new_h),Image.AFFINE,(1,-m,
            int(orin_h*m) if m<0 else 0,
            -n, 1, int(orin_w*n)if n<0 else 0), Image.BILINEAR)


        #rotate
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

        #resize
        i=i.resize((int(w*rate),int(h*rate)),Image.BILINEAR)

        w, h = i.size


        canvas.paste(i, ((x_offset+x_p), (y_b-y_p)), i)

        #str(x,y,w,h)
        i_x = str(x_offset +x_p + (w/2))
        i_y = str(y_b- y_p+(h/2))
        i_w = str(w)
        i_h = str(h)

        #creat txt info
        txt.append((dictwords[ind]+" "+i_x+" "+i_y+" "+i_w+" "+i_h))

        #count the use of char
        charcolist[dictwords[ind]] +=1




    #2
    txt2 = []
    x_offset2 = 0


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


    #make txt file
    txt = txt + txt2 +txt3
    txt = "\n".join(i for i in txt)

    if len(str(duck))<7:
        name = '0'*(7-len(str(duck))) + str(duck)
    else:
        name = str(duck)
    with codecs.open(os.path.join(path_for_save_resault,"%s.txt" %(name)), "w" ,'utf-8') as output:
        output.write(txt)

    #save combined img
    canvas.save(os.path.join(path_for_save_resault,"%s.png" %(name)))


#define the shuffle
def shuffle_words_img(goose):
    shuffle(words)
    for duck in range(0,int(len(words)/3)):
        random_img(duck)
        print('Running', duck)




#real loop
start = time.time()

for goose in range(0,1):
    shuffle_words_img(goose)

end = time.time()

print (end - start)

#save the dictionary for counting
charcolisttxt = u""
for (i,j) in charcolist.items():
    charcolisttxt = charcolisttxt + i + str(j) + u"\n"

with codecs.open(os.path.join(path_for_save_resault,"charlist.txt") , "w" ,'utf-8') as output:
    output.write(charcolisttxt)
