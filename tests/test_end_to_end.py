from compression.main import compress_text, decompress_bytes


def test_pipeline_roundtrip():
    text = "This is a test. This is a test. 123!"
    data = compress_text(text)
    out = decompress_bytes(data)
    assert out == text
