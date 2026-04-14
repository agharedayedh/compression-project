import pytest

from compression.huffman.codec import decode, encode


def test_huffman_roundtrip_simple() -> None:
    text = "aaabcc"
    freq, bits = encode(text)
    out = decode(freq, bits)
    assert out == text


def test_huffman_empty() -> None:
    freq, bits = encode("")
    out = decode(freq, bits)
    assert out == ""


def test_huffman_single_character_repetition() -> None:
    text = "aaaaaa"
    freq, bits = encode(text)
    out = decode(freq, bits)
    assert out == text


def test_huffman_unicode_roundtrip() -> None:
    text = "Hello 😊 مرحبا こんにちは"
    freq, bits = encode(text)
    out = decode(freq, bits)
    assert out == text


def test_huffman_invalid_bit_character() -> None:
    text = "abc"
    freq, bits = encode(text)

    with pytest.raises(ValueError):
        decode(freq, bits + "2")


def test_huffman_incomplete_bitstring() -> None:
    text = "abcdef"
    freq, bits = encode(text)

    if bits:
        truncated = bits[:-1]
        with pytest.raises(ValueError):
            decode(freq, truncated)


def test_huffman_single_symbol_rejects_invalid_branch() -> None:
    text = "aaaaaa"
    freq, bits = encode(text)
    assert bits == "0" * len(text)

    with pytest.raises(ValueError):
        decode(freq, "1")
