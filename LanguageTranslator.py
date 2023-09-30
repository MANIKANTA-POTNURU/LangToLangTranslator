import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import tempfile
import IPython.display as ipd
import time

# Define dictionaries mapping language codes to full names for source and target languages
language_names = {
    "en": "English",
    "te": "Telugu",
    "fr": "French",
    "es": "Spanish",
    "bo": "Tibetan",
    "de": "German",
    "ja": "Japanese",
    "ko": "Korean",
    "zh-CN": "Simplified Chinese",
    "ru": "Russian",
    "ar": "Arabic",
    # Add more languages as needed
}

def recognize_speech(target_language):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info(f"Please start speaking in {language_names[target_language]}...")
        audio = recognizer.listen(source)
        # st.success("Speech captured! Translating...")

    try:
        text = recognizer.recognize_google(audio, language=target_language)
        return text
    # except sr.UnknownValueError:
    #     #st.warning("Could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"Speech recognition request failed: {str(e)}")

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def text_to_speech(text, target_language):
    tts = gTTS(text, lang=target_language)
    
    # Create a temporary file to save the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        return temp_audio.name

st.title("Voice Translator App")

# Use st.session_state to maintain the selected source language and recognized speech
if 'source_language_code' not in st.session_state:
    st.session_state.source_language_code = "en"
    st.session_state.recognized_text = ""

# Step 1: Select the source language to speak in
source_language_code = st.selectbox("Select the source language to speak in:", list(language_names.keys()), format_func=lambda x: language_names[x], key="source_language")

# Step 2: Start recording
if st.button("Start Recording"):
    text = recognize_speech(source_language_code)
    
    if text:
        st.session_state.recognized_text = text

        # Add a delay before showing the target language selection
        time.sleep(2)  # Adjust the delay time as needed

# Display the recognized text
if st.session_state.recognized_text:
    st.subheader("Speech Recognition Result:")
    st.write(st.session_state.recognized_text)

    # Step 3: Select the target language for translation
    target_language_code = st.selectbox("Select the target language for translation:", list(language_names.keys()), format_func=lambda x: language_names[x], key="target_language")

    # Step 4: Translate the recognized text
    translation = translate_text(st.session_state.recognized_text, target_language_code)
    st.subheader("Translation:")
    st.write(translation)

    # Step 5: Convert translation to speech and play it
    audio_path = text_to_speech(translation, target_language_code)
    st.audio(open(audio_path, 'rb').read(), format="audio/mp3")