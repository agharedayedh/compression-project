from __future__ import annotations

Token = list[int]


def encode(data: bytes) -> list[Token]:
    """
    Compress bytes using LZ78 with variable-length indexes.

    Each token is:
        [index, byte]

    where:
    - index refers to a previously seen phrase
    - byte is the next literal byte (0..255)

    A final leftover phrase is emitted as:
        [index, -1]
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

    if w:
        out.append([dictionary[w], -1])

    return out


def decode(tokens: list[Token]) -> bytes:
    """
    Decompress LZ78 tokens back into the original bytes.

    Valid tokens are:
    - [index, byte] where byte is 0..255
    - final token [index, -1] for leftover phrase

    Raises:
        ValueError: if token structure or references are invalid.
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
