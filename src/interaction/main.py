import speech_recognition as sr
from ..private.key import OPENAI_API_KEY

def main(): 
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    print("Listening Complete!")

    try:
        print(f"Whisper API thinks you said \"{r.recognize_whisper_api(audio, api_key=OPENAI_API_KEY)}\"")
    except sr.RequestError as e:
        print(f"Could not request results from Whisper API; {e}")

if __name__ == "__main__":
    main()