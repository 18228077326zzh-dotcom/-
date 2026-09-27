#!/usr/bin/env python3
"""Generate SRT captions from a demo flow and its rendered WAV segments."""

import argparse
import json
import wave
from pathlib import Path


def format_timestamp(seconds: float) -> str:
    total_milliseconds = round(seconds * 1_000)
    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds_part, milliseconds = divmod(remainder, 1_000)
    return f"{hours:02d}:{minutes:02d}:{seconds_part:02d},{milliseconds:03d}"


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / audio.getframerate()


def build_srt(
    narrations: list[str],
    durations: list[float],
    *,
    lead_seconds: float = 0.8,
    tail_padding: float = 0.4,
) -> str:
    cursor = lead_seconds
    blocks: list[str] = []
    for narration, duration in zip(narrations, durations, strict=True):
        visible_duration = max(duration - tail_padding, 0.001)
        blocks.append(
            "\n".join(
                [
                    str(len(blocks) + 1),
                    f"{format_timestamp(cursor)} --> "
                    f"{format_timestamp(cursor + visible_duration)}",
                    narration.strip(),
                ]
            )
        )
        cursor += duration
    return "\n\n".join(blocks) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("flow", type=Path)
    parser.add_argument("segments", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    flow = json.loads(args.flow.read_text(encoding="utf-8"))
    narrations = [step.get("narr", "") for step in flow["steps"]]
    durations = [
        wav_duration(args.segments / f"seg{index}.wav")
        for index in range(len(narrations))
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_srt(narrations, durations), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
