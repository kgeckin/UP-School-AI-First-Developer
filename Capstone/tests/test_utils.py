"""Mock API interactions so unit tests require no secret or paid requests."""

import json
from types import SimpleNamespace

import pytest

from subtitles import SubtitleSegment
from utils import TRANSLATION_BATCH_SIZE, transcribe_audio, translate_segments


class FakeTranscriptions:
    def __init__(self, response):
        self.response = response
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return self.response


class FakeCompletions:
    def __init__(self, omit_one=False):
        self.calls = []
        self.omit_one = omit_one

    def create(self, **kwargs):
        self.calls.append(kwargs)
        texts = json.loads(kwargs["messages"][1]["content"])
        if self.omit_one:
            texts = texts[:-1]
        content = json.dumps({"translations": [f"translated: {text}" for text in texts]})
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
        )


def fake_client(transcriptions=None, completions=None):
    return SimpleNamespace(
        audio=SimpleNamespace(transcriptions=transcriptions),
        chat=SimpleNamespace(completions=completions),
    )


def test_transcription_uses_whisper_segments(tmp_path):
    audio = tmp_path / "sample.mp3"
    audio.write_bytes(b"placeholder")
    fake_api = FakeTranscriptions(
        SimpleNamespace(
            text="Hello world.",
            language="english",
            segments=[
                SimpleNamespace(start=0.25, end=1.1, text="Hello"),
                SimpleNamespace(start=1.15, end=2.6, text="world."),
            ],
        )
    )
    result = transcribe_audio(audio, client=fake_client(transcriptions=fake_api))

    assert result.language == "english"
    assert result.text == "Hello world."
    assert result.segments[1].start == 1.15
    assert result.segments[1].end == 2.6
    assert fake_api.kwargs["response_format"] == "verbose_json"
    assert fake_api.kwargs["timestamp_granularities"] == ["segment"]


def test_transcription_without_timestamps_fails(tmp_path):
    audio = tmp_path / "sample.mp3"
    audio.write_bytes(b"placeholder")
    api = FakeTranscriptions(
        SimpleNamespace(text="Hello.", language="english", segments=[])
    )
    with pytest.raises(ValueError, match="no timed segments"):
        transcribe_audio(audio, client=fake_client(transcriptions=api))


def test_translation_preserves_timing():
    cues = (
        SubtitleSegment(0.23, 1.75, "Hello"),
        SubtitleSegment(3.75, 6.5, "World"),
    )
    completions = FakeCompletions()
    result = translate_segments(cues, "Turkish", client=fake_client(completions=completions))

    assert len(result) == 2
    assert result[0].start == cues[0].start
    assert result[1].end == cues[1].end
    assert result[0].text == "translated: Hello"
    assert completions.calls[0]["response_format"] == {"type": "json_object"}


def test_translation_is_batched():
    cues = tuple(
        SubtitleSegment(float(i), float(i + 1), f"Line {i}")
        for i in range(TRANSLATION_BATCH_SIZE + 1)
    )
    completions = FakeCompletions()
    result = translate_segments(cues, "French", client=fake_client(completions=completions))

    assert len(completions.calls) == 2
    assert len(result) == len(cues)
    assert result[-1].start == cues[-1].start


def test_translation_rejects_missing_cues():
    cues = (SubtitleSegment(0, 1, "Hello"), SubtitleSegment(2, 3, "World"))
    completions = FakeCompletions(omit_one=True)
    with pytest.raises(ValueError, match="incorrect number"):
        translate_segments(cues, "German", client=fake_client(completions=completions))
