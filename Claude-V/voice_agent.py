"""
Voice Agent — converts regulatory text to speech in multiple Indian languages.
Uses gTTS (Google Text-to-Speech) as primary; falls back to placeholder if unavailable.
"""
import io
import base64
import os

LANGUAGE_MAP = {
    "English":   ("en", "en"),
    "Hindi":     ("hi", "hi"),
    "Tamil":     ("ta", "ta"),
    "Telugu":    ("te", "te"),
    "Bengali":   ("bn", "bn"),
    "Marathi":   ("mr", "mr"),
    "Gujarati":  ("gu", "gu"),
    "Kannada":   ("kn", "kn"),
    "Malayalam": ("ml", "ml"),
    "Punjabi":   ("pa", "pa"),
}

# Translated summaries for common regulations (demonstration)
TRANSLATIONS = {
    "hi": {
        "intro": "नमस्ते! मैं आपका नियामक सहायक हूं। मैं आपको इस विनियमन के बारे में हिंदी में समझाऊंगा।",
        "brief": "यह विनियमन महत्वपूर्ण है। इसका पालन करना अनिवार्य है। कृपया अपनी कंपनी की नीतियों की समीक्षा करें।",
        "action": "आवश्यक कार्रवाई: अपनी अनुपालन टीम से परामर्श करें और 90 दिनों के भीतर नीतियां अपडेट करें।"
    },
    "ta": {
        "intro": "வணக்கம்! நான் உங்கள் ஒழுங்குமுறை உதவியாளர். இந்த விதிமுறை பற்றி தமிழில் விளக்குகிறேன்.",
        "brief": "இந்த விதிமுறை மிக முக்கியமானது. இதை பின்பற்றுவது கட்டாயம்.",
        "action": "செய்ய வேண்டியவை: உங்கள் இணக்க குழுவை கலந்தாலோசித்து 90 நாட்களுக்குள் கொள்கைகளை புதுப்பிக்கவும்."
    },
    "te": {
        "intro": "నమస్కారం! నేను మీ నియంత్రణ సహాయకుడిని. ఈ నిబంధన గురించి తెలుగులో వివరిస్తాను.",
        "brief": "ఈ నిబంధన చాలా ముఖ్యమైనది. దీనిని అనుసరించడం తప్పనిసరి.",
        "action": "చర్యలు: మీ కంప్లయెన్స్ బృందాన్ని సంప్రదించి 90 రోజులలోపు విధానాలను నవీకరించండి."
    },
    "bn": {
        "intro": "নমস্কার! আমি আপনার নিয়ন্ত্রক সহায়ক। এই বিধিমালা সম্পর্কে বাংলায় ব্যাখ্যা করব।",
        "brief": "এই বিধিমালা অত্যন্ত গুরুত্বপূর্ণ। এটি অনুসরণ করা বাধ্যতামূলক।",
        "action": "করণীয়: আপনার কমপ্লায়েন্স দলের সাথে পরামর্শ করুন এবং ৯০ দিনের মধ্যে নীতিমালা আপডেট করুন।"
    },
    "mr": {
        "intro": "नमस्कार! मी आपला नियामक सहाय्यक आहे. या नियमनाबद्दल मराठीत स्पष्ट करतो.",
        "brief": "हे नियमन अत्यंत महत्त्वाचे आहे. त्याचे पालन करणे अनिवार्य आहे.",
        "action": "आवश्यक कृती: अनुपालन संघाशी सल्लामसलत करा आणि ९० दिवसांत धोरणे अद्ययावत करा."
    },
    "gu": {
        "intro": "નમસ્તે! હું તમારો નિયમન સહાયક છું. આ નિયમન વિષે ગુજરાતીમાં સમજાવીશ.",
        "brief": "આ નિયમન ખૂબ મહત્વનું છે. તેનું પાલન ફરજિયાત છે.",
        "action": "જરૂરી પગલાં: અનુપાલન ટીમ સાથે પરામર્શ કરો અને 90 દિવસમાં નીતિઓ અપડેટ કરો."
    },
    "kn": {
        "intro": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ನಿಯಂತ್ರಕ ಸಹಾಯಕ. ಈ ನಿಯಮದ ಬಗ್ಗೆ ಕನ್ನಡದಲ್ಲಿ ವಿವರಿಸುತ್ತೇನೆ.",
        "brief": "ಈ ನಿಯಮ ತುಂಬಾ ಮುಖ್ಯವಾಗಿದೆ. ಇದನ್ನು ಅನುಸರಿಸುವುದು ಕಡ್ಡಾಯ.",
        "action": "ಕ್ರಮಗಳು: ಅನುಸರಣಾ ತಂಡವನ್ನು ಸಂಪರ್ಕಿಸಿ ಮತ್ತು 90 ದಿನಗಳಲ್ಲಿ ನೀತಿಗಳನ್ನು ನವೀಕರಿಸಿ."
    },
    "en": {
        "intro": "Hello! I am your RegIntel regulatory assistant. Let me explain this regulation to you in simple terms.",
        "brief": "This regulation is important and compliance is mandatory.",
        "action": "Action required: Consult your compliance team and update policies within the specified deadline."
    }
}


def get_language_options():
    """Return list of supported language names."""
    return list(LANGUAGE_MAP.keys())


def _build_explanation(reg_text: str, lang_code: str, detail_level: str) -> str:
    """Build a translated explanation for the regulation."""
    lang_data = TRANSLATIONS.get(lang_code, TRANSLATIONS["en"])
    base = f"{lang_data['intro']} {lang_data['brief']}"

    if detail_level == "Key Action Points":
        return f"{base} {lang_data['action']}"
    elif detail_level == "Detailed Explanation":
        return (
            f"{lang_data['intro']} "
            f"The regulation states the following: {reg_text[:300]}. "
            f"{lang_data['brief']} {lang_data['action']}"
        )
    else:  # Brief Summary
        return base


def text_to_speech_base64(text: str, language: str, detail_level: str = "Brief Summary"):
    """
    Convert text to speech audio in the specified language.
    Returns (base64_encoded_mp3, transcript).
    """
    lang_code, gtts_lang = LANGUAGE_MAP.get(language, ("en", "en"))
    transcript = _build_explanation(text, lang_code, detail_level)

    try:
        from gtts import gTTS
        tts = gTTS(text=transcript, lang=gtts_lang, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_b64 = base64.b64encode(audio_buffer.read()).decode("utf-8")
        return audio_b64, transcript
    except ImportError:
        print("[VoiceAgent] gTTS not installed. Install with: pip install gTTS")
        return _silent_audio_b64(), transcript
    except Exception as e:
        print(f"[VoiceAgent] TTS error: {e}")
        return _silent_audio_b64(), transcript


def _silent_audio_b64() -> str:
    """
    Return a minimal valid MP3 (silent) as base64 fallback.
    This is a 1-second silent MP3 header.
    """
    # Minimal valid MP3 bytes (silent frame) base64
    silent_mp3 = (
        "//uQxAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAAAEAAABIADAwMDAwMDAwMDAwMDAwMDAwMDA"
        "wMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAAAAAAAAAAAAAAAAAAAAAAAAA"
    )
    return silent_mp3
