import speech_recognition as sr

r = sr.Recognizer()

# List all available microphones
print("Available microphones:")
for i, mic in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{i}: {mic}")

# Test with microphone index 0
print("\n🎤 Say something now!")
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=2)
    print(f"Energy threshold: {r.energy_threshold}")
    audio = r.listen(source, timeout=10, phrase_time_limit=15)
    print("Got audio! Processing...")
    text = r.recognize_google(audio, language="en-IN")
    print(f"You said: {text}")