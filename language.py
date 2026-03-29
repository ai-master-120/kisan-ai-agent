from deep_translator import GoogleTranslator


def translate_to_english(text, source_lang):
    """Convert farmer's language to English for the AI"""
    if source_lang == "english":
        return text
    return GoogleTranslator(source=source_lang, target='english').translate(text)


def translate_to_local(text, target_lang):
    """Convert AI's English answer back to farmer's language"""
    if target_lang == "english":
        return text
    return GoogleTranslator(source='english', target=target_lang).translate(text)


def get_language_choice():
    """Ask farmer to pick their language"""
    print("\n🌾 Welcome to Kisan AI Agent 🌾")
    print("Please select your language / ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ / अपनी भाषा चुनें")
    print("1. English")
    print("2. ਪੰਜਾਬੀ (Punjabi)")
    print("3. हिंदी (Hindi)")

    choice = input("\nEnter 1, 2 or 3: ")

    if choice == "1":
        return "english", "Hello! How can I help you today?"
    elif choice == "2":
        return "pa", "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡੀ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ?"
    elif choice == "3":
        return "hi", "नमस्ते! मैं आपकी कैसे मदद कर सकता हूं?"
    else:
        return "english", "Hello! How can I help you today?"