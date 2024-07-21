import os
import time
import threading

from dotenv import load_dotenv, dotenv_values
from openai import OpenAI
import speech_recognition as sr
from gtts import gTTS
import parselmouth
from playsound import playsound 

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def vocalize_reponse(text, audio_file):
    generated_audio = gTTS(text=text, lang='en') # Generate text to speech then save to file
    generated_audio.save(audio_file)


def play_audio_with_mouth_sync(audio_file):
    timings = find_word_timings(audio_file)

    audio_thread = threading.Thread(target=playsound, args=(audio_file,)) # Play audio asychronously
    animation_thread = threading.Thread(target=simulate_mouth, args=(timings,)) # Pipe word timings into animation function thread (make sure args passed as 2D array and not multiple sub arrays)
    audio_thread.start()
    animation_thread.start()

    audio_thread.join()
    animation_thread.join()


def find_word_timings(audio_file):
    response_audio = parselmouth.Sound(audio_file)
    response_intensity = response_audio.to_intensity() # Use intensity to detect if a word is being currently

    response_times = response_intensity.xs()
    response_values = response_intensity.values.T
    intensity_threshold = response_intensity.get_average()
    
    speech_segments = []
    is_speaking = False
    segment_start = None

    for time in range(0, len(response_times)):
        if response_values[time] > intensity_threshold and not is_speaking:
            is_speaking = True
            segment_start = response_times[time]
        elif response_values[time] <= intensity_threshold and is_speaking:
            is_speaking = False
            speech_segments.append((segment_start, response_times[time]))
            segment_start = None
    
    return speech_segments
    
def simulate_mouth(timings):
    word_number = 0
    start_time = time.time()

    while word_number < len(timings):
        current_time = time.time()-start_time

        if current_time >= timings[word_number][0] and current_time <= timings[word_number][1]:
            print("Simulate Open")
            time.sleep(timings[word_number][1]-timings[word_number][0])
            print("Simulate Close")
            word_number = word_number+1


def main(): 
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True # Adjust for ambient noise in environment

    # Use default microphone as audio source (works locally but currently broken in dev container)
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

    print("Listening Complete!")

    try:
        transcription = recognizer.recognize_whisper_api(audio, api_key=api_key)
        vocalize_reponse(transcription, "src/response/speech.mp3")
        play_audio_with_mouth_sync("src/response/speech.mp3")
        
    except sr.RequestError as error:
        print(f"Could not request results from Whisper API; {error}")


if __name__ == "__main__":
    main()