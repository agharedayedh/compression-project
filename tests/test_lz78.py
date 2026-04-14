import pytest

from compression.lz78.codec import decode, encode


def test_lz78_roundtrip_simple() -> None:
    data = b"abracadabra"
    tokens = encode(data)
    restored = decode(tokens)
    assert restored == data


def test_lz78_roundtrip_repetitions() -> None:
    data = b"aaaaaaabaaaaaaabaaaaaaab"
    tokens = encode(data)
    restored = decode(tokens)
    assert restored == data


def test_lz78_roundtrip_with_spaces_and_punctuation() -> None:
    data = b"This is a test. This is a test! 123123."
    tokens = encode(data)
    restored = decode(tokens)
    assert restored == data


def test_lz78_roundtrip_utf8_bytes() -> None:
    data = "Agharid 😊😊 hello مرحبا".encode("utf-8")
    tokens = encode(data)
    restored = decode(tokens)
    assert restored == data


def test_lz78_tokens_are_simple_integer_pairs() -> None:
    data = b"abcabcabc"
    tokens = encode(data)

    assert isinstance(tokens, list)
    for tok in tokens:
        assert isinstance(tok, list)
        assert len(tok) == 2
        assert isinstance(tok[0], int)
        assert isinstance(tok[1], int)


def test_lz78_decode_rejects_non_list_token() -> None:
    with pytest.raises(ValueError):
        decode([(0, 97)])  # type: ignore[arg-type]


def test_lz78_decode_rejects_wrong_token_length() -> None:
    with pytest.raises(ValueError):
        decode([[0, 97, 98]])  # type: ignore[list-item]


def test_lz78_decode_rejects_non_int_index() -> None:
    with pytest.raises(ValueError):
        decode([["0", 97]])  # type: ignore[list-item]


def test_lz78_decode_rejects_non_int_byte() -> None:
    with pytest.raises(ValueError):
        decode([[0, "a"]])  # type: ignore[list-item]


def test_lz78_decode_rejects_invalid_dictionary_reference() -> None:
    with pytest.raises(ValueError):
        decode([[999, 97]])


def test_lz78_decode_rejects_final_marker_before_end() -> None:
    with pytest.raises(ValueError):
        decode([[0, 97], [1, -1], [0, 98]])


def test_lz78_decode_rejects_useless_empty_final_token() -> None:
    with pytest.raises(ValueError):
        decode([[0, -1]])
