#!/usr/bin/env python3
"""Edge TTS adapter used by the product-demo recording engine."""

import asyncio
import sys
from pathlib import Path
from typing import Any, Callable, TextIO


async def synthesize_to_file(
    output: Path,
    voice: str,
    text: str,
    *,
    communicator_factory: Callable[[str, str], Any],
) -> None:
    """Synthesize trimmed text to ``output`` using the requested voice."""

    normalized = text.strip()
    if not normalized:
        raise ValueError("narration is empty")
    communicator = communicator_factory(normalized, voice)
    await communicator.save(str(output))


async def run_adapter(
    argv: list[str],
    stdin: TextIO,
    *,
    communicator_factory: Callable[[str, str], Any],
) -> int:
    """Run the ``output, voice, stdin`` contract expected by make-demo.mjs."""

    if len(argv) != 3:
        raise ValueError("usage: tts_edge.py OUTPUT VOICE")
    output = Path(argv[1])
    output.parent.mkdir(parents=True, exist_ok=True)
    await synthesize_to_file(
        output,
        argv[2],
        stdin.read(),
        communicator_factory=communicator_factory,
    )
    return 0


def _edge_communicator_factory() -> Callable[[str, str], Any]:
    dependency_dir = Path(__file__).with_name("pydeps")
    sys.path.insert(0, str(dependency_dir))
    import edge_tts

    return edge_tts.Communicate


def main() -> int:
    return asyncio.run(
        run_adapter(
            sys.argv,
            sys.stdin,
            communicator_factory=_edge_communicator_factory(),
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
