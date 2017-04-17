from collections import defaultdict, OrderedDict
import os, ast, math,codecs,json,pickle,shelve

class judge():
    def __init__(self):

        self.size=37496
        self.term_space=list()
        self.index=dict()
        self.myShelve=dict()
        self.doc_freqs=dict()
        self.doc_urls=dict()
        with codecs.open("cash/index.pickle", "rb") as A:
            self.index = pickle.load(A)
        with codecs.open("cash/termspace.pickle", "rb") as B:
            self.term_space = pickle.load(B)

        with codecs.open("cash/doc_frequence.pickle", "rb") as C:
            self.doc_freqs=pickle.load(C)
        with codecs.open("cash/doc_url.pickle", "rb") as D:
            self.doc_urls=pickle.load(D)

    def DOC_MAG(self):
        if os.path.exists('cash/MAG.pickle'):
            with codecs.open("cash/MAG.pickle", 'rb') as D:
                self.myShelve = pickle.load(D)
        else:
            for term in self.term_space:
                for item in self.index[term]:
                    docId_freq = item.split(":")
                    if docId_freq[0] in self.myShelve:
                        self.myShelve[docId_freq[0]] += math.pow(float(docId_freq[1]), 2)
                    else:
                        self.myShelve[docId_freq[0]] = math.pow(float(docId_freq[1]), 2)
            for k, v in self.myShelve.items():
                self.myShelve[k] = math.sqrt(v)
            with codecs.open('cash/MAG.pickle', 'wb') as x:
                pickle.dump(self.myShelve, x, protocol=pickle.HIGHEST_PROTOCOL)
    def process_query(self,query):
        query_list = query
        query_tfs = dict()
        for term in query_list:
            if term in self.term_space:
                if term in query_tfs:
                    query_tfs[term] += 1
                else:
                    query_tfs[term] = 1
            else:
                if term not in query_tfs:
                    query_tfs[term] = float(0)
        for t, f in query_tfs.items():
            if f != float(0):
                query_tfs[t] = self.__tfidf(f, self.doc_freqs[t])

        return query_tfs

    def get_sim_score(self,query_tfs):
        Similar = dict()
        query_mag = self.Query_Mag(query_tfs)
        #print(query_mag)
        for t, f in query_tfs.items():
            if t in self.term_space:
                for token in self.index[t]:
                    token = token.split(":")
                    # print(token)
                    if token[0] in Similar:
                        Similar[token[0]] += float(f * float(token[1]))
                    else:
                        Similar[token[0]] = float(f * float(token[1]))
        #print(Similar)
        for d, f in Similar.items():
            Similar[d] = Similar[d] / (query_mag * self.myShelve[d])
        #print(Similar)
        return Similar

    def Get_result(self, query):
        query_tfs=self.process_query(query.split())
        print(query_tfs)
        sorted_by_value = OrderedDict(sorted(self.get_sim_score(query_tfs).items(), key=lambda x: x[1], reverse=True))
        i = 0
        url_list = []
        for k, v in sorted_by_value.items():
            if (i == 5):
                return url_list
            else:
                thestr=k.split("\\")
                x=str(thestr[0])+"/"+str(thestr[1])
                url_list.append(self.doc_urls[x])
                i += 1
        #return url_list

    def __tfidf(self, termFreq, docFreq):
        return round(((1 + math.log(float(termFreq))) * math.log((self.size / float(docFreq)))), 1)

    def Query_Mag(self, query_tfs):
        squaresum = 0
        for t, f in query_tfs.items():
            if f:
                squaresum += math.pow(float(f), 2)
        squaresum=math.sqrt(squaresum)
        return squaresum


