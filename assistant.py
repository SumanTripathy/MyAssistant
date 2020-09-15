import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pyjokes
import cv2

engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices') #getting details of current voice
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio) 
    engine.runAndWait() #Without this command, speech will not be audible to us.

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Your Assistant Sir. Please tell me how may I help you")   

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')      #Using google for voice recognition.
        print(f"User said: {query}\n")                           #User query will be printed.

    except Exception as e:
        # print(e)    
        print("Say that again please...")                   #Say that again will be printed in case of improper voice 
        return "None"                                      
    return query    

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()
 
     

if __name__=="__main__" :
    wishMe()
    while True:
    # if 1:  #for one time
        query = takeCommand().lower() #Converting user query into lower case

        # Logic for executing tasks based on query
        if 'wikipedia' in query:  #if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2) 
            speak("According to Wikipedia")
            #print(results)
            speak(results)
        
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")  

        elif 'play music' in query:
            music_dir = 'D:\\songs\\song'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))  

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}") 

        elif 'open code' in query:
            codePath = "C:\\Users\\Suman Tripathy\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath) 

        elif 'joke' in query: 
            speak(pyjokes.get_joke()) 
        
        elif 'where is' in query:
            query=query.replace('where is','')
            location=query
            speak('locating on google maps'+location)
            webbrowser.open('https://www.google.com/maps/place/'+location)

        elif 'click photo' in query:
            cam = cv2.VideoCapture(0)
            cv2.namedWindow("test")
            img_counter = 0
            while True:
                ret, frame = cam.read()
                if not ret:
                    print("failed to grab frame")
                    break
                cv2.imshow("test", frame)
                k = cv2.waitKey(1)
                if k%256 == 27:
                    # ESC pressed
                     print("Escape hit, closing...")
                     break
                elif k%256 == 32:

                    # SPACE pressed
                    img_name = "opencv_frame_{}.png".format(img_counter)
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    img_counter += 1
            cam.release()
            cv2.destroyAllWindows()

        elif 'email to suman' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "st@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry. I am not able to send this email")    

        elif 'quit' in query:
            os._exit(0)