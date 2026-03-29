from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from deep_translator import GoogleTranslator
from voice import speak
from listen import listen
from weather import get_weather
import os



llm = ChatGroq(
    api_key="Your_GROQ_API_KEY",
    model="llama-3.3-70b-versatile",
    temperature=0.6
)

LANGUAGES = {
    "1": {"name": "English", "code": "en", "gtts": "en"},
    "2": {"name": "ਪੰਜਾਬੀ (Punjabi)", "code": "pa", "gtts": "pa"},
    "3": {"name": "हिंदी (Hindi)", "code": "hi", "gtts": "hi"},
}

TEXT = {
    "welcome": {
        "en": "Welcome to Kisan AI Agent",
        "pa": "ਕਿਸਾਨ AI ਏਜੰਟ ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ",
        "hi": "किसान AI एजेंट में आपका स्वागत है"
    },
    "select_topic": {
        "en": "What do you need help with?\n1. Weather Forecast\n2. Crop Advice\n3. Market Prices\n4. Government Schemes\n5. Exit",
        "pa": "ਤੁਹਾਨੂੰ ਕਿਸ ਚੀਜ਼ ਵਿੱਚ ਮਦਦ ਚਾਹੀਦੀ ਹੈ?\n1. ਮੌਸਮ ਦੀ ਭਵਿੱਖਬਾਣੀ\n2. ਫ਼ਸਲ ਸਲਾਹ\n3. ਬਾਜ਼ਾਰ ਭਾਅ\n4. ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ\n5. ਬਾਹਰ ਜਾਓ",
        "hi": "आपको किस चीज़ में मदद चाहिए?\n1. ਮੌਸਮ ਦੀ ਭਵਿੱਖਬਾਣੀ\n2. फसल सलाह\n3. बाज़ार भाव\n4. सरकारी योजनाएं\n5. बाहर जाएं"
    },
    "ask_question": {
        "en": "🎤 Speak your question or type it: ",
        "pa": "🎤 ਆਪਣਾ ਸਵਾਲ ਬੋਲੋ ਜਾਂ ਟਾਈਪ ਕਰੋ: ",
        "hi": "🎤 अपना सवाल बोलें या टाइप करें: "
    },
    "ask_city": {
        "en": "🎤 Speak or type your city name: ",
        "pa": "🎤 ਆਪਣੇ ਸ਼ਹਿਰ ਦਾ ਨਾਮ ਬੋਲੋ ਜਾਂ ਟਾਈਪ ਕਰੋ: ",
        "hi": "🎤 अपने शहर का नाम बोलें या टाइप करें: "
    },
    "another_issue": {
        "en": "Do you have another issue? (yes/no): ",
        "pa": "ਕੀ ਤੁਹਾਡੀ ਕੋਈ ਹੋਰ ਸਮੱਸਿਆ ਹੈ? (yes/no): ",
        "hi": "क्या आपकी कोई और समस्या है? (yes/no): "
    },
    "goodbye": {
        "en": "Thank you! Goodbye!",
        "pa": "ਧੰਨਵਾਦ! ਸਤ ਸ੍ਰੀ ਅਕਾਲ!",
        "hi": "धन्यवाद! नमस्ते!"
    },
    "enter_choice": {
        "en": "Enter your choice (1-5): ",
        "pa": "ਆਪਣੀ ਚੋਣ ਦਰਜ ਕਰੋ (1-5): ",
        "hi": "अपनी पसंद दर्ज करें (1-5): "
    },
    "processing": {
        "en": "Processing your request...",
        "pa": "ਤੁਹਾਡੀ ਬੇਨਤੀ ਦੀ ਪ੍ਰਕਿਰਿਆ ਕੀਤੀ ਜਾ ਰਹੀ ਹੈ...",
        "hi": "आपकी अनुरोध को प्रोसेस किया जा रहा है..."
    }
}



def translate_to_english(text, lang_code):
    if lang_code == "en":
        return text
    return GoogleTranslator(source=lang_code, target='en').translate(text)


