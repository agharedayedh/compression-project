from __future__ import annotations
from pathlib import Path
import pytest
from compression.storage import compress_file

"""
This file contains tests for checking if the compression algorithms
actually reduce file size in different situations.

The tests use temporary files and compare the original size
with the compressed size.
"""


def _write_text(path: Path, text: str) -> None:
    """
    Helper function to write text into a file.

    Args:
        path (Path): File path where text will be written.
        text (str): Text content to write.

    Returns:
        None
    """
    path.write_text(text, encoding="utf-8")


def _compress_and_sizes(
    tmp_path: Path, text: str, algorithm: str
) -> tuple[int, int]:
    """
    Helper function that:
    - writes text to a file
    - compresses it using the selected algorithm
    - returns the original and compressed file sizes

    Args:
        tmp_path (Path): Temporary directory provided by pytest.
        text (str): Input text to compress.
        algorithm (str): Compression algorithm ("huffman" or "lz78").

    Returns:
        tuple[int, int]:
            - original file size in bytes
            - compressed file size in bytes
    """
    in_path = tmp_path / "input.txt"
    out_path = tmp_path / "compressed.bin"

    _write_text(in_path, text)
    compress_file(in_path, out_path, algorithm=algorithm)

    original_size = in_path.stat().st_size
    compressed_size = out_path.stat().st_size
    return original_size, compressed_size


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_compression_smaller_for_highly_repetitive_input(
    tmp_path: Path, algorithm: str
) -> None:
    """
    This test checks that compression works well for highly repetitive input.

    The text is just one character repeated many times,
    which should be very easy to compress.

    The test passes if the compressed file is smaller than the original.
    """
    text = "a" * 200_000

    original_size, compressed_size = _compress_and_sizes(
        tmp_path, text, algorithm
    )

    assert compressed_size < original_size, (
        f"Expected compression to reduce size for repetitive input. "
        f"algorithm={algorithm}, original={original_size}, compressed={compressed_size}"
    )


def test_huffman_compression_smaller_for_large_structured_text(
    tmp_path: Path,
) -> None:
    """
    This test checks Huffman compression on more realistic text.

    The input is a paragraph repeated many times,
    which simulates natural language with some structure.

    The test passes if the compressed file is smaller than the original.
    """
    paragraph = (
        "Lossless compression is useful when the exact original text must be recovered. "
        "Natural language contains repeated words, spaces, and punctuation, "
        "which often makes it compressible in practice. "
        "This test uses a larger structured text input to verify that Huffman "
        "can reduce file size on non-trivial text.\n"
    )
    text = paragraph * 3000

    original_size, compressed_size = _compress_and_sizes(
        tmp_path, text, "huffman"
    )

    assert compressed_size < original_size, (
        "Expected Huffman compression to reduce file size for large structured text. "
        f"original={original_size}, compressed={compressed_size}"
    )
