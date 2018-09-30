#App

import os
from tkinter import *
from time import sleep
from requests import post
from threading import Thread
from PIL import ImageTk,Image
from api.speech_client import SpeechClient
from backend import update_json,nlp,genWordCloud,getTags

def cleanup():
    for i in os.listdir('temp'):
        os.remove('temp/'+i)

def update(app,client,running):
    flag=1
    while 1:
        if not running():
            break
        if app.record or flag:
            t=Thread(target=update_json,args=(client,))
            t.start()
            flag=0
            sleep(10)

class GUI:

    def __init__(self,root):
        self.match=[]
        self.matchData=[]
        self.iconBtns=[None,None,None,None]
        self.iconImgs=[[ImageTk.PhotoImage(Image.open('imgs/Record_Inactive.jpg').resize((64,64),Image.ANTIALIAS)),
                        ImageTk.PhotoImage(Image.open('imgs/Record_Active.jpg').resize((64,64),Image.ANTIALIAS))],
                       [ImageTk.PhotoImage(Image.open('imgs/Img_Inactive.jpg').resize((64,64),Image.ANTIALIAS)),
                        ImageTk.PhotoImage(Image.open('imgs/Img_Active.jpg').resize((64,64),Image.ANTIALIAS))],
                       [ImageTk.PhotoImage(Image.open('imgs/Explore_Inactive.jpg').resize((64,64),Image.ANTIALIAS)),
                        ImageTk.PhotoImage(Image.open('imgs/Explore_Active.jpg').resize((64,64),Image.ANTIALIAS))],
                       [ImageTk.PhotoImage(Image.open('imgs/Me_Inactive.jpg').resize((64,64),Image.ANTIALIAS)),
                        ImageTk.PhotoImage(Image.open('imgs/Me_Active.jpg').resize((64,64),Image.ANTIALIAS))]]
        self.root=root
        self.generateBtnImgs=[ImageTk.PhotoImage(Image.open('imgs/Generate.jpg')),
                              ImageTk.PhotoImage(Image.open('imgs/Generate_Hover.jpg'))]
        self.imgs=[ImageTk.PhotoImage(Image.open('imgs/Round_Btn_Inactive.jpg')),
                   ImageTk.PhotoImage(Image.open('imgs/Round_Btn_Inactive_Hover.jpg')),
                   ImageTk.PhotoImage(Image.open('imgs/Round_Btn_Active.jpg')),
                   ImageTk.PhotoImage(Image.open('imgs/Round_Btn_Active_Hover.jpg'))]
        root.title('Cloudify Client')
        root.attributes("-fullscreen",True)
        root.geometry(('%dx%d')%(root.winfo_screenwidth(),root.winfo_screenheight()))
        root.configure(background='black')
        root.resizable(width=True,height=True)
        self.frame=Frame(root,bg='#F3F3F3',width=int(root.winfo_screenheight()/1334*750),height=root.winfo_screenheight()) #iPhone 6 Resolution
        root.grid_columnconfigure(1,weight=1)
        self.frame.grid(column=1)
        self.frame.grid_propagate(0)
        self.frames=[Frame(self.frame,bg='#F3F3F3',width=int(root.winfo_screenheight()/1334*750),height=root.winfo_screenheight()*0.81),
                     Frame(self.frame,bg='#F3F3F3',width=int(root.winfo_screenheight()/1334*750),height=root.winfo_screenheight()*0.81),
                     Frame(self.frame,bg='#F3F3F3',width=int(root.winfo_screenheight()/1334*750),height=root.winfo_screenheight()*0.81),
                     Frame(self.frame,bg='#F3F3F3',width=int(root.winfo_screenheight()/1334*750),height=root.winfo_screenheight()*0.81)]
        for i in range(len(self.frames)):
            self.frames[i].grid_propagate(0)
        self.topFrame=Frame(self.frame,bg='#E2E2E2',width=int(root.winfo_screenheight()/1334*750),height=root.winfo_screenheight()*0.08)
        self.topFrame.grid(row=0,sticky='N')
        self.topFrame.grid_propagate(0)
        self.topFrame.grid_rowconfigure(1,weight=1)
        self.topFrame.grid_columnconfigure(1,weight=1)
        self.topLabel=Label(self.topFrame,text='Cloudify',bg='#E2E2E2',fg='#777777',font=('Courier',30))
        self.topLabel.grid(row=1,column=1)
        self.mainFrame=self.frames[0]
        self.mainFrame.grid(row=1,sticky='N')
        self.downFrame=Frame(self.frame,bg='#E2E2E2',width=int(root.winfo_screenheight()/1334*750),height=root.winfo_screenheight()*0.11)
        self.downFrame.grid(row=2,sticky='S')
        self.downFrame.grid_propagate(0)
        for i in range(0,len(self.imgs)):
            tempImg=self.iconImgs[i][0]
            self.iconBtns[i]=Label(self.downFrame,image=tempImg)
            self.iconBtns[i].photo=tempImg
            self.iconBtns[i].grid(row=0,column=i)
            self.iconBtns[i]['borderwidth']=0
            if i==0:
                self.iconBtns[i].bind('<Button-1>',lambda event:self.select(0))
            elif i==1:
                self.iconBtns[i].bind('<Button-1>',lambda event:self.select(1))
            elif i==2:
                self.iconBtns[i].bind('<Button-1>',lambda event:self.select(2))
            elif i==3:
                self.iconBtns[i].bind('<Button-1>',lambda event:self.select(3))
            self.downFrame.grid_columnconfigure(i,weight=1)
        self.select(0)
        self.frame.grid_rowconfigure(0,weight=1)
        self.frame.grid_rowconfigure(1,weight=1)
        self.record=False
        self.on_btn=Label(self.mainFrame,image=self.imgs[self.record*2])
        self.on_btn.photo=self.imgs[self.record*2]
        self.on_btn['borderwidth']=0
        self.on_btn.grid(row=1,column=1)
        self.on_btn.bind('<Enter>',self.btn_enter)
        self.on_btn.bind('<Leave>',self.btn_exit)
        self.on_btn.bind('<Button-1>',self.btn_click)
        self.mainFrame.grid_rowconfigure(1,weight=1)
        self.mainFrame.grid_columnconfigure(1,weight=1)
        self.frames[0]=self.mainFrame
        self.exportBtn=Label(self.frames[1],image=self.generateBtnImgs[0])
        self.exportBtn['borderwidth']=0
        self.exportBtn.bind('<Enter>',self.gen_btn_enter)
        self.exportBtn.bind('<Leave>',self.gen_btn_exit)
        self.exportBtn.bind('<Button-1>',self.gen_cloud)
        self.exportBtn.grid(row=1,column=1)
        self.frames[1].grid_rowconfigure(1,weight=1)
        self.frames[1].grid_columnconfigure(1,weight=1)
        self.loginFrame=Frame(self.frames[3],width=int(root.winfo_screenheight()/1334*750),height=300,bg='#F3F3F3')
        self.loginFrame.grid(row=1,column=1)
        self.loginFrame.grid_propagate(0)
        self.loginLabel=Label(self.loginFrame,text='Upload',bg='#F3F3F3',fg='#777777',font=('Courier',40))
        self.loginLabel.grid(row=0,column=1)
        self.nameEntry=Entry(self.loginFrame,borderwidth=0,bg='#F3F3F3',width=int(root.winfo_screenheight()/1334*750),
                             highlightthickness=5,highlightbackground='#777')
        self.idEntry=Entry(self.loginFrame,borderwidth=0,bg='#F3F3F3',width=int(root.winfo_screenheight()/1334*750),
                             highlightthickness=5,highlightbackground='#777')
        self.nameEntry.grid(row=1,column=1)
        self.idEntry.grid(row=2,column=1)
        self.loginBtn=Label(self.loginFrame,text='Submit',font=('Courier',25),fg='#777777',bg='#BEBEBE')
        self.loginBtn.grid(row=3,column=1)
        self.loginBtn.bind('<Enter>',lambda event:self.loginBtn.config(fg='#555555',bg='#DEDEDE'))
        self.loginBtn.bind('<Leave>',lambda event:self.loginBtn.config(fg='#777777',bg='#BEBEBE'))
        self.loginBtn.bind('<Button-1>',lambda event:self.submit(self.nameEntry.get(),self.idEntry.get()))
        self.loginFrame.grid_rowconfigure(0,pad=50)
        self.loginFrame.grid_rowconfigure(2,pad=50)
        self.loginFrame.grid_columnconfigure(1,weight=1)
        self.frames[3].grid_rowconfigure(1,weight=1)
        self.frames[3].grid_columnconfigure(1,weight=1)

    def select(self,index):
        for i in range(len(self.frames)):
            self.frames[i].grid_remove()
            self.iconBtns[i]['image']=self.iconImgs[i][0]
            self.iconBtns[i].photo=self.iconImgs[i][0]
        self.frames[index].grid(row=1,sticky='N')
        self.iconBtns[index]['image']=self.iconImgs[index][1]
        self.iconBtns[index].photo=self.iconImgs[index][1]
        if index==2:
            self.explore()
            self.frames[2].grid_columnconfigure(1,weight=1)
            for i in range(len(self.matchData)):
                name,wechat=self.matchData[i].split('%')
                self.match.append(Frame(self.frames[2],width=int(root.winfo_screenheight()/1334*750),height=100,bd=3,relief=RAISED,bg='#AEAEAE'))
                self.match[i].grid(row=i,column=1)
                self.match[i].grid_rowconfigure(1,weight=1)
                self.match[i].grid_columnconfigure(0,weight=1)
                self.match[i].grid_columnconfigure(1,weight=1)
                self.match[i].grid_propagate(0)
                Label(self.match[i],text='Name: '+name,fg='#E2E2E2',bg='#AEAEAE',font=('Courier',20)).grid(row=1,column=0)
                Label(self.match[i],text='Wechat: '+wechat,fg='#E2E2E2',bg='#AEAEAE',font=('Courier',20)).grid(row=1,column=1)

    def explore(self):
        url='http://47.52.161.199/explore/'
        for i in range(len(self.match)):
            self.match[i].grid_remove()
        tags=getTags()
        out=tags[0]
        for i in tags[1:]:
            out+='&'+i
        response=post(url,data={'tags':out})
        try:
            self.matchData=response.json()['match']
        except Exception as e:
            print('Client Error: '+str(e))

    def submit(self,username,wechat):
        url='http://47.52.161.199/data/'
        tags=getTags()
        out=tags[0]
        for i in tags[1:]:
            out+='&'+i
        response=post(url,data={'username':username,'wechat':wechat,'tags':out})
        if response.text=='Submit Successful':
            print('YAY!!!')
        else:
            print(response.text[:100])

    def gen_cloud(self,event):
        data=genWordCloud().to_image()
        directory=filedialog.askdirectory()
        if len(directory)>0:
            data.save(directory+'/cloud.jpg')

    def gen_btn_enter(self,event):
        self.exportBtn['image']=self.generateBtnImgs[1]
        self.exportBtn.photo=self.generateBtnImgs[1]

    def gen_btn_exit(self,event):
        self.exportBtn['image']=self.generateBtnImgs[0]
        self.exportBtn.photo=self.generateBtnImgs[0]

    def btn_enter(self,event):
        self.on_btn['image']=self.imgs[1+self.record*2]
        self.on_btn.photo=self.imgs[1+self.record*2]

    def btn_exit(self,event):
        self.on_btn['image']=self.imgs[self.record*2]
        self.on_btn.photo=self.imgs[self.record*2]

    def btn_click(self,event):
        self.record=not self.record
        self.on_btn['image']=self.imgs[self.record*2]
        self.on_btn.photo=self.imgs[self.record*2]

cleanup()
root=Tk()
gui=GUI(root)
sc=SpeechClient()
running=True
t=Thread(target=update,args=(gui,sc,lambda:running))
t.start()
root.mainloop()
running=False
