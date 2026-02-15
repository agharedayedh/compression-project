import pytest
from compression.main import compress_text, decompress_bytes


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_pipeline_roundtrip(algorithm):
    text = "This is a test. This is a test. 123!"
    data = compress_text(text, algorithm=algorithm)
    out = decompress_bytes(data)
    assert out == text


@pytest.mark.parametrize("algorithm", ["huffman", "lz78"])
def test_pipeline_empty(algorithm):
    data = compress_text("", algorithm=algorithm)
    out = decompress_bytes(data)
    assert out == ""


def test_pipeline_invalid_data_raises():
    with pytest.raises(ValueError):
        decompress_bytes(b"not a valid compressed file")
