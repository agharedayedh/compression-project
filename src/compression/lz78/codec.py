from __future__ import annotations

Token = list[int | str]


def encode(text: str) -> list[Token]:
    """
    This function compresses a string using the LZ78 algorithm.

    The algorithm builds a dictionary of patterns while reading the text.
    Each output token is a pair:
        [index, character]

    - index: refers to a previous pattern in the dictionary
    - character: the next new character to add

    Args:
        text (str): The input text that we want to compress.

    Returns:
        list[Token]: A list of tokens representing the compressed data.

    Notes:
        - The dictionary starts with an empty string at index 0.
        - New patterns are added as they are discovered.
        - If the text ends with an already known pattern,
          a final token is added with an empty string "".
    """
    dictionary: dict[str, int] = {"": 0}
    next_index = 1

    w = ""
    out: list[Token] = []

    for ch in text:
        wc = w + ch  # try to extend current pattern

        if wc in dictionary:
            w = wc  # pattern exists, keep building it
        else:
            out.append([dictionary[w], ch])  # output token
            dictionary[wc] = next_index  # add new pattern
            next_index += 1
            w = ""  # reset pattern

    # If we end with a known pattern, output a final token
    if w != "":
        out.append([dictionary[w], ""])

    return out


def decode(tokens: list[Token]) -> str:
    """
    This function decompresses LZ78 tokens back into the original text.

    It rebuilds the dictionary step by step using the tokens.
    Each token contains:
        [index, character]

    - index: refers to a previous dictionary entry
    - character: the next character to add

    Args:
        tokens (list[Token]): The compressed tokens from the encode() function.

    Returns:
        str: The original uncompressed text.

    Raises:
        ValueError:
            - If the token format is wrong
            - If the index does not exist in the dictionary

    Notes:
        - The dictionary is rebuilt in the same order as encoding.
        - If the character is "", it means no new character is added
          (used for the final token).
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

        # If char is empty, just use the base pattern
        if ch_raw == "":
            parts.append(base)
            continue

        phrase = base + ch_raw
        parts.append(phrase)

        dictionary[next_index] = phrase  # add new pattern
        next_index += 1

    return "".join(parts)
