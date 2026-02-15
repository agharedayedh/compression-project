from __future__ import annotations

from pathlib import Path

import pytest

from compression.main import compress_file, decompress_file


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_realistic_text_file_roundtrip(tmp_path: Path, algorithm: str) -> None:
    # Read realistic natural-language input from a real file in data/.
    source_path = Path(__file__).parent / "data" / "realistic_text.txt"
    original = source_path.read_text(encoding="utf-8")

    in_path = tmp_path / "input.txt"
    compressed_path = tmp_path / "compressed.bin"
    restored_path = tmp_path / "restored.txt"

    in_path.write_text(original, encoding="utf-8")

    # type: ignore[arg-type]
    compress_file(in_path, compressed_path, algorithm=algorithm)
    decompress_file(compressed_path, restored_path)

    restored = restored_path.read_text(encoding="utf-8")
    assert restored == original
