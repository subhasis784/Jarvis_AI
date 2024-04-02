import os
import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
from num2words import num2words
import time
import openai


engiene = pyttsx3.init('sapi5')  #collecting voice(sapi5)
voices = engiene.getProperty('voices')
# print(voices[0])  # 0 for male voice and 1 for female voice prints the voice
engiene.setProperty('voice',voices[1].id)


def speak(audio):
    engiene.say(audio)
    engiene.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if(hour>=5 and hour<12):
        speak("Good Morning Sir")
    elif(hour>=12 and hour<18):
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")
    speak("how may I help you")

def play_video_with_sound(video_query):
    search_url = f"https://www.youtube.com/results?search_query={video_query.replace(' ', '+')}"
    # Open the URL in a new tab using the default web browser
    webbrowser.open_new_tab(search_url)


def takeCommand():
    #takes voice input and returns string output
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold = 1   #if you stop speaking for less than 1 second the program will not return
        r.energy_threshold=4000 #if little bit of noise is present then you have to speak louder
        audio = r.listen(source)
    
    try:
        print("Recognizing.....")
        query = r.recognize_google(audio,language='en-in')
        print(f"user said: {query}\n")

    except Exception as e :
        #print(e) #prints type of error
        print("Say it again please......")
        return "None"
    return query


#main method
if __name__=="__main__" : 
    wishMe()

    while(True):
        query = takeCommand().lower()   #converts all command to lower case

        #Logic for executing tasks
        if('wikipedia' in query):
            speak("Sarching Wikipedia.....")
            query = query.replace("wikipedia","")
            result = wikipedia.summary(query,sentences=2)
            speak("according to wikipedia")
            print(result)
            speak(result)

        
        elif ('youtube' in query):
            speak("opening youtube")
            webbrowser.open("youtube.com")


        elif 'play video' in query:
            speak("What video would you like me to play?")
            video_query = takeCommand().lower()
            search_url = f"https://www.youtube.com/results?search_query={video_query.replace(' ', '+')}"
            speak(f"Playing {video_query} on YouTube")
            webbrowser.open(search_url)


        elif ('google' in query):
            search_query = query.split('search google for')[-1].strip()
            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)

            
        elif 'open website' in query:
            # Extract the website name from the query
            website_name = query.split('open website')[-1].strip()
            # Construct the URL
            website_url = f"https://{website_name}.com"
            # Open the website
            speak(f"Opening {website_name}")
            webbrowser.open(website_url)


        elif 'open desktop' in query:
            # Open Desktop folder
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            os.startfile(desktop_path)


        elif 'open folder' in query:
            # Extract the folder name from the query
            folder_name = query.split('open folder')[-1].strip()
            folder_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', folder_name)
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                os.startfile(folder_path)
            else:
                speak(f"Sorry, {folder_name} folder not found on the desktop.")


        elif 'open' in query:
            # List of applications and their corresponding paths
            applications = {
                'notepad': r'C:\Windows\System32\notepad.exe',
                'calculator': r'C:\Windows\System32\calc.exe',
                'code':"C:\\Users\\HP\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
                'Word':"C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
                'ppt':"C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
                'excel':"C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
                'onenote':"C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE",
                'brave':"C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
                'microsoft edge':"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", 
            }
            app_name = query.split('open')[-1].strip()
            if app_name in applications:
                speak(f"Opening {app_name}")
                os.startfile(applications[app_name])
            else:
                speak("Sorry, I couldn't find that application.")


        #Implementing OPENAI Features
        elif 'AI' in query:
            openai.api_key = 'my_key_jarvis'
                   

        elif 'time' in query:
            now = datetime.datetime.now()
            hours = num2words(now.hour)
            minutes = num2words(now.minute)
            seconds = num2words(now.second)
            spoken_time = f"{hours} hours, {minutes} minutes, and {seconds} seconds"
            speak(f"Sir, the time is {spoken_time}")


        elif 'date' in query:
            now = datetime.datetime.now()
            day = num2words(now.day, ordinal=True)
            month = now.strftime('%B')
            year = num2words(now.year)
            spoken_date = f"{day} of {month}, {year}"
            speak(f"Sir, today is {spoken_date}")


        elif 'day' in query:
            # Get the current day
            current_day = datetime.datetime.now().strftime("%A")
            speak(f"Sir, today is {current_day}")


        elif 'quit' in query or 'exit' in query:
            speak("Goodbye Sir , Have a nice day")
            break


        else:
            speak("Sorry , I can't help you")