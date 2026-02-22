from compression.lz78.codec import decode, encode
import pytest


def test_lz78_roundtrip_simple():
    text = "abracadabra"
    tokens = encode(text)
    restored = decode(tokens)
    assert restored == text


def test_lz78_roundtrip_repetitions():
    text = "aaaaaaabaaaaaaabaaaaaaab"
    tokens = encode(text)
    restored = decode(tokens)
    assert restored == text


def test_lz78_roundtrip_with_spaces_and_punctuation():
    text = "This is a test. This is a test! 123123."
    tokens = encode(text)
    restored = decode(tokens)
    assert restored == text


def test_lz78_roundtrip_unicode():
    text = "Agharid 😊😊 hello مرحبا"
    tokens = encode(text)
    restored = decode(tokens)
    assert restored == text


def test_lz78_tokens_are_json_friendly():
    text = "abcabcabc"
    tokens = encode(text)

    assert isinstance(tokens, list)
    for tok in tokens:
        assert isinstance(tok, list)
        assert len(tok) == 2
        assert isinstance(tok[0], int)
        assert isinstance(tok[1], str)


def test_lz78_decode_rejects_non_list_token():
    with pytest.raises(ValueError):
        decode([("not", "a list")])  # type: ignore[arg-type]


def test_lz78_decode_rejects_wrong_token_length():
    with pytest.raises(ValueError):
        decode([[0, "a", "extra"]])  # type: ignore[list-item]


def test_lz78_decode_rejects_non_int_index():
    with pytest.raises(ValueError):
        decode([["0", "a"]])  # type: ignore[list-item]


def test_lz78_decode_rejects_non_str_char():
    with pytest.raises(ValueError):
        decode([[0, 5]])  # type: ignore[list-item]


def test_lz78_decode_rejects_invalid_dictionary_reference():
    # Index 999 doesn't exist at the start (dictionary initially has only 0 -> "")
    with pytest.raises(ValueError):
        decode([[999, "a"]])
