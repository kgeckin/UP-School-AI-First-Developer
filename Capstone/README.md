<div align="center">

<img src="assets/LOGO.png" alt="LinguaX logo" width="140" />

# LinguaX

**AI assisted transcription, translation and timestamped subtitles**

An educational Streamlit application that turns video and audio files into subtitles while preserving the actual timing reported by Whisper.

</div>

## What it does

1. Extracts mono audio from uploaded media with FFmpeg.
2. Requests a Whisper transcription with **segment timestamps**.
3. Optionally translates each timed subtitle segment using a language model.
4. Exports valid SubRip subtitles and a ZIP archive for multiple files.

No fabricated timestamps and no automatic database history. Uploaded files are processed in a temporary directory and removed when processing finishes. Transcript results are retained only in the active Streamlit session.

## Quick start

**Prerequisites:** Python 3.11 or newer, FFmpeg installed on your system, and an OpenAI API key with available credits.

From the repository root:

```bash
cd Capstone
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then replace the placeholder value for `OPENAI_API_KEY`. Never commit your actual key.

```bash
streamlit run src/app.py
```

Open the local address provided by Streamlit, upload one or more media files, and optionally select translation languages.

**FFmpeg check:** Run `ffmpeg -version` in the same terminal. The Python package `ffmpeg-python` does not install the FFmpeg executable.

## Project layout

```text
Capstone/
├── .env.example
├── .gitignore
├── .streamlit/
│   └── config.toml
├── assets/
│   └── LOGO.png
├── Data/                 # Original educational video demos
├── docs/
│   └── ARCHITECTURE.md
├── src/
│   ├── app.py            # Streamlit interface
│   ├── utils.py          # FFmpeg and OpenAI integrations
│   └── subtitles.py      # Pure SubRip formatting and validation
├── tests/
│   ├── conftest.py
│   ├── test_subtitles.py
│   └── test_utils.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q tests
```

The tests use mocked API responses and do not require an OpenAI key or send paid requests.

## Limitations and privacy

- Uploads are sent to an external AI provider for processing. Do not upload confidential, regulated, or third-party material without authorization.
- The transcription service has a request size limit. LinguaX checks the extracted MP3 against a 24 MB local cap. It does not yet implement automatic audio splitting.
- Translated text keeps Whisper's **source segment boundaries**. This preserves the timing structure but does not perform independent alignment for longer translations.
- Translation quality, transcription accuracy, model availability, and API costs depend on the provider and input.
- Processing is synchronous. Short clips are recommended for this educational prototype.
- LinguaX does not persist a translation history. Older versions used a local SQLite history file, which is no longer created.

## Engineering notes

See [the architecture and design decisions](docs/ARCHITECTURE.md) for the processing pipeline, external dependencies, tradeoffs, and known extensions.

## Background

Developed as a capstone for the AI First Developer educational program. This repository also contains other assignments and learning exercises. This codebase is a portfolio prototype and has not been independently verified as production ready.

[Original presentation](https://www.canva.com/design/DAGQZMDAeEI/mwx65uoRkltHCMQhDoTUWg/view)

## License

This repository includes an [MIT license](../LICENSE). Review that license for reuse conditions.
