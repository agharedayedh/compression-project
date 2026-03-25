from __future__ import annotations

from pathlib import Path

import pytest

from compression.storage import compress_file, decompress_file

"""
This file contains tests for file-based compression and decompression.

It checks that:
- files can be compressed and restored correctly
- both small and large inputs work
- compression can actually reduce file size in some cases
"""


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_file_roundtrip_small(tmp_path: Path, algorithm: str) -> None:
    """
    This test checks compression and decompression for a small text file.

    The file is compressed and then decompressed again.
    The restored text should be exactly the same as the original.

    It also includes:
    - symbols
    - emojis
    - non-English characters

    This ensures correct handling of UTF-8 text.
    """
    original = "This is a test. This is a test. 123! 😊 مرحبا\n"
    in_path = tmp_path / "input.txt"
    compressed_path = tmp_path / "compressed.bin"
    out_path = tmp_path / "restored.txt"

    in_path.write_text(original, encoding="utf-8")

    compress_file(in_path, compressed_path, algorithm=algorithm)
    assert compressed_path.exists()
    assert compressed_path.stat().st_size > 0

    decompress_file(compressed_path, out_path)
    assert out_path.exists()

    restored = out_path.read_text(encoding="utf-8")
    assert restored == original


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_file_roundtrip_large_text(tmp_path: Path, algorithm: str) -> None:
    """
    This test checks compression on a larger and more realistic text.

    A paragraph is repeated many times to simulate natural language.
    The goal is to verify that both algorithms still correctly
    restore the original content after compression.

    The test passes if the decompressed file matches the original text.
    """
    paragraph = (
        "Lossless compression means we can recover the exact original text after decoding. "
        "This matters when storing documents, logs, and data that must not change. "
        "In practice, texts contain repetition and skewed character frequencies, "
        "so algorithms like Huffman coding and LZ78 can reduce size while preserving content.\n"
    )
    original = paragraph * 200

    in_path = tmp_path / "input.txt"
    compressed_path = tmp_path / "compressed.bin"
    out_path = tmp_path / "restored.txt"

    in_path.write_text(original, encoding="utf-8")
    compress_file(in_path, compressed_path, algorithm=algorithm)
    decompress_file(compressed_path, out_path)

    restored = out_path.read_text(encoding="utf-8")
    assert restored == original


def test_compression_can_reduce_size_on_repetitive_text(tmp_path: Path) -> None:
    """
    This test checks that compression can actually reduce file size.

    The input is highly repetitive text, which should compress well.

    The test passes if at least one of the algorithms (Huffman or LZ78)
    produces a smaller file than the original.
    """
    original = ("abcabcabcabcabcabcabcabcabc\n" * 2000)

    in_path = tmp_path / "input.txt"
    compressed_path_h = tmp_path / "compressed_huffman.bin"
    compressed_path_lz = tmp_path / "compressed_lz78.bin"

    in_path.write_text(original, encoding="utf-8")
    original_size = in_path.stat().st_size

    compress_file(in_path, compressed_path_h, algorithm="huffman")
    compress_file(in_path, compressed_path_lz, algorithm="lz78")

    assert (
        compressed_path_h.stat().st_size < original_size
        or compressed_path_lz.stat().st_size < original_size
    )
