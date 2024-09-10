import ffmpeg
from dotenv import load_dotenv
import os
import openai
import langdetect
import pyttsx3
import sqlite3
import time
from datetime import datetime
import streamlit as st

# .env file load
load_dotenv()

# Get the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def detect_language(text):
    """
    Function to return the detected language
    """
    return langdetect.detect(text)

def text_to_speech(text, output_audio):
    """
    Function to convert text to speech
    """
    engine = pyttsx3.init()
    engine.save_to_file(text, output_audio)
    engine.runAndWait()

def video_to_audio(video_path, output_audio_path):
    """
    Converts video to audio without asking for overwrite confirmation.
    """
    stream = ffmpeg.input(video_path)
    stream = ffmpeg.output(stream, output_audio_path)

    # Add the '-y' flag to force overwrite without confirmation
    ffmpeg.run(stream, overwrite_output=True)

def transcribe_audio(audio_path):
    """
    Function to transcribe audio to text (OpenAI Whisper)
    """
    with open(audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

def translate_text(text, target_language):
    """
    Function to translate text into the specified target language (OpenAI ChatCompletion - GPT-4)
    """
    messages = [
        {"role": "system", "content": f"Translate the following text to {target_language}:"},
        {"role": "user", "content": text}
    ]

    # Send chat completion request using the GPT-4 model
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1500
    )

    return response['choices'][0]['message']['content'].strip()

def generate_srt_file(translated_text, language_code):
    """
    Function to generate .srt file from translated text
    """
    srt_content = ''
    lines = translated_text.splitlines()
    for i, line in enumerate(lines):
        srt_content += f"{i + 1}\n00:00:0{i},000 --> 00:00:0{i + 2},000\n{line}\n\n"

    file_name = f"{language_code}_translation.srt"
    with open(file_name, "w") as f:
        f.write(srt_content)
    return file_name

def create_database():
    """
    Function to create a database
    """
    conn = sqlite3.connect('translations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS translations
                 (id INTEGER PRIMARY KEY, original_text TEXT, translated_text TEXT, language TEXT, timestamp TEXT)''')
    conn.commit()
    return conn, c

def save_translation_to_db(conn, c, transcript, translations):
    """
    Function to save translation results to the database
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Capture the current date and time
    for language, translation in translations.items():
        c.execute("INSERT INTO translations (original_text, translated_text, language, timestamp) VALUES (?, ?, ?, ?)",
                  (transcript, translation, language, timestamp))
        conn.commit()

def load_translations_from_db(c):
    """
    Function to fetch past translations from the database
    """
    c.execute("SELECT * FROM translations")
    return c.fetchall()

def process_translation_progress(step, total_steps):
    """
    Function to simulate the translation process with a progress bar
    """
    translation_progress = st.progress(0)
    for i in range(step, total_steps):
        time.sleep(0.1)
        translation_progress.progress((i + 1) * (100 // total_steps))

def process_video_audio(video_path, output_audio_path):
    """
    Function to process video to audio conversion without a progress bar
    """
    st.write("1. Converting video to audio (ffmpeg)")
    video_to_audio(video_path, output_audio_path)  # Directly call the conversion function
