from tkinter import *
import sys
import Judge
class graphics():
    def __init__(self):
        self.query=''
        self._if_click=False
        self.root=Tk()
        self.root.geometry("470x200")
        frame1=Frame(self.root)
        frame2 = Frame(self.root)
        frame1.grid(row=7,column=0,padx=10,pady=10,sticky=W+E)
        frame2.grid(row=8, column=1, padx=10, pady=10, sticky=W + E)
        label1=Button(frame1,text="search",command=self._search_button)
        label2=Button(frame1,text='quit',command=self._quit_button)
        label3=Label(self.root,text="Cool Kid Search",font = ('Helvetica', 34))
        self.entry1=Entry(self.root,width=30)
        label4=Label(frame2,text="Done by Alan Xie")
        label1.grid(row=0,column=0,padx = 10, pady = 10,sticky=W)
        label2.grid(row=0,column=1,padx = 10, pady = 10,sticky=W)
        label3.grid(row=1)
        label4.grid(row=5,column=0,padx = 10, pady = 10,sticky=E)
        self.entry1.grid(row=5,columnspan=10,padx=10,pady=2,sticky=W+E)
    def start(self):
        self.root.mainloop()
    def work(self):
        if self._if_click==True:
            self.query=self.entry1.get().lower()
            Score = Judge.judge()
            Score.DOC_MAG()
            text=Score.Get_result(self.query)
            if text==None:
                show_final("NO result can be found for :"+ self.query)
            else:
                result=''
                k=1
                for i in text:
                    result+=str(k)+':'+"http://"+i+'\n'+"\n"
                    k+=1
                print(result)
                show_final(result)


    def _search_button(self):
        self._if_click=True
        self.work()
    def _quit_button(self):
        sys.exit(0)
class show_final:
    def __init__(self,text):
        self.window=Tk()
        self.result=Text(self.window)
        self.result.insert(INSERT,text)
        self.result.pack()
        self.window.mainloop()
win=graphics().start()
#show_final("hahahahahahhah")