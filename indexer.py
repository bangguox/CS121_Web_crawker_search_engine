
from collections import defaultdict
import math
import codecs
import os,json,pickle,shelve
class Indexer():
    def __init__(self):
        self.dict= defaultdict(list)
        self.dict_title=dict()
    def __tfidf(self,tf,df,size):
        if tf==0:
            return 0
        return round(((1 + math.log(float(tf)))*math.log((size/float(df)))), 1)
    def build_index(self,terms,filename,size,doc_freq,title_index):
        for token in title_index:
            token = token.split()
            self.dict_title[token[0]] = token[1]
        for token in terms:
            num=0
            token=token.split()
            t2=token[1].split(':')
            if token[0] in self.dict_title:
                values=self.dict_title[token[0]]
                values=values.split(':')
            if values[0]==t2[0]:
                num+=int(values[1])
            self.tfidf=self.__tfidf(t2[1],doc_freq[token[0]],size)
            #self.tfidf=math.pow(2,num)*self.tfidf
            self.dict[token[0]].append(t2[0]+":"+str(self.tfidf))
            #indexshelve.update(self.dict)
        #json.dump((dict(self.dict)), index_file)#save index as json file
        #index_file.write(str(dict(self.dict)))
        with codecs.open(filename, 'wb') as FILE:
            pickle.dump(self.dict, FILE, protocol=pickle.HIGHEST_PROTOCOL)


    def report(self,file_path,num_of_term,num_of_doc,index_file):
        self.report_file=codecs.open(file_path,'w+')
        self.answer="Conclusion:\nThe total number of unique terms is: %d\n"%(num_of_term)
        self.answer+="The total number of doc is: %d\n"%(num_of_doc)
        self.answer+= "The size for index file is: %d KB" %(os.path.getsize(index_file)/1024)
        self.report_file.write(self.answer)
        self.report_file.close()

source_path='FULLfile'
indexfile='cash/index.pickle'
reportfile='cash/report.txt'


indexer=Indexer()
num_of_doc=37496
num_of_term=420875
with codecs.open("cash/final_list.pickle",'rb') as D:
    final=pickle.load(D)
with codecs.open('cash/termspace.pickle','rb') as A:
    term_space=pickle.load(A)
with codecs.open('cash/doc_frequence.pickle','rb') as B:
    doc_freq=pickle.load(B)
with codecs.open('cash/final_title.pickle', 'rb') as C:
    title_index=pickle.load(C)
indexer.build_index(final,indexfile,num_of_doc,doc_freq,title_index)
indexer.report(reportfile,num_of_term,num_of_doc,indexfile)