from __future__ import annotations

from dataclasses import dataclass
import heapq
from typing import Optional


@dataclass
class _Node:
    """Internal node for Huffman tree construction."""
    freq: int
    char: Optional[str] = None
    left: Optional["_Node"] = None
    right: Optional["_Node"] = None


def build_frequency_table(text: str) -> dict[str, int]:
    """
    Build a frequency table mapping each character to its occurrence count.

    Args:
        text: Input text.

    Returns:
        Dictionary mapping character -> frequency.
    """
    freq: dict[str, int] = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def build_huffman_tree(freq: dict[str, int]) -> Optional[_Node]:
    """
    Build the Huffman tree from a frequency table.

    Args:
        freq: Dictionary mapping character -> frequency.

    Returns:
        Root node of the Huffman tree, or None if freq is empty.
    """
    if not freq:
        return None

    heap: list[tuple[int, int, _Node]] = []
    counter = 0

    for ch, f in sorted(freq.items()):
        heap.append((f, counter, _Node(freq=f, char=ch)))
        counter += 1

    heapq.heapify(heap)

    # Special case: only one distinct symbol.
    # Ensure the resulting code is non-empty by making a parent node.
    if len(heap) == 1:
        f, _, only = heap[0]
        return _Node(freq=f, char=None, left=only, right=None)

    while len(heap) > 1:
        f1, _, a = heapq.heappop(heap)
        f2, _, b = heapq.heappop(heap)
        parent = _Node(freq=f1 + f2, char=None, left=a, right=b)
        heapq.heappush(heap, (parent.freq, counter, parent))
        counter += 1

    return heap[0][2]


def build_code_table(root: Optional[_Node]) -> dict[str, str]:
    """
    Build a mapping from character -> Huffman bitstring (as '0'/'1' string).

    Args:
        root: Root of the Huffman tree.

    Returns:
        Dictionary mapping character -> bitstring.
    """
    if root is None:
        return {}

    codes: dict[str, str] = {}

    def dfs(node: _Node, prefix: str) -> None:
        if node.char is not None:
            # If there's only one symbol, use "0" as its code.
            codes[node.char] = prefix or "0"
            return
        if node.left is not None:
            dfs(node.left, prefix + "0")
        if node.right is not None:
            dfs(node.right, prefix + "1")

    dfs(root, "")
    return codes


def encode(text: str) -> tuple[dict[str, int], str]:
    """
    Huffman-encode a text string.

    This implementation returns:
    - frequency table (needed to reconstruct the tree)
    - encoded data as a '0'/'1' string

    Args:
        text: Input text.

    Returns:
        (freq_table, encoded_bits)
    """
    freq = build_frequency_table(text)
    root = build_huffman_tree(freq)
    codes = build_code_table(root)
    bits = "".join(codes[ch] for ch in text) if text else ""
    return freq, bits


def decode(freq: dict[str, int], bits: str) -> str:
    """
    Decode Huffman-encoded bits back into original text.

    Args:
        freq: Frequency table used to rebuild the Huffman tree.
        bits: Bitstring consisting only of '0' and '1'.

    Returns:
        Decoded text.

    Raises:
        ValueError: If bits contain characters other than '0'/'1', or if the
                    bitstring ends mid-code (incomplete final symbol).
    """
    root = build_huffman_tree(freq)
    if root is None:
        return ""

    out: list[str] = []
    node = root

    for b in bits:
        if b == "0":
            node = node.left if node.left is not None else node
        elif b == "1":
            node = node.right if node.right is not None else node
        else:
            raise ValueError(
                "Invalid Huffman bitstring: contains characters other than '0' and '1'."
            )

        if node.char is not None:
            out.append(node.char)
            node = root

    # If we didn't end exactly at the root, the final code was incomplete.
    if node is not root:
        raise ValueError(
            "Invalid Huffman bitstring: ended unexpectedly (incomplete code).")

    return "".join(out)
