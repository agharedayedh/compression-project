from __future__ import annotations

from pathlib import Path

import pytest

from compression.storage import compress_file, decompress_file


def _load_corpus() -> str:
    """
    Load the natural-language corpus from data/corpus/.

    Returns:
        str: Combined corpus text.
    """
    corpus_dir = Path("data") / "corpus"
    parts: list[str] = []

    for path in sorted(corpus_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            parts.append(text)

    if not parts:
        pytest.skip("No usable corpus files found in data/corpus/.")

    return "\n\n".join(parts)


def _safe_prefix_to_size(text: str, target_bytes: int) -> str:
    """
    Return a UTF-8 safe prefix of the text with approximately target_bytes.

    Args:
        text (str): Input corpus text.
        target_bytes (int): Wanted size in bytes.

    Returns:
        str: Prefix that does not cut UTF-8 characters in the middle.
    """
    raw = text.encode("utf-8")

    if len(raw) < target_bytes:
        pytest.skip(
            f"Corpus is too small for this test. "
            f"Need {target_bytes} bytes, got {len(raw)} bytes."
        )

    return raw[:target_bytes].decode("utf-8", errors="ignore")


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_large_corpus_roundtrip_6mb(tmp_path: Path, algorithm: str) -> None:
    """
    Test compression and decompression on a large realistic corpus input (~6 MB).

    This better represents "several megabytes" as mentioned in requirements.
    """
    corpus = _load_corpus()
    text = _safe_prefix_to_size(corpus, 6 * 1024 * 1024)

    input_path = tmp_path / "large_input.txt"
    compressed_path = tmp_path / "large_compressed.bin"
    restored_path = tmp_path / "large_restored.txt"

    input_path.write_text(text, encoding="utf-8")

    compress_file(input_path, compressed_path, algorithm=algorithm)
    decompress_file(compressed_path, restored_path)

    restored = restored_path.read_text(encoding="utf-8")

    assert restored == text


def test_lz78_large_corpus_roundtrip_10mb(tmp_path: Path) -> None:
    """
    Test LZ78 on a large (~10 MB) realistic corpus input.

    LZ78 is especially important to test on large inputs because
    dictionary-related errors may only appear after the dictionary grows
    and variable-length index sizes increase.
    """
    corpus = _load_corpus()
    text = _safe_prefix_to_size(corpus, 10 * 1024 * 1024)

    input_path = tmp_path / "lz78_large_input.txt"
    compressed_path = tmp_path / "lz78_large_compressed.bin"
    restored_path = tmp_path / "lz78_large_restored.txt"

    input_path.write_text(text, encoding="utf-8")

    compress_file(input_path, compressed_path, algorithm="lz78")
    decompress_file(compressed_path, restored_path)

    restored = restored_path.read_text(encoding="utf-8")

    assert restored == text


def test_huffman_large_corpus_roundtrip_10mb(tmp_path: Path) -> None:
    """
    Test Huffman coding on a large (~10 MB) realistic corpus input.

    This ensures that Huffman encoding and decoding remain correct
    when the input contains many characters and large frequency tables.
    """
    corpus = _load_corpus()
    text = _safe_prefix_to_size(corpus, 10 * 1024 * 1024)

    input_path = tmp_path / "huffman_large_input.txt"
    compressed_path = tmp_path / "huffman_large_compressed.bin"
    restored_path = tmp_path / "huffman_large_restored.txt"

    input_path.write_text(text, encoding="utf-8")

    compress_file(input_path, compressed_path, algorithm="huffman")
    decompress_file(compressed_path, restored_path)

    restored = restored_path.read_text(encoding="utf-8")

    assert restored == text
