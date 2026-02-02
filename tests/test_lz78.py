from compression.lz78.codec import decode, encode


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
    text = "Ågharid 😊😊 hello مرحبا"
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
