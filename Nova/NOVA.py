#_____________________________________________________N.O.V.A________________________________________________________
#Python modules used for this programm
import sys
import speech_recognition as sr
import pyttsx3
import pywhatkit
import pywhatkit as kit
import datetime
import wikipedia
import pyjokes
import webbrowser
import time
import subprocess
import os
import cv2
import random
from requests import get
import smtplib
import psutil
import instaloader
import pyautogui
import PyPDF2
from Recordings import Record_Option
from PIL import ImageGrab
import pyaudio
import wave
import numpy as np 
from PhoneNumer import Phonenumber_location_tracker
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from NovaUi import Ui_NovaUI
from pywikihow import search_wikihow
import speedtest
from pytube import YouTube
import qrcode
import contextvars

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id) 

#alarm
def alarm(query):
        timehere = open("Alarmtext.txt", "a")
        timehere.write(query)
        timehere.close()
        os.startfile("alarm.py")
class DataStore:
    _instance = None
    user_input = ""

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataStore, cls).__new__(cls)
        return cls._instance

    def set_user_input(self, input_value):
        DataStore.user_input = input_value

    def get_user_input(self):
        input_value = DataStore.user_input  
        return input_value
    
    def clear_user_input(self):
        DataStore.user_input = ""
    
class MainThread(QThread):
    command_recognized = pyqtSignal(str)  # Signal to send recognized text
    def __init__(self):
        super(MainThread,self).__init__()
    
    def run(self):
        self.Intro()
   
    #function that will take the commands  to convert voice into text
    def take_Command(self):
        try:
            listener = sr.Recognizer()
            with sr.Microphone() as source:

                print('Listening....')
                listener.pause_threshold = 1
                voice = listener.listen(source,timeout=4,phrase_time_limit=7)
                print("Recognizing...")
                command1 = listener.recognize_google(voice,language='en-in')
                command1 = command1.lower()
                self.command_recognized.emit(command1)  
                if 'Nova' in command1: 
                    command1 = command1.replace('Nova','')    
            return command1
        except:
            self.command_recognized.emit("None")
            return 'None'
        
    #nova commands controller 
    def run_Nova(self):
        self.talk('Hello I am nova your assistant. please tell me how can i help you')
        while True:
            self.command = self.take_Command() 
            print(self.command)
            if ('play a song' in self.command) or ('youtube' in self.command) or ("download a song" in self.command) or ("download song" in self.command) : 
                #commands for opening youtube, playing a song in youtube, and download a song in youtube
                self.yt(self.command)
            #Interaction commands with nova
            elif ('your age' in self.command) or ('are you there' in self.command) or ('tell me something' in self.command) or ('thank you' in self.command) or ('in your free time' in self.command) or ('can you hear me' in self.command) or ('do you ever get tired' in self.command):
                self.Fun(self.command)
            elif 'time' in self.command : 
                self.Clock_time(self.command)
            elif (('hi' in self.command) and len(self.command)==2) or ((('hai' in self.command) or ('hey' in self.command)) and len(self.command)==3) or (('hello' in self.command) and len(self.command)==5):
                self.comum(self.command)
            elif ('what can you do' in self.command) or ('your name' in self.command) or ('my name' in self.command) or ('university name' in self.command):
                self.Fun(self.command)
            elif ('joke'in self.command) or ('date' in self.command):
                self.Fun(self.command)
            #It will tell the day 
            elif ("today" in self.command):
                day = self.Cal_day()
                self.talk("Today is "+day)
            #command to keep nova silent for maximum of 10mins
            elif ('silence' in self.command) or ('silent' in self.command) or ('keep quiet' in self.command) or ('wait for' in self.command) :
                self.silenceTime(self.command)
            #Command for opening the social media accounts in webrowser
            elif ('facebook' in self.command) or ('whatsapp' in self.command) or ('instagram' in self.command) or ('twitter' in self.command)  or ('social media' in self.command):
                self.social(self.command)
            #command for opening the OTT platform accounts
            elif ('hotstar' in self.command) or ('prime' in self.command) or ('netflix' in self.command):
                self.OTT(self.command)
            #command to search for something in wikipedia
            elif ('wikipedia' in self.command) or ('what is meant by' in self.command) or ('tell me about' in self.command) or ('who the heck is' in self.command):
                self.B_S(self.command)
            #command for opening the browsers and search for information in google
            elif ('open google'in self.command) or ('open edge'in self.command) :
                self.brows(self.command)
            #command to open the google applications
            elif ('open gmail'in self.command) or('open maps'in self.command) or('open calender'in self.command) or('open documents'in self.command )or('open spredsheet'in self.command) or('open images'in self.command) or('open drive'in self.command) or('open news' in self.command):
                self.Google_Apps(self.command)
           
            #commands to open presentaion makeing tools like CANVA and GOOGLE SLIDES
            elif ('slides'in self.command) or ('canva'in self.command) :
                self.edit(self.command)
            #Command to open desktop applications
            elif ('open calculator'in self.command) or ('open notepad'in self.command) or ('open paint'in self.command)   or ('open editor'in self.command) or ('open spotify'in self.command)  or ('open media player'in self.command):
                self.OpenApp(self.command)
            #Command to close desktop applications
            elif ('close calculator'in self.command) or ('close notepad'in self.command) or ('close paint'in self.command)  or ('close editor'in self.command) or ('close spotify'in self.command)  or ('close media player'in self.command):
                self.CloseApp(self.command)
            #command for opening shopping websites 
            elif ('flipkart'in self.command) or ('amazon'in self.command) :
                self.shopping(self.command)
            #command for asking your current location
            elif ('where i am' in self.command) or ('where we are' in self.command):
                self.locaiton()
            #command for opening command prompt 
            #Eg: nova open command prompt
            elif ('command prompt'in self.command) :
                self.talk('Opening command prompt')
                os.system('start cmd')
            #Command for opening an instagram profile and downloading the profile pictures of the profile
            elif ('instagram profile' in self.command) or("profile on instagram" in self.command):
                self.Instagram_Pro()
            #Command for opening taking screenshot
            #Eg: nova take a screenshot
            elif ('take screenshot' in self.command)or ('screenshot' in self.command) or("take a screenshot" in self.command):
                self.scshot()
            #Command for reading PDF
            #EG: nova read pdf
            elif ("read pdf" in self.command) or ("pdf" in self.command):
                self.pdf_reader()
            #command for searching for a procedure of how to do something
            #Eg:nova activate mod
            #   nova How to make a cake (or) nova how to convert int to string in programming 
            elif "activate mod" in self.command:
                self.How()
            #command for increaing the volume in the system
            #Eg: nova increase volume
            elif ("volume up" in self.command) or ("increase volume" in self.command):
                pyautogui.press("volumeup")
                self.talk('volume increased')
            #command for decreaseing the volume in the system
            #Eg: nova decrease volume
            elif ("volume down" in self.command) or ("decrease volume" in self.command):
                pyautogui.press("volumedown")
                self.talk('volume decreased')
            #Command to mute the system sound
            #Eg: nova mute the sound
            elif ("volume mute" in self.command) or ("mute the sound" in self.command) :
                pyautogui.press("volumemute")
                self.talk('volume muted')
            #command for opening your webcamera
            #Eg: nova open webcamera
            elif ('web cam'in self.command) :
                self.webCam()
            #Command for creating a new contact
            elif("create a new contact" in self.command):
                self.AddContact()
            #Command for searching for a contact
            elif("number in contacts" in self.command):
                self.NameIntheContDataBase(self.command)
            #Command for displaying all contacts
            elif("display all the contacts" in self.command) or ("display all contacts" in self.command) or ("display contacts" in self.command):
                self.Display()
            #Command for screenRecording
            #Eg: nova start Screen recording
            elif ("recording" in self.command) or ("screen recording" in self.command) or ("voice recording" in self.command):
                try:
                    self.talk("press q key to stop recordings")
                    option = self.command
                    Record_Option(option=option)
                    self.talk("recording is being saved")
                except:
                    self.talk("an unexpected error occured couldn't start screen recording")
            #command for playing a dowloaded mp3 song in which is present in the system
            #Eg: nova play music
            elif 'music' in self.command:
                try:
                    music_dir = 'E:\\music' 
                    songs = os.listdir(music_dir)
                    for song in songs:
                        if song.endswith('.mp3'):
                            os.startfile(os.path.join(music_dir, song))
                except:
                    self.talk("an unexpected error occured")
            #command for knowing the system IP address
            #Eg: nova check my ip address
            elif 'ip address' in self.command:
                ip = get('https://api.ipify.org').text
                print(f"your IP address is {ip}")
                self.talk(f"your IP address is {ip}")
            #command for sending a whatsapp  message
            elif ('send a message' in self.command):
                self.whatsapp(self.command)
            #command for sending an email 
            #Eg: nova send email
            elif 'send email' in self.command:
                self.verifyMail()
            #command for checking the temperature in surroundings
            #nova check the surroundings temperature
            elif "temperature" in self.command:
                self.temperature()
            #Command to generate the qr codes
            elif "create a qr code" in self.command:
                self.qrCodeGenerator()
            #command for checking internet speed
            #Eg: nova check my internet speed
            elif "internet speed" in self.command:
                self.InternetSpeed()
            #command to make the nova sleep
            elif ("you can sleep" in self.command) or ("sleep now" in self.command):
                self.talk("Okay, I am going to sleep you can call me anytime.")
                break
            #command for waking the nova from sleep
            #nova wake up
            elif ("wake up nova" in self.command) or ("get up nova" in self.command):
                self.talk("I am not sleeping, I am in online, what can I do for u")
            #command for exiting nova from the program
            #Eg: nova goodbye
            elif ("goodbye" in self.command) or ("get lost" in self.command):
                self.talk("Thanks for using me , have a good day")
                sys.exit()
            #command for knowing about the system condition
            #Eg: nova what is the system condition
            elif ('system condition' in self.command) or ('condition of the system' in self.command):
                self.talk("checking the system condition")
                self.condition()
            #command for knowing the latest news
            #Eg: nova tell me the news
            elif ('tell me news' in self.command) or ("the news" in self.command) or ("todays news" in self.command):
                self.talk("Please wait , featching the latest news")
                self.news()
            #command for shutting down the system
            #Eg: nova shutdown the system
            elif ('shutdown the system' in self.command) or ('down the system' in self.command):
                self.talk(" shutting down the system in 10 seconds")
                time.sleep(10)
                os.system("shutdown /s /t 5")
            #command for restarting the system
            #Eg: nova restart the system
            elif 'restart the system' in self.command:
                self.talk(" restarting the system in 10 seconds")
                time.sleep(10)
                os.system("shutdown /r /t 5")
            #command for make the system sleep
            #Eg: nova sleep the system
            elif 'sleep the system' in self.command:
                self.talk(" the system is going to sleep")
                os.system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")    
            elif "play a game" in self.command:
                    from game import game_play
                    game_play()
            elif "set alarm" in self.command:
                    self.talk("Set the time")
                    s = self.take_Command()
                    alarm(s)
                    self.talk("Done, ")
            elif 'create a file' in self.command:
                    self.talk('tell me a file name')
                    file_name = self.take_Command().lower()
                    with open(f"{file_name}.txt", "w") as file:
                    # Write content to the file
                        self.talk('what content i want to write')
                        content = self.take_Command().lower()
                        file.write(f"{content}")
                        self.talk("File created successfully!")

    #Intro msg
    def Intro(self):
        while True:
            self.permission = self.take_Command()
            print(self.permission)
            if ("wake up nova" in self.permission) or ("get up nova" in self.permission):
                self.run_Nova()
            elif ("goodbye nova" in self.permission) or ("get lost nova" in self.permission):
                self.talk("Thanks for using me,have a good day")
                sys.exit()                
    #Talk 
    def talk(self,text):
        engine.say(text)
        engine.runAndWait()

    #Wish
    def wish(self):
        hour = int(datetime.datetime.now().hour)
        t = time.strftime("%I:%M %p")
        day = self.Cal_day()
        print(t)
        if (hour>=0) and (hour <=12) and ('AM' in t):
            self.talk(f'Good morning  , its {day} and the time is {t}')
        elif (hour >= 12) and (hour <= 16) and ('PM' in t):
            self.talk(f"good afternoon, its {day} and the time is {t}")
        else:
            self.talk(f"good evening, its {day} and the time is {t}")

    #Weather forecast
    def temperature(self):
        IP_Address = get('https://api.ipify.org').text
        url = 'https://get.geojs.io/v1/ip/geo/'+IP_Address+'.json'
        geo_reqeust = get(url)
        geo_data = geo_reqeust.json()
        city = geo_data['city']
        search = f"temperature in {city}"
        url_1 = f"https://www.google.com/search?q={search}"
        r = get(url_1)
        data = BeautifulSoup(r.text,"html.parser")
        temp = data.find("div",class_="BNeawe").text
        self.talk(f"current {search} is {temp}")
    
    #qrCodeGenerator
    def qrCodeGenerator(self):
        self.talk(f"enter the text/link that you want to keep in the qr code")
        input_Text_link = self.get_user_input("Enter the Text/Link : ")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,
            border=4,
        )
        QRfile_name = (str(datetime.datetime.now())).replace(" ","-")
        QRfile_name = QRfile_name.replace(":","-")
        QRfile_name = QRfile_name.replace(".","-")
        QRfile_name = QRfile_name+"-QR.png"
        qr.add_data(input_Text_link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"QRCodes\{QRfile_name}")
        self.talk(f"  the qr code has been generated")

    #Web camera
    def webCam(self):    
        self.talk('Opening camera')
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow('web camera',img)
            k = cv2.waitKey(50)
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    #Whatsapp
    def whatsapp(self,command):
        try:
            command = command.replace('send a message to','')
            command = command.strip()
            name,numberID,F = self.SearchCont(command)
            if F:
                print(numberID)
                self.talk(f'what message do you want to send to {name}')
                message = self.take_Command()
                hour = int(datetime.datetime.now().hour)
                min = int(datetime.datetime.now().minute)
                print(hour,min)
                if "group" in command:
                    kit.sendwhatmsg_to_group(numberID,message,int(hour),int(min)+1)
                else:
                    kit.sendwhatmsg(numberID,message,int(hour),int(min)+1)
                self.talk("  message have been sent")
            if F==False:
                self.talk(f'the name not found in our data base, shall I add the contact')
                AddOrNot = self.take_Command()
                print(AddOrNot)
                if ("yes" in AddOrNot) or ("add" in AddOrNot) or ("yeah" in AddOrNot) or ("yah" in AddOrNot):
                    self.AddContact()
                elif("no" in AddOrNot):
                    self.talk('Ok  ')
        except:
            print("Error occured, please try again")


    #Add contacts
    def AddContact(self):
        self.talk(f'Enter the contact details')
        name = self.get_user_input("Enter the name :")
        print("add contact"+name)
        number = self.get_user_input("Enter the number :")
        print("executed")
        NumberFormat = f'"{name}":"+91{number}"'
        print(NumberFormat)
        try:
            with open("Contacts.txt", "a") as ContFile:
                ContFile.write(f"{NumberFormat}\n")
            self.talk(f'Contact Saved Successfully')
        except Exception as e:
            self.talk(f"An error occurred: {e}")
            print(f"Error: {e}")

    def get_user_input(self, prompt):
        self.command_recognized.emit(prompt)  # Prompt user with the text
        user_input = ""
        
        while True:
            data_store = DataStore()
            user_input = data_store.get_user_input().strip().lower()  
            # If the input is empty, ask again
            if not user_input:
                self.talk("")
            else:
                data_store.clear_user_input()
                break  # Exit loop if input is valid
        
        return user_input

    #Search Contact
    def SearchCont(self,name):
        with open("Contacts.txt","r") as ContactsFile:
            for line in ContactsFile:
                if name in line:
                    print("Name Match Found")
                    s = line.split("\"")
                    return s[1],s[3],True
        return 0,0,False
    
    #Display all contacts
    def Display(self):
        ContactsFile = open("Contacts.txt","r")
        count=0
        for line in ContactsFile:
            count+=1
        ContactsFile.close()
        ContactsFile = open("Contacts.txt","r")
        self.talk(f"displaying the {count} contacts stored in our data base")    
        for line in ContactsFile:
            s = line.split("\"")
            print("Name: "+s[1])
            print("Number: "+s[3])
        ContactsFile.close()

    #search contact
    def NameIntheContDataBase(self,command):
        line = command
        line = line.split("number in contacts")[0]
        if("tell me" in line):
            name = line.split("tell me")[1]
            name = name.strip()
        else:
            name= line.strip()
        name,number,bo = self.SearchCont(name)
        if bo:
            print(f"Contact Match Found in our data base with {name} and the mboile number is {number}")
            self.talk(f"Contact Match Found in our data base with {name} and the mboile number is {number}")
        else:
            self.talk("the name not found in our data base, shall I add the contact")
            AddOrNot = self.take_Command()
            print(AddOrNot)
            if ("yes add it" in AddOrNot)or ("yeah" in AddOrNot) or ("yah" in AddOrNot):
                self.AddContact()
                self.talk(f',Contact Saved Successfully')
            elif("no" in AddOrNot) or ("don't add" in AddOrNot):
                self.talk('Ok  ')

    #Internet spped
    def InternetSpeed(self):
        self.talk("Wait a few seconds,checking your internet speed")
        st = speedtest.Speedtest()
        dl = st.download()
        dl = dl/(1000000) #converting bytes to megabytes
        up = st.upload()
        up = up/(1000000)
        print(dl,up)
        self.talk(f"we have {dl} megabytes per second downloading speed and {up} megabytes per second uploading speed")
        
    #Search for a process how to do
    def How(self):
        self.talk("How to do mode is activated")
        while True:
            self.talk("Please tell me what you want to know")
            how = self.take_Command()
            try:
                if ("exit" in how) or("close" in how):
                    self.talk("Ok how to mode is closed")
                    break
                else:
                    max_result=1
                    how_to = search_wikihow(how,max_result)
                    assert len(how_to) == 1
                    how_to[0].print()
                    self.talk(how_to[0].summary)
            except Exception as e:
                self.talk("Sorry,I am not able to find this")

    #Communication commands
    def comum(self,command):
        print(command)
        if ('hi'in command) or('hai'in command) or ('hey'in command) or ('hello' in command) :
            self.talk("Hello what can I help for u")
        else :
            self.No_result_found()

    #Fun commands to interact with nova
    def Fun(self,command):
        print(command)
        if 'your name' in command:
            self.talk("My name is nova")
        elif 'my name' in command:
            self.talk("your name is AIT's")
        elif 'university name' in command:
            self.talk("you are studing in Acharya, with bachelor of engineering in information science and engineering") 
        elif 'what can you do' in command:
            self.talk("I talk with you until you want to stop, I can say time, open your social media accounts,your open source accounts, open google browser,and I can also open your college websites, I can search for some thing in google and I can tell jokes")
        elif 'your age' in command:
            self.talk("I am very younger than u")
        elif 'date' in command:
            self.talk('Sorry not intreseted,I am having headache, we will catch up some other time')
        elif 'are you single' in command:
            self.talk('No, I am in a relationship with wifi')
        elif 'joke' in command:
            self.talk(pyjokes.get_joke())
        elif 'are you there' in command:
            self.talk('YesI am here')
        elif 'tell me something' in command:
            self.talk('I don\'t have much to say, you only tell me someting i will give you the company')
        elif 'thank you' in command:
            self.talk('I am here to help you..., your welcome')
        elif 'in your free time' in self.command:
            self.talk('I will be listening to all your words')
        elif 'i love you' in command:
            self.talk('I love you too  ')
        elif 'can you hear me' in command:
            self.talk('Yes,I can hear you')
        elif 'do you ever get tired' in command:
            self.talk('It would be impossible to tire of our conversation')
        else :
            self.No_result_found()

    #Social media accounts commands
    def social(self,command):
        print(command)
        if 'facebook' in command:
            self.talk('opening your facebook')
            webbrowser.open('https://www.facebook.com/')
        elif 'whatsapp' in command:
            self.talk('opening your whatsapp')
            webbrowser.open('https://web.whatsapp.com/')
        elif 'instagram' in command:
            self.talk('opening your instagram')
            webbrowser.open('https://www.instagram.com/')
        elif 'twitter' in command:
            self.talk('opening your twitter')
            webbrowser.open('https://twitter.com/Suj8_116')
       
        else :
            self.No_result_found()
        
    #clock commands
    def Clock_time(self,command):
        print(command)
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        self.talk("Current time is "+time)
    
    #calender day
    def Cal_day(self):
        day = datetime.datetime.today().weekday() + 1
        Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',4: 'Thursday', 5: 'Friday', 6: 'Saturday',7: 'Sunday'}
        if day in Day_dict.keys():
            day_of_the_week = Day_dict[day]
            print(day_of_the_week)
        
        return day_of_the_week

    #college resources commands
    def college(self,command):
        print(command)
        if 'teams' in command:
            self.talk('opening your microsoft teams')
            webbrowser.open('https://teams.microsoft.com/')
        elif 'stream' in command:
            self.talk('opening your microsoft stream')
            webbrowser.open('https://web.microsoftstream.com/')
        elif 'outlook' in command:
            self.talk('opening your microsoft school outlook')
            webbrowser.open('https://outlook.office.com/mail/')
        else :
            self.No_result_found()

    #Browser Search commands
    def B_S(self,command):
        print(command)
        try:
            # ('what is meant by' in self.command) or ('tell me about' in self.command) or ('who the heck is' in self.command)
            if ('wikipedia' in command):
                target1 = command.replace('search for','')
                target1 = target1.replace('in wikipedia','')
            elif('what is meant by' in command):
                target1 = command.replace("what is meant by"," ")
            elif('tell me about' in command):
                target1 = command.replace("tell me about"," ")
            elif('who the heck is' in command):
                target1 = command.replace("who the heck is"," ")
            print("searching....")
            info = wikipedia.summary(target1,5)
            print(info)
            self.talk("according to wikipedia "+info)
        except :
            self.No_result_found()
        
    #Browser
    def brows(self,command):
        print(command)
        if 'google' in command:
            self.talk("what should I search on google..")
            S = self.take_Command()#taking command for what to search in google
            webbrowser.open(f"{S}")
        elif 'edge' in command:
            self.talk('opening your Miscrosoft edge')
            os.startfile('..\\..\\MicrosoftEdge.exe')#path for your edge browser application
        else :
            self.No_result_found()

    #google applications selection
    def Google_Apps(self,command):
        print(command)
        if 'gmail' in command:
            self.talk('opening your google gmail')
            webbrowser.open('https://mail.google.com/mail/')
        elif 'maps' in command:
            self.talk('opening google maps')
            webbrowser.open('https://www.google.co.in/maps/')
        elif 'news' in command:
            self.talk('opening google news')
            webbrowser.open('https://news.google.com/')
        elif 'calender' in command:
            self.talk('opening google calender')
            webbrowser.open('https://calendar.google.com/calendar/')
        elif 'photos' in command:
            self.talk('opening your google photos')
            webbrowser.open('https://photos.google.com/')
        elif 'documents' in command:
            self.talk('opening your google documents')
            webbrowser.open('https://docs.google.com/document/')
        elif 'spreadsheet' in command:
            self.talk('opening your google spreadsheet')
            webbrowser.open('https://docs.google.com/spreadsheets/')
        else :
            self.No_result_found()

    #youtube
    def yt(self,command):
        print(command)
        if 'play' in command:
            self.talk("can you please say the name of the song")
            song = self.take_Command()
            if "play" in song:
                song = song.replace("play","")
            self.talk('playing '+song)
            print(f'playing {song}')
            pywhatkit.playonyt(song)
            print('playing')
        elif "download" in command:
            self.talk("please enter the youtube video link which you want to download")
            link = self.get_user_input("Enter the YOUTUBE video link: ")
            yt=YouTube(link)
            yt.streams.get_highest_resolution().download()
            self.talk(f"downloaded {yt.title} from the link you given into the main folder")
        elif 'youtube' in command:
            self.talk('opening your youtube')
            webbrowser.open('https://www.youtube.com/')
        else :
            self.No_result_found()

    #Photo shops
    def edit(self,command):
        print(command)
        if 'slides' in command:
            self.talk('opening your google slides')
            webbrowser.open('https://docs.google.com/presentation/')
        elif 'canva' in command:
            self.talk('opening your canva')
            webbrowser.open('https://www.canva.com/')
        else :
            self.No_result_found()

    #OTT 
    def OTT(self,command):
        print(command)
        if 'hotstar' in command:
            self.talk('opening your disney plus hotstar')
            webbrowser.open('https://www.hotstar.com/in')
        elif 'prime' in command:
            self.talk('opening your amazon prime videos')
            webbrowser.open('https://www.primevideo.com/')
        elif 'netflix' in command:
            self.talk('opening Netflix videos')
            webbrowser.open('https://www.netflix.com/')
        else :
            self.No_result_found()

    #PC allications
    def OpenApp(self,command):
        print(command)
        if ('calculator'in command) :
            self.talk('Opening calculator')
            os.startfile('C:\\Windows\\System32\\calc.exe')
        elif ('paint'in command) :
            self.talk('Opening msPaint')
            os.startfile('c:\\Windows\\System32\\mspaint.exe')
        elif ('notepad'in command) :
            self.talk('Opening notepad')
            os.startfile('c:\\Windows\\System32\\notepad.exe')
        elif ('editor'in command) :
            self.talk('Opening your Visual studio code')
            os.startfile('..\\..\\Code.exe')
        elif ('spotify'in command) :
            self.talk('Opening spotify')
            os.startfile('..\\..\\Spotify.exe')
        elif ('media player'in command) :
            self.talk('Opening VLC media player')
            os.startfile("C:\Program Files\VideoLAN\VLC\vlc.exe")
        else :
            self.No_result_found()
            
    #closeapplications function
    def CloseApp(self,command):
        print(command)
        if ('calculator'in command) :
            self.talk("okay  , closeing caliculator")
            os.system("taskkill /f /im calc.exe")
        elif ('paint'in command) :
            self.talk("okay,closeing mspaint")
            os.system("taskkill /f /im mspaint.exe")
        elif ('notepad'in command) :
            self.talk("okay  , closeing notepad")
            os.system("taskkill /f /im notepad.exe")
        elif ('editor'in command) :
            self.talk("okay  , closeing vs code")
            os.system("taskkill /f /im Code.exe")
        elif ('spotify'in command) :
            self.talk("okay  , closeing spotify")
            os.system("taskkill /f /im Spotify.exe")
        elif ('media player'in command) :
            self.talk("okay  , closeing media player")
            os.system("taskkill /f /im vlc.exe")
        else :
            self.No_result_found()

    #Shopping links
    def shopping(self,command):
        print(command)
        if 'flipkart' in command:
            self.talk('Opening flipkart online shopping website')
            webbrowser.open("https://www.flipkart.com/")
        elif 'amazon' in command:
            self.talk('Opening amazon online shopping website')
            webbrowser.open("https://www.amazon.in/")
        else :
            self.No_result_found()

    #PDF reader
    def pdf_reader(self):
        self.talk("  enter the name of the book which you want to read")
        n = self.get_user_input("Enter the book name: ")
        n = n.strip()+".pdf"
        book_n = open(n,'rb')
        pdfReader = PyPDF2.PdfFileReader(book_n)
        pages = pdfReader.numPages
        self.talk(f"there are total of {pages} in this book")
        self.talk("plsase enter the page number Which I nedd to read")
        num = int(self.get_user_input("Enter the page number: "))
        page = pdfReader.getPage(num)
        text = page.extractText()
        print(text)
        self.talk(text)

    #Time caliculating algorithm
    def silenceTime(self,command):
        print(command)
        x=0
        #caliculating the given time to seconds from the speech commnd string
        if ('10' in command) or ('ten' in command):x=600
        elif '1' in command or ('one' in command):x=60
        elif '2' in command or ('two' in command):x=120
        elif '3' in command or ('three' in command):x=180
        elif '4' in command or ('four' in command):x=240
        elif '5' in command or ('five' in command):x=300
        elif '6' in command or ('six' in command):x=360
        elif '7' in command or ('seven' in command):x=420
        elif '8' in command or ('eight' in command):x=480
        elif '9' in command or ('nine' in command):x=540
        self.silence(x)
        
    #Silence
    def silence(self,k):
        t = k
        s = "Ok   I will be silent for "+str(t/60)+" minutes"
        self.talk(s)
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
        self.talk("  "+str(k/60)+" minutes over")

    #Mail verification
    def verifyMail(self):
        try:
            self.talk("what should I say?")
            content = self.take_Command()
            self.talk("To whom do u want to send the email?")
            to = self.get_user_input("Enter to whom you want to send: ")
            self.SendEmail(to,content)
            self.talk("Email has been sent to "+str(to))
        except Exception as e:
            print(e)
            self.talk("Sorry I am not not able to send this email")
    
    #Email Sender
    def SendEmail(self,to,content):
        print(content)
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login("sdmp75407@gmail.com","lbbw taot rhbr jzcb")
        server.sendmail("sdmp75407@gmail.com",to,content)
        server.close()

    #location
    def locaiton(self):
        self.talk("Wait,let me check")
        try:
            IP_Address = get('https://api.ipify.org').text
            print(IP_Address)
            url = 'https://get.geojs.io/v1/ip/geo/'+IP_Address+'.json'
            print(url)
            geo_reqeust = get(url)
            geo_data = geo_reqeust.json()
            city = geo_data['city']
            state = geo_data['region']
            country = geo_data['country']
            tZ = geo_data['timezone']
            longitude = geo_data['longitude']
            latidute = geo_data['latitude']
            org = geo_data['organization_name']
            print(city+" "+state+" "+country+" "+tZ+" "+longitude+" "+latidute+" "+org)
            self.talk(f" i am not sure, but i think we are in {city} city of {state} state of {country} country")
            self.talk(f"and,we are in {tZ} timezone the latitude os our location is {latidute}, and the longitude of our location is {longitude}, and we are using {org}\'s network ")
        except Exception as e:
            self.talk("Sorry,due to network issue i am not able to find where we are.")
            pass

    #Instagram profile
    def Instagram_Pro(self):
        self.talk("please enter the user name of Instagram: ")
        name = self.get_user_input("Enter username here: ")
        webbrowser.open(f"www.instagram.com/{name}")
        time.sleep(5)
        self.talk(" would you like to download the profile picture of this account.")
        cond = self.take_Command()
        if('download' in cond):
            mod = instaloader.Instaloader()
            mod.download_profile(name,profile_pic_only=True)
            self.talk("I am done,profile picture is saved in your main folder. ")
        else:
            pass

    #ScreenShot
    def scshot(self):
        self.talk(" please tell me the name for this screenshot file")
        name = self.take_Command()
        self.talk("Please hold the screen for few seconds, I am taking screenshot")
        time.sleep(3)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        self.talk("I am done,the screenshot is saved in main folder.")

    #News
    def news(self):
        MAIN_URL_= "https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=984d416b6ad8453497bef6e1c21984e9"
        MAIN_PAGE_ = get(MAIN_URL_).json()
        articles = MAIN_PAGE_["articles"]
        headings=[]
        seq = ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth'] #If you need more than ten you can extend it in the list
        for ar in articles:
            headings.append(ar['title'])
        for i in range(len(seq)):
            print(f"todays {seq[i]} news is: {headings[i]}")
            self.talk(f"todays {seq[i]} news is: {headings[i]}")
        self.talk(" I am done, I have read most of the latest news")

    #System condition
    def condition(self):
        usage = str(psutil.cpu_percent())
        self.talk("CPU is at"+usage+" percentage")
        battray = psutil.sensors_battery()
        percentage = battray.percent
        self.talk(f" our system have {percentage} percentage Battery")
        if percentage >=75:
            self.talk(f" we could have enough charging to continue our work")
        elif percentage >=40 and percentage <=75:
            self.talk(f" we should connect out system to charging point to charge our battery")
        elif percentage >=15 and percentage <=30:
            self.talk(f" we don't have enough power to work, please connect to charging")
        else:
            self.talk(f" we have very low power, please connect to charging otherwise the system will shutdown very soon")
        
    #no result found
    def No_result_found(self):
        self.talk(' I couldn\'t understand, could you please say it again.')        

