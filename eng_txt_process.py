# Load LSTM network and generate text
import sys
import numpy
import re
import argparse
import codecs

parser = argparse.ArgumentParser()
parser.add_argument('input_txt', help='the path of input txt file')
#parser.add_argument('model', help = 'the trained model for prediction')
args = parser.parse_args()

# load ascii text and covert to lowercase
filename = args.input_txt
raw_text = open(filename).read().decode('utf-8').split(' ')

gen_txt = '\n'.join(i for i in raw_text)

#open: 'a', append
with codecs.open('/home/yingminc/Documents/y_g.txt', "w", 'utf-8') as output:
    output.write(gen_txt)
