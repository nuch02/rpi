import speech_recognition as sr
from gtts import gTTS
import time
from tkinter import *
import os
import openai


def audio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
      print("Say something!")
      r.adjust_for_ambient_noise(source)
      audio = r.listen(source)
      data = r.recognize_google(audio)
      print(data)

    return data



def speak(audiostring):
    tts=gTTS(text=audiostring,lang="en")
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")

openai.api_key = ''
messages = [ {"role": "system", "content": "You are an intelligent assistant." } ]
def info():

    message=audio().replace(" ","")

    messages.append(
        {"role": "user", "content": message},
    )

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )

    reply = chat.choices[0].message

    print("Assistant: ", reply.content)
    speak(reply.content)

    messages.append(reply)

win = Tk()
win.geometry('320x50');win.title('Freedomtech Player')
button = Button(win, text="Speak", command = info )
button.pack()
win.mainloop()
