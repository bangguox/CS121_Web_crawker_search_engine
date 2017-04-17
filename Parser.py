from nltk import *
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re
import os.path
import codecs,pickle
import io,json,glob

class MyParser():
    def Parseuseful(self,path):
        trash_list = ['39/373']
        filedump = path
        h1=''
        h2=''
        h3=''
        title=''
        finallist_title = []
        doc_freq = dict()
        filedump = filedump + "/**[0-9]/**[0-9]"
        for filename in glob.iglob(filedump, recursive=True):
            docid = filename[len(path) + 1:]
            if docid not in trash_list:
                print(docid)
                with codecs.open(filename, 'r', 'UTF-8') as source:
                    source = source.read()
                    soup = BeautifulSoup(source, 'html.parser')
                    if soup.title !=None :
                        title=soup.title.text
                    if soup.h1 != None:
                        h1=soup.h1.text
                    if soup.h2 != None:
                        h2=soup.h2.text
                    if soup.h3 !=None:
                        h3=soup.h3.text
                    text=h1+','+h2+','+h3+','+title
                    tokenizer = RegexpTokenizer(r'[a-z]+|\d+')
                    token_text = tokenizer.tokenize(text)
                    token_word = [w.lower() for w in token_text if not w in stopwords.words('english')]
                    freq_text = dict()
                    for w in token_word:
                        if w in freq_text:
                            freq_text[w] += 1
                        else:
                            freq_text[w] = 1
                            if w in doc_freq:
                                doc_freq[w] += 1
                            else:
                                doc_freq[w] = 1
                    for x, y in freq_text.items():
                        target = x + ' ' + str(docid) + ':' + str(y)
                        finallist_title.append(target)
        with codecs.open('cash/final_title.pickle', 'wb') as q :
            pickle.dump(finallist_title, q, protocol=pickle.HIGHEST_PROTOCOL)

    def Parsefile(self,path):
        num_of_document=0
        doc_freq=dict()
        term_space=set()
        finallist=[]
        doc_url=dict()
        trash_list=['39/373'] #element that don't need to visit
        #if not os.path.exists("index"):
        if 1:
            #os.mkdir("index")
            list_of_document = []
            #current = os.getcwd()
            filedump = path
            filedump = filedump+"/**[0-9]/**[0-9]"
            url_file=path+'/'+'bookkeeping.json'
            url_file=json.load(open(url_file))
            url_data=dict(url_file.items()) #dict hold all value about docid and url
            for filename in glob.iglob(filedump, recursive=True):
                list_of_document.append(filename)
                docid = filename[len(path)+1:]
                if docid not in trash_list:
                    print(docid)
                    with codecs.open(filename, 'r', 'UTF-8') as source:
                        source = source.read()
                        soup = BeautifulSoup(source, 'html.parser')
                        title=''
                        h1=''
                        h2=''
                        h3=''
                        if soup.title != None:
                            title = soup.title.text
                        if soup.h1 != None:
                            h1 = soup.h1.text
                        if soup.h2 != None:
                            h2 = soup.h2.text
                        if soup.h3 != None:
                            h3 = soup.h3.text
                        text = soup.text+title+h1+h2+h3
                        tokenizer = RegexpTokenizer(r'[a-z]+|\d+')
                        token_text = tokenizer.tokenize(text)
                        token_word = [w.lower() for w in token_text if not w in stopwords.words('english')]
                        for word in token_word:
                            term_space.add(word)
                        freq_text = dict()
                        for w in token_word:
                            if w in freq_text:
                                freq_text[w] += 1
                            else:
                                freq_text[w] = 1
                                if w in doc_freq:
                                    doc_freq[w] += 1
                                else:
                                    doc_freq[w] = 1
                        for x, y in freq_text.items():
                            target = x + ' ' + str(docid) + ':' + str(y)
                            finallist.append(target)

            num_of_document=len(list_of_document) #give the value of number of document
            with codecs.open('cash/lisdoc.pickle','wb') as f:
                pickle.dump(list_of_document, f, protocol=pickle.HIGHEST_PROTOCOL)
            with codecs.open('cash/termspace.pickle','wb') as A:
                pickle.dump(term_space, A, protocol=pickle.HIGHEST_PROTOCOL)
            with codecs.open('cash/doc_frequence.pickle','wb') as B:
                pickle.dump(doc_freq, B, protocol=pickle.HIGHEST_PROTOCOL)
            with codecs.open("cash/doc_url.pickle",'wb') as C:
                pickle.dump(url_data, C, protocol=pickle.HIGHEST_PROTOCOL)
            with codecs.open("cash/final_list.pickle",'wb') as D:
                pickle.dump(finallist, D, protocol=pickle.HIGHEST_PROTOCOL)
            print(num_of_document)
            print(len(term_space))
        #Data=(num_of_document,len(term_space))# return tuple contain number of document and number of unique terms
        #return Data
parse=MyParser()
parse.Parsefile("FULLfile")
parse.Parseuseful("FULLfile")