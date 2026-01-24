from compression.huffman.codec import encode, decode


def test_huffman_roundtrip_simple():
    text = "aaabcc"
    freq, bits = encode(text)
    out = decode(freq, bits)
    assert out == text


def test_huffman_empty():
    freq, bits = encode("")
    out = decode(freq, bits)
    assert out == ""


def test_huffman_single_character_repetition():
    text = "aaaaaa"
    freq, bits = encode(text)
    out = decode(freq, bits)
    assert out == text
