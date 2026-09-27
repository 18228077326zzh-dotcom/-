import json
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPOSITORY_ROOT / "tools" / "demo_video" / "make_subtitles.py"


def write_silent_wav(path: Path, seconds: float) -> None:
    sample_rate = 8_000
    frame_count = round(sample_rate * seconds)
    with wave.open(str(path), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(sample_rate)
        audio.writeframes(b"\x00\x00" * frame_count)


class SubtitleGeneratorTests(unittest.TestCase):
    def test_cli_uses_real_segment_durations_for_srt_timing(self):
        with tempfile.TemporaryDirectory() as directory:
            workdir = Path(directory)
            flow = workdir / "flow.json"
            output = workdir / "demo.srt"
            flow.write_text(
                json.dumps(
                    {
                        "steps": [
                            {"narr": "First line"},
                            {"narr": "Second line"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            write_silent_wav(workdir / "seg0.wav", 1.0)
            write_silent_wav(workdir / "seg1.wav", 1.5)

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(flow), str(workdir), str(output)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                output.read_text(encoding="utf-8"),
                "1\n"
                "00:00:00,800 --> 00:00:01,400\n"
                "First line\n\n"
                "2\n"
                "00:00:01,800 --> 00:00:02,900\n"
                "Second line\n",
            )


if __name__ == "__main__":
    unittest.main()
