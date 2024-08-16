import pvporcupine
import pyaudio
import struct
import time,os
from faster_whisper import WhisperModel
from openai import OpenAI
import speech_recognition as sr
from elevenlabs import Voice,VoiceSettings, play
from elevenlabs.client import ElevenLabs
from assistant import AssistantManager
from playsound import playsound
import threading
from colorama import Fore,init

class Assistant:
    def __init__(self):
        self.r = sr.Recognizer()
        self.source = sr.Microphone()
        self.openaiclients = OpenAI(api_key="OPENAI API")
        self.elevenclient = ElevenLabs(api_key="ELEVENLABS API")
        self.asistant = AssistantManager(api_key="OPENAI API",tools_file="tools.json")
        self.idle_timer = None
        self.recognition_active = False
        init(autoreset=True)
    def text2Speech(self,question):
        audio = self.elevenclient.generate(
        text=question[:500],
        voice=Voice(
            voice_id="oWAxZDx7w5VEj9dCyTzz",
            settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
        ),
            model="eleven_multilingual_v2"
        )
        play(audio)

    def ask(self,question):
        response = self.openaiclients.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": question}]
        )
        result = response.choices[0].message.content
        # self.text2Speech(result)

    def callback(self,recognizer,audio):
        global recognition_active, idle_timer
        try:
            print("Listening...")
            try:
                # text = recognizer.recognize_google(audio).lower()
                text = recognizer.recognize_whisper_api(api_key="OPENAI API",audio_data=audio).lower()
                print(f"You said: {text}")

                if "alexa" in text:
                    print("Jarvis activated!")
                    self.recognition_active = True
                    self.start_idle_timer()

                elif self.recognition_active:
                    # print("Recognized speech in active mode.")
                    self.reset_idle_timer()
                    self.text2Speech(self.asistant.generate_response(text, "516", "fatihh",role='user'))

            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            except sr.UnknownValueError:
                print(Fore.RED+"Sorry, I did not understand that.")

        except sr.WaitTimeoutError:
            print(Fore.YELLOW + "Listening timed out, no speech detected.")
            if self.recognition_active:
                self.deactivate_recognition()

    def start_idle_timer(self):
        global idle_timer
        if self.idle_timer:
            idle_timer.cancel()
        idle_timer = threading.Timer(20, self.deactivate_recognition)
        idle_timer.start()

    # Function to reset the idle timer
    def reset_idle_timer(self):
        global idle_timer
        if self.idle_timer:
            idle_timer.cancel()
        idle_timer = threading.Timer(20, self.deactivate_recognition)
        idle_timer.start()

    # Function to deactivate recognition mode
    def deactivate_recognition(self):
        global recognition_active
        self.recognition_active = False
        print("Recognition mode deactivated due to inactivity.")


    def listening(self):
        with self.source as s:
            self.r.adjust_for_ambient_noise(s,duration=2)
        self.r.listen_in_background(self.source,self.callback)
        for _ in range(50): time.sleep(0.1)
        while True: time.sleep(0.1) 

    def main(self):
        while True:
            self.listening()

if __name__ == '__main__':
    vo = Assistant()
    vo.main()
    # vo.text2Speech("hi i'm jarvis, how i can help you today?")