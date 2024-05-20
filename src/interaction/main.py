import speech_recognition as sr
import pyttsx3
from ..private.key import OPENAI_API_KEY
from openai import OpenAI

def main(): 

    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True #adjust for ambient noise in environment
    engine = pyttsx3.init()

    # use default microphone as audio source
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

    print("Listening Complete!")

    try:
        transcription = recognizer.recognize_whisper_api(audio, api_key=OPENAI_API_KEY)
        print(transcription)
        engine.say(transcription)
        engine.runAndWait()
    except sr.RequestError as error:
        print(f"Could not request results from Whisper API; {error}")

if __name__ == "__main__":
    main()