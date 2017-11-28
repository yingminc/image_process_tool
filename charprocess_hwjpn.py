#encoding: utf-8
import cv2
import numpy as np
from PIL import Image
import os

JPNtest= '/home/ubuntu/Documents/alp_test'
JPNtest_r='/home/ubuntu/Documents/alp_test_r/' #destnation

allfolder = [filename for filename in os.listdir(JPNtest)]

allfile=[]
for folder in allfolder:
    for i in os.listdir(os.path.join(JPNtest,folder)):
        if i.split('.')[1] == 'png':
            allfile.append(i.split('.')[0])

#for folder in allfolder:
#    os.makedirs(os.path.join(JPNtest_r, folder))

for filename in allfile:

    print filename

    char, n1, n2, n3 = filename.split('_')
    #get contour
    img_o= cv2.imread(os.path.join(os.path.join(JPNtest,char),filename+'.png'))

    #get threshold

    img = img_o.copy()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret,thresh= cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((2,2), np.uint8)
    img_de= cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    img2,contours,heirarchy = cv2.findContours(img_de,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    h_o, w_o, c = img_o.shape



    #remove undesired contours
    noise=[]
    noise_size = (h_o * w_o) * 0.03
    for ind, i in enumerate(contours):

        print cv2.contourArea(i)
        if ((0 in i) or (h_o-1 in i) or (w_o-1 in i)) and (cv2.contourArea(i)<noise_size):
        #and (cv2.contourArea(i,True)<500):
            noise.append(ind)

    if (noise == None) or (len(noise) == len(contours)) :
        cnt = contours
    else:
        cnt = np.delete(contours, noise,0)

    #cv2.drawContours(img_o,cnt,-1,(0,255,0),3)

    #point=[]
    #for i in contours:
    #    point.append((i[0][0][0], i[0][0][1]))
    #for ind, i in enumerate(point):
    #    cv2.putText(img_o, str(ind), i, cv2.FONT_HERSHEY_PLAIN,1,(255,0,0))



    xall=[]
    yall=[]
    for i in cnt:
        for j in i:
            xall.append(j[0][0])
            yall.append(j[0][1])

    x = min(xall)-1
    w = max(xall)-min(xall)+1
    y = min(yall)-1
    h = max(yall)-min(yall)+1

    if y < 0:
        y = 0

    if x < 0:
        x=0

    print (x, y, w, h)

    img_c = img_o[y:y+h, x:x+w]

    img_c = cv2.cvtColor(img_c, cv2.COLOR_RGB2GRAY)
    ret,img_c= cv2.threshold(img_c,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    #ret,img_c= cv2.threshold(img_c,220,255,cv2.THRESH_BINARY)

    img_p = Image.fromarray(img_c)


    imgp = img_p.convert("RGBA")
    datas = imgp.getdata()
    newdata = []
    for item in datas:
        if item[0] == 255 and item[1] ==255 and item[2] ==255: #white
            newdata.append((255,255,255,0)) #transparent
        else:
            newdata.append(item)
    imgp.putdata(newdata)

    imgp.save(os.path.join(os.path.join(JPNtest_r, char),filename+'_r.png'))
