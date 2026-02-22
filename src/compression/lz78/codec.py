from __future__ import annotations

Token = list[int | str]


def encode(text: str) -> list[Token]:
    """
    LZ78-encode a string into a list of tokens.

    Each token is a pair: [index, char]
    - index: integer reference to a previous dictionary entry
    - char: the next character to append (may be "" in the final token)

    Args:
        text: Input text.

    Returns:
        List of tokens representing the compressed data.
    """
    dictionary: dict[str, int] = {"": 0}
    next_index = 1

    w = ""
    out: list[Token] = []

    for ch in text:
        wc = w + ch
        if wc in dictionary:
            w = wc
        else:
            out.append([dictionary[w], ch])
            dictionary[wc] = next_index
            next_index += 1
            w = ""

    # If we end with a phrase already in the dictionary, emit a final token.
    if w != "":
        out.append([dictionary[w], ""])

    return out


def decode(tokens: list[Token]) -> str:
    """
    Decode LZ78 tokens back into the original string.

    Args:
        tokens: Tokens produced by encode(), each token must be [int, str].

    Returns:
        The decoded (original) text.

    Raises:
        ValueError: If the token format is invalid or the dictionary reference
                    is impossible.
    """
    dictionary: dict[int, str] = {0: ""}
    next_index = 1

    parts: list[str] = []

    for token in tokens:
        if not isinstance(token, list) or len(token) != 2:
            raise ValueError("Invalid token format. Expected [index, char].")

        idx_raw, ch_raw = token

        if not isinstance(idx_raw, int):
            raise ValueError("Invalid token index. Expected int.")
        if not isinstance(ch_raw, str):
            raise ValueError("Invalid token char. Expected str.")

        if idx_raw not in dictionary:
            raise ValueError(
                f"Invalid token index {idx_raw}: not in dictionary.")

        base = dictionary[idx_raw]

        # Final token may use empty string to indicate "no new character".
        if ch_raw == "":
            parts.append(base)
            continue

        phrase = base + ch_raw
        parts.append(phrase)

        dictionary[next_index] = phrase
        next_index += 1

    return "".join(parts)
