import tempfile
import unittest
from io import StringIO
from pathlib import Path

from tools.demo_video.tts_edge import run_adapter, synthesize_to_file


class FakeCommunicator:
    calls = []

    def __init__(self, text: str, voice: str):
        self.text = text
        self.voice = voice
        self.__class__.calls.append((text, voice))

    async def save(self, output: str) -> None:
        Path(output).write_bytes(b"fake-mp3")


class EdgeTtsAdapterTests(unittest.IsolatedAsyncioTestCase):
    async def test_synthesize_writes_audio_with_requested_voice(self):
        FakeCommunicator.calls.clear()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "speech.raw"

            await synthesize_to_file(
                output,
                "zh-CN-XiaoxiaoNeural",
                "  测试旁白  ",
                communicator_factory=FakeCommunicator,
            )

            self.assertEqual(output.read_bytes(), b"fake-mp3")
            self.assertEqual(
                FakeCommunicator.calls,
                [("测试旁白", "zh-CN-XiaoxiaoNeural")],
            )

    async def test_synthesize_rejects_blank_narration(self):
        FakeCommunicator.calls.clear()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "speech.raw"

            with self.assertRaisesRegex(ValueError, "narration is empty"):
                await synthesize_to_file(
                    output,
                    "zh-CN-XiaoxiaoNeural",
                    "   ",
                    communicator_factory=FakeCommunicator,
                )

            self.assertFalse(output.exists())
            self.assertEqual(FakeCommunicator.calls, [])

    async def test_adapter_reads_engine_contract_from_args_and_stdin(self):
        FakeCommunicator.calls.clear()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "speech.raw"

            exit_code = await run_adapter(
                ["tts_edge.py", str(output), "en-US-AvaNeural"],
                StringIO("A short product demo."),
                communicator_factory=FakeCommunicator,
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(output.read_bytes(), b"fake-mp3")
            self.assertEqual(
                FakeCommunicator.calls,
                [("A short product demo.", "en-US-AvaNeural")],
            )


if __name__ == "__main__":
    unittest.main()
