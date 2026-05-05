import pytest
import random


from compression.huffman.codec import decode, encode


def test_huffman_roundtrip_simple() -> None:
    """
    Test basic roundtrip compression and decompression.

    Checks that a simple string can be encoded and decoded
    back to the original text.
    """
    text = "aaabcc"
    freq, bits = encode(text)
    out = decode(freq, bits)
    assert out == text


def test_huffman_empty() -> None:
    """
    Test behavior with empty input.

    Encoding and decoding an empty string should return an empty string.
    """
    freq, bits = encode("")
    out = decode(freq, bits)
    assert out == ""


def test_huffman_single_character_repetition() -> None:
    """
    Test input containing only one unique character.

    This checks that the algorithm correctly handles the special case
    where the Huffman tree has only one symbol.
    """
    text = "aaaaaa"
    freq, bits = encode(text)
    out = decode(freq, bits)
    assert out == text


def test_huffman_unicode_roundtrip() -> None:
    """
    Test Huffman coding with Unicode text.

    Ensures that encoding and decoding works correctly with
    non-ASCII characters such as emoji and non-Latin scripts.
    """
    text = "Hello 😊 مرحبا こんにちは"
    freq, bits = encode(text)
    out = decode(freq, bits)
    assert out == text


def test_huffman_invalid_bit_character() -> None:
    """
    Test that decoding fails if the bitstring contains invalid characters.

    Only '0' and '1' are allowed in the encoded bitstring.
    """
    text = "abc"
    freq, bits = encode(text)

    with pytest.raises(ValueError):
        decode(freq, bits + "2")


def test_huffman_incomplete_bitstring() -> None:
    """
    Test that decoding fails for incomplete bitstrings.

    Removing part of the bitstring should make decoding invalid.
    """
    text = "abcdef"
    freq, bits = encode(text)

    if bits:
        truncated = bits[:-1]
        with pytest.raises(ValueError):
            decode(freq, truncated)


def test_huffman_single_symbol_rejects_invalid_branch() -> None:
    """
    Test invalid traversal in a single-symbol Huffman tree.

    If the encoded data tries to use a non-existing branch,
    decoding should fail.
    """
    text = "aaaaaa"
    freq, bits = encode(text)
    assert bits == "0" * len(text)

    with pytest.raises(ValueError):
        decode(freq, "1")


def test_huffman_exact_bits_for_small_input() -> None:
    """
    Test a small Huffman case where the expected bitstring can be checked by hand.

    For "aaab", 'a' appears 3 times and 'b' appears 1 time.
    With this implementation, 'b' gets code "0" and 'a' gets code "1".
    Therefore "aaab" becomes "1110".
    """
    text = "aaab"
    freq, bits = encode(text)

    assert freq == {"a": 3, "b": 1}
    assert bits == "1110"
    assert decode(freq, bits) == text


def test_huffman_many_different_unicode_characters() -> None:
    """
    Test Huffman coding with many different Unicode characters.

    This checks that the implementation works when the number of
    different characters is larger than 256.
    """
    text = "".join(chr(0x1000 + i) for i in range(400))

    freq, bits = encode(text)
    restored = decode(freq, bits)

    assert restored == text
    assert len(freq) == 400


def test_huffman_random_text() -> None:
    """
    Test Huffman coding with random Unicode characters.

    A fixed random seed is used so that the test is reproducible.
    """
    random.seed(12345)

    text = "".join(chr(random.randint(0, 1000)) for _ in range(2000))

    freq, bits = encode(text)
    restored = decode(freq, bits)

    assert restored == text
