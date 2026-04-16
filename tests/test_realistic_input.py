from __future__ import annotations

from pathlib import Path

import pytest

from compression.storage import compress_file, decompress_file


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_realistic_text_file_roundtrip(tmp_path: Path, algorithm: str) -> None:
    """
    Integration test using a realistic natural-language text file.

    This test verifies the full file-based pipeline:
    - read input text file
    - compress it using the selected algorithm
    - decompress the result
    - compare with the original text

    The test is executed for both Huffman and LZ78.
    """
    # Path to realistic input file used for testing
    source_path = Path(__file__).parent / "data" / "realistic_text.txt"

    # Skip test if the file is missing
    if not source_path.exists():
        pytest.skip(
            "Missing tests/data/realistic_text.txt (realistic input file not found)."
        )

    original = source_path.read_text(encoding="utf-8")

    # Temporary files used during the test
    in_path = tmp_path / "input.txt"
    compressed_path = tmp_path / "compressed.bin"
    restored_path = tmp_path / "restored.txt"

    # Write original input
    in_path.write_text(original, encoding="utf-8")

    # Run compression and decompression pipeline
    compress_file(in_path, compressed_path, algorithm=algorithm)
    decompress_file(compressed_path, restored_path)

    # Read result and verify correctness
    restored = restored_path.read_text(encoding="utf-8")
    assert restored == original
