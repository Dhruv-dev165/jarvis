import speech_recognition as sr
import pyttsx3
import os
import subprocess
import datetime
import webbrowser

# Text-to-Speech (TTS) Initialization
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

# Dictionary for predefined applications and their paths
app_paths = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "vlc": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
    "spotify": "C:\\Users\\YourUsername\\AppData\\Roaming\\Spotify\\Spotify.exe",
    "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
    "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
    "file explorer": "explorer.exe",
}

def speak(text):
    """Function to make Jarvis speak."""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greet the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning! I am Jarvis. How can I assist you today?")
    elif 12 <= hour < 18:
        speak("Good afternoon! I am Jarvis. How can I assist you?")
    else:
        speak("Good evening! I am Jarvis. How can I assist you?")

def take_command():
    """Listen to the user's voice and return it as a command string."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that. Please repeat.")
            return "None"
        except sr.RequestError:
            speak("Sorry, there's a network issue. Please try again.")
            return "None"

def open_application(command):
    """Open the requested application if it's in the predefined list."""
    for app_name in app_paths.keys():
        if app_name in command:
            app_path = app_paths[app_name]
            speak(f"Opening {app_name}.")
            subprocess.Popen(app_path, shell=True)
            return
    speak("Sorry, I couldn't find that application in my system. You can add it to my database.")

def search_web(query):
    """Search the web using Google."""
    speak(f"Searching Google for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def execute_command(command):
    """Function to execute different commands."""
    if 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {current_time}.")
    elif 'open' in command:
        open_application(command)
    elif 'search for' in command:
        query = command.replace("search for", "").strip()
        search_web(query)
    elif 'quit' in command or 'exit' in command:
        speak("Goodbye! Have a great day.")
        exit()
    else:
        speak("I didn't catch that. Can you try again?")

if __name__ == "__main__":
    greet_user()
    while True:
        user_command = take_command()
        if user_command != "None":
            execute_command(user_command)
