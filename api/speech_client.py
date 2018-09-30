#SpeechClient

from uuid import getnode
from aip import AipSpeech
from base64 import b64decode

class SpeechClient:
    
    def __init__(self,path='baidu_keys.txt'):
        with open(path,'rb') as f:
            keys=b64decode(f.readline())
        APP_ID,API_KEY,SECRET_KEY=keys.decode('utf-8').split('%')
        self.client=AipSpeech(APP_ID,API_KEY,SECRET_KEY)

    def post_audio(self,path):
        try:
            with open(path,'rb') as f:
                audio=f.read()
        except IOError as e:
            return 'Error:0'
        try:
            response=self.client.asr(audio,path.split('.')[-1],16000,{'dev_pid':1537})
        except Exception:
            return 'Error:1'
        if response['err_no']!=0:
            return 'Error:{}'.format(response['err_no'])
        return response['result'][0]
