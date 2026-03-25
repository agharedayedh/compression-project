from compression.huffman.codec import encode, decode
import pytest

"""
This file contains tests for the Huffman coding implementation.

It checks:
- correct encoding and decoding (roundtrip)
- handling of empty input
- behavior with repeated characters
- support for Unicode text
- proper error handling for invalid input
"""


def test_huffman_roundtrip_simple():
    """
    This test checks basic functionality.

    A simple string is encoded and then decoded again.
    The output should match the original text.
    """
    text = "aaabcc"
    freq, bits = encode(text)
    out = decode(freq, bits)
    assert out == text


def test_huffman_empty():
    """
    This test checks that empty input is handled correctly.

    Encoding and decoding an empty string should return an empty string.
    """
    freq, bits = encode("")
    out = decode(freq, bits)
    assert out == ""


def test_huffman_single_character_repetition():
    """
    This test checks behavior when the input contains only one character.

    This is a special case in Huffman coding.
    The algorithm should still work correctly.
    """
    text = "aaaaaa"
    freq, bits = encode(text)
    out = decode(freq, bits)
    assert out == text


def test_huffman_unicode_roundtrip():
    """
    This test checks that Unicode text is handled correctly.

    It includes:
    - normal English text
    - emoji
    - Arabic text
    - Japanese text

    The decoded output should match the original input.
    """
    text = "Hello 😊 مرحبا こんにちは"
    freq, bits = encode(text)
    out = decode(freq, bits)
    assert out == text


def test_huffman_invalid_bit_character():
    """
    This test checks error handling for invalid bitstrings.

    If the bitstring contains characters other than '0' and '1',
    decoding should raise a ValueError.
    """
    text = "abc"
    freq, bits = encode(text)

    with pytest.raises(ValueError):
        decode(freq, bits + "2")  # invalid binary character


def test_huffman_incomplete_bitstring():
    """
    This test checks error handling for incomplete bitstrings.

    If the bitstring is cut off before a full character is decoded,
    the decoder should raise a ValueError.
    """
    text = "abcdef"
    freq, bits = encode(text)

    if bits:  # avoid empty case
        truncated = bits[:-1]
        with pytest.raises(ValueError):
            decode(freq, truncated)