def translate_to_local(text, lang_code):
    if lang_code == "en":
        return text
    return GoogleTranslator(source='en', target=lang_code).translate(text)


def get_input(prompt, lang_code, gtts_code):
    """Get input via voice first, fallback to typing"""
    speak(prompt, gtts_code)
    print(f"\n{prompt}")

    # Try voice first
    result = listen(lang_code)

    # If voice fails, fallback to typing
    if not result:
        result = input("⌨️  Type instead: ").strip()

    return result


def ask_ai(question, topic, lang_code):
    system_prompts = {
        "2": """You are an expert crop advisor for Indian farmers. 
                Give short practical crop advice specific to Indian conditions.
                Keep answer under 100 words.""",
        "3": """You are a market price expert for Indian agricultural products. 
                Give current price ranges and buying/selling tips for Indian farmers.
                Keep answer under 100 words.""",
        "4": """You are an expert on Indian government agricultural schemes. 
                Explain schemes like PM-KISAN, MSP, Fasal Bima Yojana simply.
                Keep answer under 100 words."""
    }

    english_question = translate_to_english(question, lang_code)

    messages = [
        SystemMessage(content=system_prompts.get(topic,
                                                 "You are a helpful agricultural advisor for Indian farmers. Keep answer under 100 words.")),
        HumanMessage(content=english_question)
    ]

    response = llm.invoke(messages)
    return translate_to_local(response.content, lang_code)



def main():
    # Step 1 - Select Language
    print("\n" + "=" * 50)
    print("🌾 KISAN AI AGENT 🌾")
    print("=" * 50)
    print("\nSelect Language / ਭਾਸ਼ਾ ਚੁਣੋ / भाषा चुनें:")
    print("1. English")
    print("2. ਪੰਜਾਬੀ (Punjabi)")
    print("3. हिंदी (Hindi)")

    lang_choice = input("\nEnter 1, 2 or 3: ").strip()
    if lang_choice not in LANGUAGES:
        lang_choice = "1"

    lang = LANGUAGES[lang_choice]
    lang_code = lang["code"]
    gtts_code = lang["gtts"]

    # Welcome
    welcome = TEXT["welcome"][lang_code]
    print(f"\n🌾 {welcome} 🌾")
    speak(welcome, gtts_code)

    # Step 2 - Main Loop
    while True:
        print("\n" + "=" * 50)
        print(TEXT["select_topic"][lang_code])
        print("=" * 50)

        choice = input(TEXT["enter_choice"][lang_code]).strip()

        # Exit
        if choice == "5":
            goodbye = TEXT["goodbye"][lang_code]
            print(f"\n{goodbye}")
            speak(goodbye, gtts_code)
            break

        # Weather
        elif choice == "1":
            city = get_input(TEXT["ask_city"][lang_code], lang_code, gtts_code)
            if not city:
                city = "Ludhiana"
            print(f"\n{TEXT['processing'][lang_code]}")
            weather_data = get_weather(city)
            local_weather = translate_to_local(weather_data, lang_code)
            print(f"\n🌤️  {local_weather}")
            speak(local_weather, gtts_code)

        # Crop, Prices, Schemes
        elif choice in ["2", "3", "4"]:
            question = get_input(TEXT["ask_question"][lang_code], lang_code, gtts_code)
            if question:
                print(f"\n{TEXT['processing'][lang_code]}")
                answer = ask_ai(question, choice, lang_code)
                print(f"\n🌾 {answer}")
                speak(answer, gtts_code)

        else:
            print("❌ Invalid choice, please try again!")
            continue

        # Ask if another issue
        another = get_input(TEXT["another_issue"][lang_code], lang_code, gtts_code)
        if another and any(word in another.lower() for word in ["yes", "y", "ਹਾਂ", "हां", "han", "ha", "haan"]):
            continue
        else:
            goodbye = TEXT["goodbye"][lang_code]
            print(f"\n{goodbye}")
            speak(goodbye, gtts_code)
            break


if __name__ == "__main__":
    main()
