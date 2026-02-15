from __future__ import annotations

from pathlib import Path

import pytest

from compression.main import compress_file


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _compress_and_sizes(tmp_path: Path, text: str, algorithm: str) -> tuple[int, int]:
    in_path = tmp_path / "input.txt"
    out_path = tmp_path / "compressed.bin"

    _write_text(in_path, text)
    # type: ignore[arg-type]
    compress_file(in_path, out_path, algorithm=algorithm)

    original_size = in_path.stat().st_size
    compressed_size = out_path.stat().st_size
    return original_size, compressed_size


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_compression_smaller_for_highly_repetitive_input(tmp_path: Path, algorithm: str) -> None:
    # Highly repetitive input should compress smaller with both algorithms.
    # Use a large size so container/header overhead cannot dominate.
    text = "a" * 200_000

    original_size, compressed_size = _compress_and_sizes(
        tmp_path, text, algorithm)

    assert compressed_size < original_size, (
        f"Expected compression to reduce size for repetitive input. "
        f"algorithm={algorithm}, original={original_size}, compressed={compressed_size}"
    )


def test_huffman_compression_usually_smaller_for_large_natural_language(tmp_path: Path) -> None:
    # Natural-language style input (multi-sentence) repeated to a realistic size.
    # For Huffman, we expect the compressed output to be smaller in typical cases,
    # especially when input is large enough.
    paragraph = (
        "Lossless compression is useful when the exact original text must be recovered. "
        "Natural language contains patterns such as repeated words, spaces, and punctuation, "
        "which makes it compressible in many practical cases. "
        "This test uses a realistic paragraph repeated many times to produce a large input.\n"
    )
    text = paragraph * 3000  # large enough that size behavior is meaningful

    original_size, compressed_size = _compress_and_sizes(
        tmp_path, text, "huffman")

    assert compressed_size < original_size, (
        "Expected Huffman compression to reduce file size for large natural-language input. "
        f"original={original_size}, compressed={compressed_size}"
    )