startExecution = MainThread()
class Main(QMainWindow):
    cpath =""

    user_text = ""
    
    def __init__(self,path):
        self.cpath = path
        super().__init__()
        self.ui = Ui_NovaUI(path=current_path)
        self.ui.setupUi(self)
        self.ui.pushButton_4.clicked.connect(self.startTask)
        self.ui.pushButton_3.clicked.connect(self.close)
        self.ui.submitButton.clicked.connect(self.on_submit)

    def update_recognition_text(self, recognized_text):
        # Update the textBrowser with recognized text
        self.ui.label_3.setText(recognized_text)
    
    def startTask(self):
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\ironman1.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\circle.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\lines1.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\ironman3.gif")
        self.ui.label_8.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\circle.gif")
        self.ui.label_9.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\powersource.gif")
        self.ui.label_12.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\powersource.gif")
        self.ui.label_13.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\ironman3_flipped.gif")
        self.ui.label_16.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\nova.gif")
        self.ui.label_17.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.command_recognized.connect(self.update_recognition_text)
        startExecution.start()
    
    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

    def on_submit(self):
        # Get the text from the input box
        user_input = self.ui.inputTextBox.text()
        data_store = DataStore()
        data_store.set_user_input(user_input)
        self.ui.inputTextBox.setText("")
    

current_path = os.getcwd()
app = QApplication(sys.argv)
Nova = Main(path=current_path)
Nova.show()
exit(app.exec_())