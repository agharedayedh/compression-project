from __future__ import annotations

Token = list[int]


def encode(data: bytes) -> list[Token]:
    """
    Compress input bytes using the LZ78 algorithm.

    The algorithm builds a dictionary of byte patterns while reading
    the input from left to right.

    Each output token has the form:
        [index, byte]

    where:
    - index points to an earlier dictionary entry
    - byte is the next new byte that extends that pattern

    If the input ends with a pattern that is already in the dictionary,
    a final token [index, -1] is added.

    Args:
        data (bytes): Input data to compress.

    Returns:
        list[Token]: A list of LZ78 tokens.
    """
    dictionary: dict[bytes, int] = {b"": 0}
    next_index = 1

    w = b""
    out: list[Token] = []

    for b in data:
        byte_seq = bytes([b])
        wb = w + byte_seq

        if wb in dictionary:
            w = wb
            continue

        out.append([dictionary[w], b])
        dictionary[wb] = next_index
        next_index += 1
        w = b""

    # If the input ends with an already known pattern,
    # store one final token without a new byte.
    if w:
        out.append([dictionary[w], -1])

    return out


def decode(tokens: list[Token]) -> bytes:
    """
    Decompress LZ78 tokens back into the original bytes.

    The function rebuilds the dictionary in the same order that
    encoding created it.

    Valid tokens are:
    - [index, byte], where byte is in the range 0..255
    - [index, -1] as the final token for a leftover phrase

    Args:
        tokens (list[Token]): Compressed LZ78 tokens.

    Returns:
        bytes: The original decompressed bytes.

    Raises:
        ValueError: If the token structure is invalid,
        the index does not exist, or the final-token rule is broken.
    """
    dictionary: dict[int, bytes] = {0: b""}
    next_index = 1
    parts: list[bytes] = []

    for i, token in enumerate(tokens):
        if not isinstance(token, list) or len(token) != 2:
            raise ValueError("Invalid token format. Expected [index, byte].")

        idx_raw, byte_raw = token

        if not isinstance(idx_raw, int):
            raise ValueError("Invalid token index. Expected int.")
        if not isinstance(byte_raw, int):
            raise ValueError("Invalid token byte. Expected int.")

        if idx_raw < 0:
            raise ValueError(
                f"Invalid token index {idx_raw}: must be non-negative.")
        if idx_raw not in dictionary:
            raise ValueError(
                f"Invalid token index {idx_raw}: not in dictionary.")

        base = dictionary[idx_raw]

        if byte_raw == -1:
            if i != len(tokens) - 1:
                raise ValueError(
                    "Invalid token: -1 byte is only allowed in the final token.")
            if idx_raw == 0:
                raise ValueError(
                    "Invalid token: [0, -1] does not encode any data.")
            parts.append(base)
            continue

        if not 0 <= byte_raw <= 255:
            raise ValueError(
                f"Invalid token byte {byte_raw}: must be in range 0..255 or -1.")

        phrase = base + bytes([byte_raw])
        parts.append(phrase)

        dictionary[next_index] = phrase
        next_index += 1

    return b"".join(parts)
