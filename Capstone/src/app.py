"""Streamlit interface for LinguaX."""

from __future__ import annotations

import os
import tempfile
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import streamlit as st

from subtitles import build_srt
from utils import api_client, extract_audio, transcribe_audio, translate_segments


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOGO = PROJECT_ROOT / "assets" / "LOGO.png"
SUPPORTED_TYPES = ["mp3", "mp4", "avi", "mov", "m4v", "m4a", "wav", "webm"]
LANGUAGES = {
    "Turkish": "tr",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Dutch": "nl",
}


def create_bundle(results: list[dict]) -> bytes:
    """Bundle subtitles using generated names only, never an uploaded filename."""
    output = BytesIO()
    with ZipFile(output, mode="w", compression=ZIP_DEFLATED) as archive:
        for item in results:
            directory = f"video_{item['index']:02d}"
            archive.writestr(f"{directory}/original.srt", item["original_srt"])
            for language, srt_content in item["translations"].items():
                archive.writestr(
                    f"{directory}/{LANGUAGES[language]}.srt",
                    srt_content,
                )
    return output.getvalue()


def main() -> None:
    st.set_page_config(
        page_title="LinguaX | Video subtitles",
        page_icon="🎬",
        layout="wide",
    )

    if LOGO.is_file():
        st.image(str(LOGO), width=136)
    st.title("LinguaX")
    st.caption("Transcribe once. Translate into multiple languages. Keep the real timing.")

    st.info(
        "Videos are processed in a temporary folder and removed after processing. "
        "Audio and subtitle text are sent to an external AI API for transcription "
        "and translation. Results remain in this browser session until cleared."
    )

    with st.form("conversion", clear_on_submit=False):
        uploads = st.file_uploader(
            "Video or audio files",
            type=SUPPORTED_TYPES,
            accept_multiple_files=True,
            help="Upload short clips. A large recording may exceed the transcription API size limit.",
        )
        targets = st.multiselect(
            "Translate to (optional)",
            options=list(LANGUAGES),
            default=[],
        )
        submitted = st.form_submit_button(
            "Create subtitles", type="primary", use_container_width=True
        )

    if submitted:
        if not uploads:
            st.warning("Choose at least one video or audio file.")
        elif not os.getenv("OPENAI_API_KEY"):
            st.error("Add OPENAI_API_KEY to the environment or Capstone/.env.")
        else:
            st.session_state["linguax_results"] = []
            progress = st.progress(0)
            client = api_client()

            for index, upload in enumerate(uploads, start=1):
                try:
                    with tempfile.TemporaryDirectory(prefix="linguax_") as temp:
                        folder = Path(temp)
                        suffix = Path(upload.name).suffix.lower()
                        if suffix not in {f".{item}" for item in SUPPORTED_TYPES}:
                            raise ValueError("Unsupported file extension.")

                        # Uploaded names are never used for local filesystem paths.
                        source = folder / f"input{suffix}"
                        audio = folder / "audio.mp3"
                        source.write_bytes(upload.getvalue())

                        with st.spinner(f"Processing {index}/{len(uploads)}: {upload.name}"):
                            extract_audio(source, audio)
                            transcript = transcribe_audio(audio, client=client)
                            original_srt = build_srt(transcript.segments)

                            translations: dict[str, str] = {}
                            for language in targets:
                                if transcript.language.casefold() in {
                                    language.casefold(),
                                    LANGUAGES[language].casefold(),
                                }:
                                    continue
                                translated_cues = translate_segments(
                                    transcript.segments, language, client=client
                                )
                                translations[language] = build_srt(translated_cues)

                            st.session_state["linguax_results"].append(
                                {
                                    "index": index,
                                    "name": upload.name,
                                    "language": transcript.language,
                                    "original_srt": original_srt,
                                    "text": transcript.text,
                                    "translations": translations,
                                }
                            )
                except (ValueError, RuntimeError) as exc:
                    st.error(f"Could not process {upload.name}: {exc}")
                except Exception:
                    st.error(
                        f"Could not process {upload.name}. Check the API credentials, "
                        "available quota, and supported media format."
                    )
                finally:
                    progress.progress(index / len(uploads))

            if st.session_state["linguax_results"]:
                st.success("Subtitle generation completed for the files shown below.")

    results = st.session_state.get("linguax_results", [])
    if not results:
        return

    st.divider()
    st.subheader("Your subtitles")
    for item in results:
        with st.expander(f"{item['name']} · Detected: {item['language']}", expanded=True):
            st.text_area(
                "Transcription",
                value=item["text"],
                height=135,
                key=f"transcription_{item['index']}",
            )
            st.download_button(
                "Download original subtitles",
                data=item["original_srt"],
                file_name=f"video_{item['index']:02d}_original.srt",
                mime="application/x-subrip",
                key=f"download_original_{item['index']}",
            )

            for language, content in item["translations"].items():
                with st.expander(f"{language} subtitles"):
                    st.download_button(
                        f"Download {language}",
                        data=content,
                        file_name=f"video_{item['index']:02d}_{LANGUAGES[language]}.srt",
                        mime="application/x-subrip",
                        key=f"download_{item['index']}_{LANGUAGES[language]}",
                    )

    st.download_button(
        "Download all subtitles as ZIP",
        data=create_bundle(results),
        file_name="linguax_subtitles.zip",
        mime="application/zip",
        type="primary",
    )
    if st.button("Clear session results"):
        st.session_state.pop("linguax_results", None)
        st.rerun()


if __name__ == "__main__":
    main()
