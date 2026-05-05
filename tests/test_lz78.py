import pytest
import random

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


def test_lz78_exact_tokens_for_aaa() -> None:
    """
    Test a small LZ78 case where the expected tokens can be checked by hand.

    For b"aaa", the encoding should be:
    - [0, 97] for the first 'a'
    - [1, 97] for 'aa'
    """
    data = b"aaa"
    tokens = encode(data)

    assert tokens == [[0, 97], [1, 97]]
    assert decode(tokens) == data


def test_lz78_final_leftover_token_for_aaaa() -> None:
    """
    Test the special case where the last phrase is already in the dictionary.

    For b"aaaa", the last 'a' is left over at the end.
    It is represented using the final token [1, -1].
    """
    data = b"aaaa"
    tokens = encode(data)

    assert tokens == [[0, 97], [1, 97], [1, -1]]
    assert decode(tokens) == data


def test_lz78_exact_tokens_for_aba() -> None:
    """
    Test another small hand-checkable LZ78 example.

    The last 'a' is already in the dictionary, so the final token
    should use the -1 marker.
    """
    data = b"aba"
    tokens = encode(data)

    assert tokens == [[0, 97], [0, 98], [1, -1]]
    assert decode(tokens) == data


def test_lz78_random_byte_data_roundtrip() -> None:
    """
    Test LZ78 with random byte input.

    A fixed seed is used so that the test is reproducible.
    """
    random.seed(12345)

    data = bytes(random.randint(0, 255) for _ in range(10000))

    tokens = encode(data)
    restored = decode(tokens)

    assert restored == data


def test_lz78_index_width_boundary_growth() -> None:
    """
    Test that LZ78 encoding and decoding work correctly
    when the dictionary grows large and index width increases.

    This is an indirect test: it ensures correctness when
    index width transitions occur during encoding.
    """
    data = b"abcdefghijklmnopqrstuvwxyz" * 20

    tokens = encode(data)
    restored = decode(tokens)

    assert restored == data
    assert len(tokens) > 32  # ensures dictionary grows enough
