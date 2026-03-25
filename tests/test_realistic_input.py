from __future__ import annotations

from pathlib import Path

import pytest

from compression.storage import compress_file, decompress_file

@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_realistic_text_file_roundtrip(tmp_path: Path, algorithm: str) -> None:
    """
    Integration-style test using a real natural-language text file.
    """
    source_path = Path(__file__).parent / "data" / "realistic_text.txt"
    if not source_path.exists():
        pytest.skip(
            "Missing tests/data/realistic_text.txt (realistic input file not found).")

    original = source_path.read_text(encoding="utf-8")

    in_path = tmp_path / "input.txt"
    compressed_path = tmp_path / "compressed.bin"
    restored_path = tmp_path / "restored.txt"

    in_path.write_text(original, encoding="utf-8")

    compress_file(in_path, compressed_path, algorithm=algorithm)
    decompress_file(compressed_path, restored_path)

    restored = restored_path.read_text(encoding="utf-8")
    assert restored == original
