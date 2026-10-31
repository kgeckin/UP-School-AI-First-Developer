"""Subtitle primitives shared by transcription, translation and tests.

These utilities do not depend on Streamlit, FFmpeg or an API client.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True, slots=True)
class SubtitleSegment:
    start: float
    end: float
    text: str

    def __post_init__(self) -> None:
        if not isfinite(self.start) or not isfinite(self.end):
            raise ValueError("Cue timestamps must be finite.")
        if self.start < 0 or self.end <= self.start:
            raise ValueError("A cue must start at or after zero and end after its start.")
        if not self.text.strip():
            raise ValueError("A subtitle cue cannot be empty.")


def srt_timestamp(seconds: float) -> str:
    """Format an elapsed time as HH:MM:SS,mmm."""
    if not isfinite(seconds) or seconds < 0:
        raise ValueError("Timestamp must be a finite, nonnegative number.")

    milliseconds = round(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def build_srt(segments: Iterable[SubtitleSegment]) -> str:
    """Serialize genuine timed segments into SubRip format."""
    cues = list(segments)
    if not cues:
        raise ValueError("There are no timed segments to export.")

    blocks: list[str] = []
    last_start = -1.0
    for index, segment in enumerate(cues, start=1):
        if segment.start < last_start:
            raise ValueError("Segments must be ordered by start time.")
        last_start = segment.start
        # Normalize line breaks but keep multi-line subtitles readable.
        text = "\n".join(line.strip() for line in segment.text.splitlines() if line.strip())
        blocks.append(
            f"{index}\n"
            f"{srt_timestamp(segment.start)} --> {srt_timestamp(segment.end)}\n"
            f"{text}"
        )

    return "\n\n".join(blocks) + "\n"
