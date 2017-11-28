from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import cv2
import sys
import skimage
#from builtins import bytes,chr

font = ImageFont.truetype('/home/yingminc/Documents/notofonts/NotoSansCJKjp-hinted/NotoSansCJKjp-DemiLight.otf',20)

def draw_retangles(filename):
    img = cv2.imread('/home/yingminc/Documents/JPN_test_img/%s.png' %(filename))


    text_file = open('/home/yingminc/Documents/JPN_test_img/%s.txt' %(filename), "r")
    lines = text_file.read().split('\n')

    txtlist = []
    for i in lines:
        txtlist.append(i.split(' '))

    

    for i in txtlist:
        x_c = float(i[1])
        y_c = float(i[2])
        w = float(i[3])
        h = float(i[4])

        x = int(x_c-(w/2))
        y = int(y_c-(h/2))
        w = int(w)
        h = int(h)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    img = img[:, :, ::-1].copy()
    img=Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    for i in txtlist:
        x = int(float(i[1])-(float(i[3])/2))
        y = int(float(i[2])-(float(i[4])/2))

        name = i[0]
        name = name.decode('utf-8')




        draw.text((x, y-30),name,(255,0,0),font=font)
        img.save('/home/yingminc/Documents/JPN_test_img_tag/%s_r.png'%(filename))

for filename in range (0,50):
    filename = '{:07d}'.format(filename)
    print filename
    draw_retangles(filename)
