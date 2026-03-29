from gtts import gTTS
import pygame
import time
import os

def speak(text, gtts_code):
    try:
        # Generate speech
        tts = gTTS(text=text, lang=gtts_code, slow=False)
        tts.save("response.mp3")
        time.sleep(0.5)

        # Play using pygame
        pygame.mixer.init()
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()

        # Wait until audio finishes
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()

    except Exception as e:
        print(f"Voice error: {e}")