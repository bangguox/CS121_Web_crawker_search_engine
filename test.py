from bs4 import BeautifulSoup
import re,pickle
import os.path
import codecs,glob
from nltk import *
'''
test_html=codecs.open('FULLfile/3/382','r','UTF-8')
test_html=test_html.read()
soup=BeautifulSoup(test_html,'html.parser')
tokenizer = RegexpTokenizer('[^\w.]+',gaps=True)
tokenizer = RegexpTokenizer(r'[a-z]+|\d+')
#token_text=tokenizer.tokenize(soup.title)
print(soup.h2)'''
#str='44\\199'
final=[]
dic={}
with codecs.open("cash/.pickle",'rb') as D:
    final=pickle.load(D)


print( final)