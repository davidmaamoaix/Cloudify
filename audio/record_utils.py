#Record

import os
import sounddevice as sd

def audio_thread(speech_client,nlp,duration=10,fs=16000,file='temp.pcm'):
    rec=sd.rec(duration*fs,samplerate=fs,channels=1,dtype='int16')
    sd.wait()
    pcm=rec.tostring()
    with open(file,'wb') as f:
        f.write(pcm)
    result=speech_client.post_audio(file)
    os.remove(file)
    if result[:5].lower()!='error':
        nlp(result)
    else:
        print(result)
