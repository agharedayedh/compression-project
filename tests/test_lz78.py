import pytest

from compression.lz78.codec import decode, encode


def test_lz78_roundtrip_simple() -> None:
    """
    Test basic LZ78 roundtrip.

    Checks that simple byte data can be encoded and decoded
    back to the original.
    """
    data = b"abracadabra"
    tokens = encode(data)
    restored = decode(tokens)
    assert restored == data


def test_lz78_roundtrip_repetitions() -> None:
    """
    Test LZ78 with highly repetitive input.

    Ensures that repeated patterns are handled correctly.
    """
    data = b"aaaaaaabaaaaaaabaaaaaaab"
    tokens = encode(data)
    restored = decode(tokens)
    assert restored == data


def test_lz78_roundtrip_with_spaces_and_punctuation() -> None:
    """
    Test LZ78 with typical text containing spaces and punctuation.
    """
    data = b"This is a test. This is a test! 123123."
    tokens = encode(data)
    restored = decode(tokens)
    assert restored == data


def test_lz78_roundtrip_utf8_bytes() -> None:
    """
    Test LZ78 with UTF-8 encoded text.

    Ensures that byte-level encoding works correctly
    for Unicode input.
    """
    data = "Agharid 😊😊 hello مرحبا".encode("utf-8")
    tokens = encode(data)
    restored = decode(tokens)
    assert restored == data


def test_lz78_tokens_are_simple_integer_pairs() -> None:
    """
    Test that generated tokens have the correct structure.

    Each token should:
    - be a list
    - have exactly two elements
    - both elements should be integers
    """
    data = b"abcabcabc"
    tokens = encode(data)

    assert isinstance(tokens, list)
    for tok in tokens:
        assert isinstance(tok, list)
        assert len(tok) == 2
        assert isinstance(tok[0], int)
        assert isinstance(tok[1], int)


def test_lz78_decode_rejects_non_list_token() -> None:
    """
    Test that decode rejects tokens that are not lists.
    """
    with pytest.raises(ValueError):
        decode([(0, 97)])  # type: ignore[arg-type]


def test_lz78_decode_rejects_wrong_token_length() -> None:
    """
    Test that decode rejects tokens with incorrect length.
    """
    with pytest.raises(ValueError):
        decode([[0, 97, 98]])  # type: ignore[list-item]


def test_lz78_decode_rejects_non_int_index() -> None:
    """
    Test that decode rejects tokens where the index is not an integer.
    """
    with pytest.raises(ValueError):
        decode([["0", 97]])  # type: ignore[list-item]


def test_lz78_decode_rejects_non_int_byte() -> None:
    """
    Test that decode rejects tokens where the byte is not an integer.
    """
    with pytest.raises(ValueError):
        decode([[0, "a"]])  # type: ignore[list-item]


def test_lz78_decode_rejects_invalid_dictionary_reference() -> None:
    """
    Test that decode fails if a token refers to a non-existing dictionary entry.
    """
    with pytest.raises(ValueError):
        decode([[999, 97]])


def test_lz78_decode_rejects_final_marker_before_end() -> None:
    """
    Test that the special final token marker (-1) is only allowed at the end.
    """
    with pytest.raises(ValueError):
        decode([[0, 97], [1, -1], [0, 98]])


def test_lz78_decode_rejects_useless_empty_final_token() -> None:
    """
    Test that an invalid final token [0, -1] is rejected.

    This token would not represent any data.
    """
    with pytest.raises(ValueError):
        decode([[0, -1]])
