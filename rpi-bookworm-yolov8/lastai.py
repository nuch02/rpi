from tkinter import *
import speech_recognition as sr
from gtts import gTTS
import os

# Function to handle speech recognition and text-to-speech
def info():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            data = r.recognize_google(audio)
            print("You said: " + data)
            speak(data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Function to convert text to speech
def speak(audiostring):
    tts = gTTS(text=audiostring, lang="en")
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")

# Tkinter GUI
win = Tk()
win.geometry('320x50')
win.title('Freedomtech Player')
button = Button(win, text="Speak", command=info)
button.pack()
win.mainloop()
