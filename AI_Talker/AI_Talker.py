
# ========Library Required==============
# Voice recognition                 ==> pip install SpeechRecognition
# To get wikipedia data             ==> pip install wikipedia
# To speak out, or text to speech   ==> pip install pyttsx3
# For advance control on browser    ==> pip3 install pywhatkit
# To get funny jokes                ==> pip install pyjokes
# To get audio working              ==> pip install pyaudio
# ===========================================

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes


from gtts import gTTS


AI_Name = 'Hey Dude'
VoiceRate = 135



listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate',VoiceRate)
engine.runAndWait()

class Home_AI:

    shutoff = False

    def __init__(self):
       #create sectors locations:
       self.name = AI_Name.lower()
       self.shutoff = False

    def __del__(self):
        print('bye!')
        shutoff = True

    def talk(self,text):
        tts = gTTS(text=self.text, lang = "en")
        filename ="voice.mp3"
        tts.save(filename)
        playsound.playsound(filename)
    
    
        #engine.say(text)
        #engine.runAndWait()


    def take_command(self):

        try:
            with sr.Microphone() as source:
                print('Any question?')
                voice = listener.listen(source)
                command = listener.recognize_google(voice)

                print("Your statement: ", command)
                command = command.lower()
                if self.name in command:
                    command = command.replace(self.name , '')
                    print(command)
                    return command
        except:
            pass
        return

    def run_AI(self):

        command = self.take_command()

        if command is not None:
            print(command)
            if 'play' in command:
                song = command.replace('play', '')
                self.talk('playing' + song)
                pywhatkit.playonyt(song)
            elif 'time' in command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                self.talk('The current time is ' + time)
                print(time)
            elif 'date' in command:
                time = datetime.datetime.now().strftime('%A, %d. %B %Y')
                self.talk('The current time is ' + time)
                print(time)
            elif 'who is' in command:
                person = command.replace('who is', '')
                try:
                    info = wikipedia.summary(person, 1)
                    print(info)
                    self.talk(info)
                except:
                    self.talk('I don\'t know nothing about this', person)

            elif 'what is' in command:
                thing = command.replace('what is', '')
                try:
                    info = wikipedia.summary(thing, 1)
                    print(info)
                    self.talk(info)
                except:
                     self.talk('I don\'t know nothing about this', thing)

            elif 'joke' in command:
                self.talk(pyjokes.get_joke())
            elif 'hello' in command:
                self.talk('Hello Andrei')
            elif 'how are you'  in command:
                self.talk('I am doing good! Thanks for asking!')
            elif 'shut off' in command:
                self.talk('OK I am turning off myself bye!')
                self.__del__()
            else:
                self.talk('I didn\'t understand well. Please say again.')
    def run(self):
        while True:
            self.run_AI()
            if self.shutoff == True:
              break


nova = Home_AI()
nova.run()
