#Backend

import json
import numpy as np
from jieba import cut
from uuid import uuid4
from random import randint
from wordcloud import WordCloud
from audio.record_utils import audio_thread

def update_json(speech_client):
    audio_thread(speech_client,nlp,file='temp/'+str(uuid4())+'.pcm')

def nlp(string):
    keywords=[j for j in process_string(string)]
    with open('keywords.json','r+') as f:
        try:
            wordFile=json.load(f)
        except ValueError:
            wordFile={}
    for i in keywords:
        if i in wordFile:
            wordFile[i]+=1
        else:
            wordFile[i]=1
    #print(wordFile)
    with open('keywords.json','w+') as f:
        json.dump(wordFile,f)

def process_string(raw):
    with open('stopwords.txt','rb') as f:
        stopwords=[i.decode('utf-8')[:-1] for i in f.readlines()]
    out=[i for i in cut(raw) if i not in stopwords and i!='\n']
    return out

def genWordCloud():
    with open('keywords.json','r+') as f:
        try:
            wordFile=json.load(f)
        except ValueError:
            wordFile={}
    wc=WordCloud('font/SimSun.ttf',width=1280,height=1280,background_color='#FFF',max_font_size=100,mask=np.load('masks/Mask_{}.npy'.format(randint(0,4))))
    wc.fit_words(wordFile)
    return wc

def getTags():
    with open('keywords.json','r+') as f:
        try:
            wordFile=json.load(f)
        except ValueError:
            return []
    tags=sorted(wordFile.keys(),key=lambda x:wordFile[x])
    if len(tags)>50:
        tags=tags[:50]
    return tags
