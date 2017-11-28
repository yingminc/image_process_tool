#encoding: utf-8
from gensim.corpora import WikiCorpus
import codecs
import os

path_for_save_resault = '/home/ubuntu/Documents/hw_background_gene/'

wiki_jpn = WikiCorpus('/home/ubuntu/Documents/hw_background_gene/jawiki-latest-pages-articles.xml.bz2')

with codecs.open(os.path.join(path_for_save_resault,"wiki_jpn.txt") , "w" ,'utf-8') as output:
    for i in wiki_jpn.get_texts():
        output.write('\n'.join(i).decode('utf-8'))
