import pytest

from compression.storage import compress_bytes, decompress_bytes, StorageError

"""
This file tests the full compression and decompression pipeline.

It checks that:
- data can be compressed and then correctly decompressed (round-trip)
- empty input works correctly
- invalid data is handled properly with errors
"""


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_pipeline_roundtrip(algorithm: str) -> None:
    """
    This test checks that compression and decompression work together correctly.

    The text is compressed and then decompressed again.
    The result should be exactly the same as the original text.

    It also includes different types of characters:
    - normal text
    - numbers and symbols
    - emojis
    - non-English characters

    This ensures the system works for general UTF-8 text.
    """
    text = "This is a test. This is a test. 123! 😊 مرحبا"
    data = compress_bytes(text, algorithm=algorithm)
    out = decompress_bytes(data)
    assert out == text


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_pipeline_empty(algorithm: str) -> None:
    """
    This test checks that empty input is handled correctly.

    Compressing and decompressing an empty string
    should return an empty string.
    """
    data = compress_bytes("", algorithm=algorithm)
    out = decompress_bytes(data)
    assert out == ""


def test_pipeline_invalid_data_raises() -> None:
    """
    This test checks that invalid compressed data is handled safely.

    If we try to decompress data that is not in the correct format,
    the program should raise a StorageError.

    This prevents crashes and ensures proper error handling.
    """
    with pytest.raises(StorageError):
        decompress_bytes(b"not a valid compressed file")
