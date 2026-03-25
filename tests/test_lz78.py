from compression.lz78.codec import decode, encode
import pytest

"""
This file contains tests for the LZ78 compression algorithm.

It checks:
- correct encoding and decoding (roundtrip)
- handling of different types of text
- support for Unicode
- that tokens have the correct structure
- proper error handling for invalid tokens
"""


def test_lz78_roundtrip_simple():
    """
    This test checks basic functionality.

    A simple string is encoded and then decoded again.
    The result should match the original text.
    """
    text = "abracadabra"
    tokens = encode(text)
    restored = decode(tokens)
    assert restored == text


def test_lz78_roundtrip_repetitions():
    """
    This test checks compression on repetitive input.

    Repeated patterns should be handled correctly by LZ78.
    """
    text = "aaaaaaabaaaaaaabaaaaaaab"
    tokens = encode(text)
    restored = decode(tokens)
    assert restored == text


def test_lz78_roundtrip_with_spaces_and_punctuation():
    """
    This test checks that normal text with spaces,
    punctuation, and numbers is handled correctly.
    """
    text = "This is a test. This is a test! 123123."
    tokens = encode(text)
    restored = decode(tokens)
    assert restored == text


def test_lz78_roundtrip_unicode():
    """
    This test checks that Unicode text works correctly.

    It includes:
    - emoji
    - Arabic text
    - normal English text
    """
    text = "Agharid 😊😊 hello مرحبا"
    tokens = encode(text)
    restored = decode(tokens)
    assert restored == text


def test_lz78_tokens_are_json_friendly():
    """
    This test checks that the output tokens have a simple structure.

    The tokens should:
    - be a list
    - contain only lists of length 2
    - store index as int and character as string

    This makes them easy to store or convert (for example to JSON).
    """
    text = "abcabcabc"
    tokens = encode(text)

    assert isinstance(tokens, list)
    for tok in tokens:
        assert isinstance(tok, list)
        assert len(tok) == 2
        assert isinstance(tok[0], int)
        assert isinstance(tok[1], str)


def test_lz78_decode_rejects_non_list_token():
    """
    This test checks that invalid token types are rejected.

    Tokens must be lists, not tuples or other types.
    """
    with pytest.raises(ValueError):
        decode([("not", "a list")])  # type: ignore[arg-type]


def test_lz78_decode_rejects_wrong_token_length():
    """
    This test checks that tokens must have exactly two elements.

    Extra elements should cause an error.
    """
    with pytest.raises(ValueError):
        decode([[0, "a", "extra"]])  # type: ignore[list-item]


def test_lz78_decode_rejects_non_int_index():
    """
    This test checks that the token index must be an integer.
    """
    with pytest.raises(ValueError):
        decode([["0", "a"]])  # type: ignore[list-item]


def test_lz78_decode_rejects_non_str_char():
    """
    This test checks that the token character must be a string.
    """
    with pytest.raises(ValueError):
        decode([[0, 5]])  # type: ignore[list-item]


def test_lz78_decode_rejects_invalid_dictionary_reference():
    """
    This test checks that invalid dictionary references are not allowed.

    If a token refers to an index that does not exist,
    decoding should raise an error.
    """
    # Index 999 does not exist at the start
    with pytest.raises(ValueError):
        decode([[999, "a"]])
