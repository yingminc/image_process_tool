from PIL import Image
import random, os, glob
import numpy as np

orin_path = '../../data/generate_sentences/original_bg'
save_path = '../../data/generate_sentences/background_images'

allback = [back for back in os.listdir(orin_path) if ('jpg' in back) or ('png' in back) or ('jpeg' in back) or ('JPG' in back) or ('JPEG' in back)]


for ind, back in enumerate(allback):
    backim = Image.open(os.path.join(orin_path,back))
    backname,ext = back.split('.')
    print (backname)
    backim = backim.resize((500,500), Image.NEAREST)
    backim.save(os.path.join(save_path,'back_'+str(ind)+'.png'))
