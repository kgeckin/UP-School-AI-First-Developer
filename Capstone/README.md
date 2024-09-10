# LinguaX: AI-Powered Video Translation and Transcription

<p align="center">
  <img src="https://github.com/kgeckin/UP-School-AI-First-Developer/blob/1e1a84ec306c5ac27dec84f7a770c760d5e0f375/Capstone/assets/LOGO.png" alt="LinguaX Logo" width="200"/>
</p>

## Introduction

**LinguaX** is an AI-powered application that transcribes and translates video files into multiple languages with precision. It leverages OpenAI's Whisper for transcription and GPT-4 for accurate translations, providing users with downloadable `.srt` subtitle files in their chosen languages.

## Features

- **Video Upload**: Supports multiple video formats such as MP4, AVI, MOV, and more.
- **Audio Extraction**: Automatically extracts audio from uploaded videos using ffmpeg.
- **AI-Powered Transcription**: Converts extracted audio into text using OpenAI Whisper.
- **Multi-Language Translation**: Translates transcriptions into various languages, including Turkish, English, French, Spanish, and more, with the power of GPT-4.
- **Subtitle Generation**: Automatically generates `.srt` files for each language and allows users to download them.

## Installation

1. Clone the repository:
   ```
   https://github.com/kgeckin/UP-School-AI-First-Developer.git
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Use

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
2. Upload a video file in the supported formats.
3. Select the languages you want to translate the transcription into.
4. Download the transcriptions and translations as `.srt` files.

## Project Structure

```
Capstone/
│
├── src/                   
│   ├── app.py             
│   └── utils.py          
│
├── assets/                
│   ├── LOGO.png          
│
├── data/                 
│   ├── LinguaX_Demo.mp4   
│   ├── Presentation.pptx  
│
├── requirements.txt       
├── .gitignore            
└── README.md              

```

## About Me

I am Kardellen Geçkin, a passionate AI enthusiast and cybersecurity professional. I have a strong background in AI, machine learning, and natural language processing. Through my journey, I have worked on multiple projects combining AI with cybersecurity and video translation, with a keen interest in NLP technologies.

## License

This project is licensed under the MIT License.

## Presentation

For further details about the project, you can access the presentation [here](https://www.canva.com/design/DAGQZMDAeEI/mwx65uoRkltHCMQhDoTUWg/view?utm_content=DAGQZMDAeEI&utm_campaign=share_your_design&utm_medium=link&utm_source=shareyourdesignpanel).
