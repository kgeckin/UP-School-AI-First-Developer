"""Tests for SubRip timing and formatting; no external API calls."""

import pytest

from subtitles import SubtitleSegment, build_srt, srt_timestamp


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0, "00:00:00,000"),
        (1.234, "00:00:01,234"),
        (61.9, "00:01:01,900"),
        (3600.001, "01:00:00,001"),
        (3661.999, "01:01:01,999"),
    ],
)
def test_srt_timestamp(seconds, expected):
    assert srt_timestamp(seconds) == expected


@pytest.mark.parametrize("bad_value", [-1, float("inf"), float("nan")])
def test_invalid_timestamp(bad_value):
    with pytest.raises(ValueError):
        srt_timestamp(bad_value)


def test_build_srt_uses_original_timestamps():
    cues = [
        SubtitleSegment(0.15, 1.8, "Hello!"),
        SubtitleSegment(5.5, 7.375, "  How are you?  "),
    ]
    assert build_srt(cues) == (
        "1\n00:00:00,150 --> 00:00:01,800\nHello!\n\n"
        "2\n00:00:05,500 --> 00:00:07,375\nHow are you?\n"
    )


def test_missing_segments_rejected():
    with pytest.raises(ValueError, match="no timed segments"):
        build_srt([])


def test_reverse_order_rejected():
    with pytest.raises(ValueError, match="ordered"):
        build_srt(
            [SubtitleSegment(4, 5, "Later"), SubtitleSegment(1, 2, "Earlier")]
        )


def test_invalid_cues_rejected():
    for start, end, text in [(1, 1, "Same"), (-1, 2, "Negative"), (0, 2, "")]:
        with pytest.raises(ValueError):
            SubtitleSegment(start, end, text)
