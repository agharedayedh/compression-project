from compression.huffman.codec import encode, decode
import pytest


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


def test_huffman_unicode_roundtrip():
    text = "Hello 😊 مرحبا こんにちは"
    freq, bits = encode(text)
    out = decode(freq, bits)
    assert out == text


def test_huffman_invalid_bit_character():
    text = "abc"
    freq, bits = encode(text)

    with pytest.raises(ValueError):
        decode(freq, bits + "2")  # invalid binary character


def test_huffman_incomplete_bitstring():
    text = "abcdef"
    freq, bits = encode(text)

    if bits:  # avoid empty case
        truncated = bits[:-1]
        with pytest.raises(ValueError):
            decode(freq, truncated)
