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
#from builtins import bytes,chr
import time
import codecs
from random import shuffle
import argparse

# Make directory if not found
def make_directory(path):
    if not os.path.isdir(path):
        os.makedirs(path)

# Print iterations progress
def _printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    u"""
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr       = "{0:." + str(decimals) + "f}"
    percents        = formatStr.format(100 * (iteration / float(total)))
    filledLength    = int(round(barLength * iteration / float(total)))
    bar             = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\x1b[2K\r')
    sys.stdout.flush()

# Format time to h, m, s
def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)


#mode = "training/"
mode = "wiki_with_fonts/"

extracted_characters_folder = "../../data/character_extraction/fonts_processed/"
#file_of_dict = 'wiki_jpn.txt'
path_for_save_result = "../../data/generate_sentences/" + mode
background_path = '../../data/generate_sentences/background_jpg/'

make_directory(path_for_save_result+"Images/")
make_directory(path_for_save_result+"Annotations/")

#set argument
parser =argparse.ArgumentParser()
parser.add_argument('input_dict', help = 'the file of input dictionary')
parser.add_argument('image_num',help = 'number of image to generate', type=int)
parser.add_argument('-ln','--line_num',help = 'number of line in one image; at least 3', type=int, default = 6)
#parser.add_argument('-r', '--rate',help = 'the resize rate', type=float, default = 1)
parser.add_argument('--font', help = 'switch to font mode', action = 'store_true')
parser.add_argument('-sh','--shuffle', help = 'shuffle the input_dict', action = 'store_true')
args = parser.parse_args()


#make a list of all char
print("Making list of characters...")
charalist = os.listdir(extracted_characters_folder)

charlist = list(set(charalist))

charlist = [g.decode('utf-8') for g in charlist]

#make a dir for counting the uses of chars
charcolist={}
for g in charlist:
    charcolist[g] = 0


#load the background
print("Loading background images...")
allback = [back for back in os.listdir(background_path) if 'jpg' in back]

#make a list of dictionary vocabuary
print("Loading dictionary file...")
if args.input_dict.split('.')[-1] == 'csv':
    input_format = 'csv'

    with open(args.input_dict, 'rb',) as words:
        words = csv.reader(words, delimiter=',', quotechar='|',encoding='utf-8')
        wordslist=list(words)
    print('Making list of words to use...')
    words = []
    for i in range (0,len(wordslist)):
        words.append(wordslist[i][0])
    print('Total number of words {}'.format(len(wordslist)))

elif args.input_dict.split('.')[-1] == 'txt':
    input_format = 'txt'

    text_file = open(args.input_dict, "r")
    wordslist = text_file.read().split('\n')
    print('Making list of words to use...')
    words = list(set(wordslist))
    print('Total number of words {}'.format(len(wordslist)))

if args.shuffle:
    shuffle(words)

#make a font list
if args.font:
    fontlist = []
    allimgs = []
    for char in os.listdir(extracted_characters_folder):
        charimg = os.listdir(os.path.join(extracted_characters_folder,char))
        allimgs.extend(charimg)
    for img in allimgs:
        n1, n2, fontex = img.split('_')
        font, ex = fontex.split('.')
        fontlist.append(font)
    fontlist = list(set(fontlist))



wordline = 0
sum_height = 0

def random_img(duck):
    global wordline
    #background
    backg = random.choice(allback)
    canvas = Image.open(os.path.join(background_path,backg))
    eggw = np.random.randint(2,args.line_num)

    if args.font:
        targetfont = np.random.choice(fontlist, 1)
        targetfontname = targetfont[0]


    #rate = args.rate
    rate = np.random.random() + 0.3

    wordline += eggw

    if wordline > len(words)-1:
        wordline = 0
        if args.shuffle:
            shuffle(words)
    line_offset = wordline - eggw

    txt = []
    #FIXME breaks when rate is too big
    y_p = np.random.randint(0, 500-(eggw*rate*50))
    global sum_height
    sum_height = 0


    def txt_processing(yolk):

        #select target word
        if input_format == 'txt':
            u = words[line_offset+yolk].decode('utf-8') #.upper()
        elif input_format == 'csv':
            u = words[line_offset+yolk]

        #list char for target words
        dictwords = []
        for i, c in enumerate(u):
            dictwords.append(c)

        #return if the char is not in dataset
        for i in dictwords:
            if i ==
            if i not in charlist:
                print(u'couldnt find {}'.format(i))
                return

        size = len(dictwords)

        ims = []

        for ind, i in enumerate(dictwords):
            if i == ' ':
                im_folder = os.path.join(extracted_characters_folder,'space')
            else:
                im_folder = os.path.join(extracted_characters_folder,i)

            charfolder = os.listdir(im_folder)

            if args.font:
                #chose the file with targetfont name in its name
                target_img = [ j for j in charfolder if targetfont in j]
            else:
                target_img = np.random.choice(charfolder, 1)

            im = Image.open(os.path.join(im_folder,target_img[0]))
            ims.append(im)

        if ims == []:
            return

        #get size info of imgs
        widths, heights = zip(*(i.size for i in ims))
        total_width = sum(widths)
        max_height = max(heights)+10
        global sum_height
        sum_height += max_height*rate

        #avoid extrame size error
        if (total_width*rate + 10) > 500:
            return

        #random position
        if 500-100-((total_width)*rate)<1:
            x_p = 0
        else:
            x_p = np.random.randint(0,500-100-((total_width)*rate))
        #y_p_max = max_height*6
        #y_p = np.random.randint(0, 500- (((y_p_max)*rate)+10))

        #combine image
        if x_p-10<0:
            x_offset= 0
        else:
            x_offset = x_p -10


        for ind, i in enumerate(ims):

            w, h = i.size

            #adjust position
            if ind > 0:
                previous = ims[ind - 1]
                wp, hp = previous.size
                if wp < (0.2*max(widths)):
                    x_offset += int(wp*rate)
                else:
                    x_offset += int(max(widths)*rate)
            else:
                x_offset += 2



            if h<(0.2*max(heights)):
                y_b = 500 - int(sum_height - (max_height*0.4*rate) + y_p)
            else:
                y_b = 500 - int(sum_height + y_p)

            #resize
            new_w = int(w*rate)
            if new_w == 0:
                new_w = 1

            new_h = int(h*rate)
            if new_h == 0:

                new_h = 1


            i=i.resize((new_w, new_h),Image.BILINEAR)

            w, h = i.size


            canvas.paste(i, ((x_offset), (y_b)), i)

            #str(x,y,w,h)
            if (x_offset + w) >500:
                w = 500 - x_offset
            i_x = str(x_offset + (w/2))
            if (y_b) < 0:
                h = h + y_b
            i_y = str(y_b+(h/2))
            i_w = str(w)
            i_h = str(h)

            #creat txt info
            if (dictwords[ind] != ' ') and ((x_offset+w) < 500) and (y_b > 0):
                txt.append((dictwords[ind]+" "+i_x+" "+i_y+" "+i_w+" "+i_h))

            #count the use of char
            if dictwords[ind] == ' ':
                charcolist['space'] +=1
            else:
                charcolist[dictwords[ind]] +=1


    #run the loop to paste lines on background
    for yolk in range (0, eggw):
        txt_processing(yolk)

    if txt == []:
        return

    txt = "\n".join(i for i in txt)

    if len(str(duck))<7:
        name = '0'*(7-len(str(duck))) + str(duck)
    else:
        name = str(duck)
    with codecs.open(os.path.join(path_for_save_result,"Annotations/%s.txt" %(name)), "w" ,'utf-8') as output:
        output.write(txt)

    #save combined img
    canvas.save(os.path.join(path_for_save_result,"Images/%s.png" %(name)))

total_generate = args.image_num
initial_time = time.time()

for duck in range (0,args.image_num-1):
    elapsed_time = (time.time() - initial_time)
    remaining_time = int(elapsed_time * (total_generate - duck) / (duck+1))
    random_img(duck)
    _printProgress(duck+1, total_generate,
        prefix = 'Generating ({}/{})'.format(duck+1, total_generate),
        suffix = 'elapsed '+format_time(elapsed_time)+', remaining '+format_time(remaining_time),
        barLength = 30, decimals = 2)

#save the dictionary for counting
print()
print('Saving character count list...')
charcolisttxt = u""
for (i,j) in charcolist.items():
    charcolisttxt = charcolisttxt + i + ' '+ str(j) + u"\n"

with codecs.open(os.path.join(path_for_save_result,"charlist.txt") , "w" ,'utf-8') as output:
    output.write(charcolisttxt)
