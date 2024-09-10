import os
import streamlit as st
import base64
from utils import (create_database, process_video_audio, transcribe_audio,
                   generate_srt_file, detect_language, translate_text,
                   save_translation_to_db, load_translations_from_db)

# Theme selection
theme = st.sidebar.selectbox("Theme Selection", ["Light", "Dark"], index=0)

# Apply CSS for theme switching
if theme == "Light":
    st.markdown("""
        <style>
        body {
            background-color: white;
            color: black;
        }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body {
            background-color: #2e2e2e;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

# CSS for aligning the content in the center and styling title and subtitle
st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
    }
    .subheader {
        text-align: center;
        font-size: 16px;
        color: grey;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Collapsible section for previous translations
conn, c = create_database()

with st.sidebar:
    st.subheader("Past Translations")
    translations_data = load_translations_from_db(c)
    if translations_data:
        for idx, row in enumerate(translations_data):
            # Use expander to show translation details when clicked
            with st.expander(f"Translation #{idx + 1} - {row[3]} - {row[4]}"):
                st.text_area(f"{row[3]} Translation", row[2], key=f"text_area_{idx}")

# Dynamic path for project directory
image_path = os.path.join(os.getcwd(), "LOGO.png")
st.markdown(
    f'<div class="center"><img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" width="200"></div>',
    unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="title">LinguaX</h1>', unsafe_allow_html=True)

# Subtitle
st.markdown(
    '<h3 class="subheader">Effortlessly transcribe and translate your videos into multiple languages with AI-powered precision.</h3>',
    unsafe_allow_html=True)

# Step 1: Video Upload
uploaded_files = st.file_uploader("Upload Your Video Files", type=["mp4", "avi", "mov", "m4v", "m2a", "mpeg4", "m4a"],
                                  accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        video_path = f"uploaded_video_{uploaded_file.name}"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Step 2: Convert video to audio
        audio_path = "output_audio.mp3"
        process_video_audio(video_path, audio_path)

        # Audio preview
        audio_bytes = open(audio_path, 'rb').read()
        st.audio(audio_bytes, format='audio/mp3')

        # Step 3: Transcribe the audio to text
        st.write("2. Transcribing audio to text (OpenAI Whisper)")
        transcript = transcribe_audio(audio_path)
        st.text_area("Transcription", transcript)

        # Make the transcription downloadable
        srt_file = generate_srt_file(transcript, "tr")
        st.download_button("Download Transcription (.srt)", data=open(srt_file).read(), file_name="transcript_tr.srt")

        # Step 4: Ask the user for which languages to translate the transcription into
        detected_lang = detect_language(transcript)
        st.info(f"Detected language: {detected_lang}. Please select the languages you want to translate to.")

        # Provide a multi-select widget for language choices
        languages_available = {
            "Turkish": "tr", "English": "en", "French": "fr", "German": "de",
            "Spanish": "es", "Italian": "it", "Portuguese": "pt", "Russian": "ru",
            "Dutch": "nl",
        }

        selected_languages = st.multiselect(
            "Select the languages you want to translate the transcription into:",
            options=list(languages_available.keys()),
        )

        # Button to start the translation process
        if st.button("Start Translation"):
            # Step 5: Display the progress bar and start translation
            st.write("Translating... Please wait.")
            progress_bar = st.progress(0)
            translations = {}
            total_languages = len(selected_languages)

            for idx, language in enumerate(selected_languages):
                lang_code = languages_available[language]

                if lang_code == detected_lang:
                    st.warning(f"The transcript is already in {language}, skipping translation.")
                    continue  # Skip if the detected language is the same as the selected language

                # Perform the translation
                translation = translate_text(transcript, language)
                translations[language] = translation

                # Update the progress bar
                progress_bar.progress((idx + 1) / total_languages)

            # Hide progress bar and show results
            st.write("Translation complete!")

            # Step 6: Show translations and download buttons
            for language in selected_languages:
                translation = translations.get(language)
                if translation:
                    st.text_area(f"{language} Translation", translation)

                    # Make the translation downloadable
                    lang_code = languages_available[language]
                    srt_file = generate_srt_file(translation, lang_code)
                    st.download_button(f"Download {language} Translation", data=open(srt_file).read(),
                                       file_name=f"{lang_code}_translation.srt")

            # Save translations to the database
            save_translation_to_db(conn, c, transcript, translations)