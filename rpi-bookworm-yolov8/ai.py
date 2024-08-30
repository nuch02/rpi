import speech_recognition as sr
from gtts import gTTS
import os
import time
from tkinter import *


def audio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
      print("พูดอะไรบางอย่าง!")
      tts=gTTS(text="พูดบางอย่าง!",lang="th")
      tts.save("audio2.mp3")
      os.system("mpg321 audio2.mp3")
      r.adjust_for_ambient_noise(source)
      audio = r.listen(source)
      data = r.recognize_google(audio, language="th-TH")
      print(data)

    return data



def speak(audiostring):
    tts=gTTS(text=audiostring,lang="th")
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")