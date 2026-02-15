from __future__ import annotations

from typing import List

Token = list[int | str]


def encode(text: str) -> List[Token]:
    dictionary: dict[str, int] = {"": 0}
    next_index = 1

    w = ""
    out: List[Token] = []

    for c in text:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            out.append([dictionary[w], c])
            dictionary[wc] = next_index
            next_index += 1
            w = ""

    if w != "":
        out.append([dictionary[w], ""])

    return out


def decode(tokens: List[Token]) -> str:
    dictionary: dict[int, str] = {0: ""}
    next_index = 1
    parts: list[str] = []

    for t in tokens:
        if not isinstance(t, list) or len(t) != 2:
            raise ValueError("Invalid token format. Expected [index, char].")

        idx_raw, ch_raw = t
        if not isinstance(idx_raw, int):
            raise ValueError("Invalid token index. Expected int.")
        if not isinstance(ch_raw, str):
            raise ValueError("Invalid token char. Expected str.")

        if idx_raw not in dictionary:
            raise ValueError(
                f"Invalid token index {idx_raw}: not in dictionary.")

        base = dictionary[idx_raw]

        if ch_raw == "":
            parts.append(base)
            continue

        phrase = base + ch_raw
        parts.append(phrase)

        dictionary[next_index] = phrase
        next_index += 1

    return "".join(parts)
