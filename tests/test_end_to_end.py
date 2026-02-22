import pytest

from compression.storage import compress_bytes, decompress_bytes, StorageError


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_pipeline_roundtrip(algorithm: str) -> None:
    text = "This is a test. This is a test. 123! 😊 مرحبا"
    data = compress_bytes(text, algorithm=algorithm)
    out = decompress_bytes(data)
    assert out == text


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_pipeline_empty(algorithm: str) -> None:
    data = compress_bytes("", algorithm=algorithm)
    out = decompress_bytes(data)
    assert out == ""


def test_pipeline_invalid_data_raises() -> None:
    with pytest.raises(StorageError):
        decompress_bytes(b"not a valid compressed file")
