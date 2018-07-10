from __future__ import division
from PIL import Image
from PIL import ImageDraw
import os
import numpy as np
import os
from skimage import img_as_ubyte
import cv2
import skimage
import fileinput
import sys
import time


def cv2pil(cvimg):
    return Image.fromarray(cvimg[:, :, ::-1].copy())

def draw_retangle(cvimg,(x_c,y_c,w,h),how='center'):
    if how=='center':
        #if given center of retangle and width and hight
        x = int(x_c-(w/2))
        y = int(y_c-(h/2))
        w = int(w)
        h = int(h)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    elif how == 'coordinate':
        # if given cordinate of 4 corners
        cv2.rectangle(img,(x_c,y_c),(w,h),(0,255,0),2)
    return img

def bound_cut(im, save=None):
    #cut off useless white frame
    img_p = im.copy()
    img_p = cv2.cvtColor(img_p, cv2.COLOR_RGB2GRAY)
    ret,thresh = cv2.threshold(img_p,127,255,cv2.THRESH_BINARY_INV)
    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    im = im[y:y+h, x:x+w]
    img=Image.fromarray(im)
    if save:
        img.save(savename)
    else:
        return img

def white2transparent(img, save=None):
    # PIL img as input
    # cuz cv2 is fk annoying with alpha
    im = img.convert("RGBA")
    datas = im.getdata()
    newdata = []
    for item in datas:
        if item[0] == 255 and item[1] ==255 and item[2] ==255: #white
            newdata.append((255,255,255,0)) #transparent
        else:
            newdata.append(item)
    im.putdata(newdata)
    if save:
        im.save(savename)
    else:
        return im
