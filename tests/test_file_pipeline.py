from __future__ import annotations

from pathlib import Path

import pytest

from compression.main import compress_file, decompress_file


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_file_roundtrip_small(tmp_path: Path, algorithm: str) -> None:
    original = "This is a test. This is a test. 123! 😊 مرحبا\n"
    in_path = tmp_path / "input.txt"
    compressed_path = tmp_path / "compressed.bin"
    out_path = tmp_path / "restored.txt"

    in_path.write_text(original, encoding="utf-8")

    # type: ignore[arg-type]
    compress_file(in_path, compressed_path, algorithm=algorithm)
    assert compressed_path.exists()
    assert compressed_path.stat().st_size > 0

    decompress_file(compressed_path, out_path)
    assert out_path.exists()

    restored = out_path.read_text(encoding="utf-8")
    assert restored == original


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_file_roundtrip_realistic_text(tmp_path: Path, algorithm: str) -> None:
    # A more "realistic" natural-language sized input (not huge, but clearly non-trivial).
    paragraph = (
        "Lossless compression means we can recover the exact original text after decoding. "
        "This matters when storing documents, logs, and data that must not change. "
        "In practice, texts contain repetition and skewed character frequencies, "
        "so algorithms like Huffman coding and LZ78 can reduce size while preserving content.\n"
    )
    original = paragraph * 200  # scale up to make it realistically larger

    in_path = tmp_path / "input.txt"
    compressed_path = tmp_path / "compressed.bin"
    out_path = tmp_path / "restored.txt"

    in_path.write_text(original, encoding="utf-8")
    # type: ignore[arg-type]
    compress_file(in_path, compressed_path, algorithm=algorithm)
    decompress_file(compressed_path, out_path)

    restored = out_path.read_text(encoding="utf-8")
    assert restored == original


def test_compression_can_reduce_size_on_repetitive_text(tmp_path: Path) -> None:
    # Compression is not guaranteed to be smaller for every input.
    # This test uses highly repetitive input where compression should typically help.
    original = ("abcabcabcabcabcabcabcabcabc\n" * 2000)

    in_path = tmp_path / "input.txt"
    compressed_path_h = tmp_path / "compressed_huffman.bin"
    compressed_path_lz = tmp_path / "compressed_lz78.bin"

    in_path.write_text(original, encoding="utf-8")
    original_size = in_path.stat().st_size

    compress_file(in_path, compressed_path_h, algorithm="huffman")
    compress_file(in_path, compressed_path_lz, algorithm="lz78")

    # At least one of the algorithms should compress this repetitive input noticeably.
    assert (
        compressed_path_h.stat().st_size < original_size
        or compressed_path_lz.stat().st_size < original_size
    )
