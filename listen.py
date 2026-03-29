import speech_recognition as sr


def listen(lang_code):
    lang_map = {
        "en": "en-IN",
        "pa": "pa-IN",
        "hi": "hi-IN"
    }

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 1000  # Force set it high
    recognizer.dynamic_energy_threshold = False  # Don't let it auto-adjust to wrong value
    recognizer.pause_threshold = 2

    with sr.Microphone() as source:
        print("\n🎤 Listening... Speak now! (You have 20 seconds)")
        # Remove adjust_for_ambient_noise — it's causing the low threshold!

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=20
            )
            print("⏳ Processing your voice...")

            text = recognizer.recognize_google(
                audio,
                language=lang_map.get(lang_code, "en-IN")
            )
            print(f"✅ You said: {text}")
            return text

        except sr.WaitTimeoutError:
            print("❌ No voice detected, please try again")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand, please speak clearly")
            return None
        except sr.RequestError:
            print("❌ Internet issue, voice not working")
            return None