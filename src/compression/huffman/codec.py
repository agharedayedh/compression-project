from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Optional


@dataclass
class _Node:
    """
    One node in the Huffman tree.

    A node can be:
    - a leaf node, which stores one character
    - an internal node, which stores only the combined frequency

    Attributes:
        freq (int): Frequency of the character or combined frequency.
        char (Optional[str]): Stored character for a leaf node.
            Internal nodes use None.
        left (Optional[_Node]): Left child node.
        right (Optional[_Node]): Right child node.
    """
    freq: int
    char: Optional[str] = None
    left: Optional["_Node"] = None
    right: Optional["_Node"] = None


def build_frequency_table(text: str) -> dict[str, int]:
    """
    Build a frequency table for the input text.

    The function counts how many times each character appears.

    Args:
        text (str): Input text.

    Returns:
        dict[str, int]: A dictionary where keys are characters
        and values are their frequencies.
    """
    freq: dict[str, int] = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def build_huffman_tree(freq: dict[str, int]) -> Optional[_Node]:
    """
    Build a Huffman tree from a frequency table.

    The tree is created by repeatedly taking the two nodes with the
    smallest frequencies and combining them into a new parent node.

    Args:
        freq (dict[str, int]): Frequency table of the input text.

    Returns:
        Optional[_Node]: Root node of the Huffman tree.
        Returns None if the frequency table is empty.
    """
    if not freq:
        return None

    heap: list[tuple[int, int, _Node]] = []
    counter = 0

    for ch, f in sorted(freq.items()):
        heap.append((f, counter, _Node(freq=f, char=ch)))
        counter += 1

    heapq.heapify(heap)

    # Special case: if the text contains only one different character,
    # create a parent node so that the code is not empty.
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
    Build the Huffman code table from the tree.

    Moving left adds "0" to the code and moving right adds "1".
    Each leaf node gets the code built on the path from the root.

    Args:
        root (Optional[_Node]): Root of the Huffman tree.

    Returns:
        dict[str, str]: A dictionary that maps each character
        to its Huffman code.
    """
    if root is None:
        return {}

    codes: dict[str, str] = {}

    def dfs(node: _Node, prefix: str) -> None:
        """
        Traverse the tree recursively and assign codes to characters.

        Args:
            node (_Node): Current node in the tree.
            prefix (str): Current binary code built so far.

        Returns:
            None
        """
        if node.char is not None:
            # If there is only one unique character,
            # use "0" as its code.
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
    Encode text using Huffman coding.

    The function builds the frequency table, creates the Huffman tree,
    creates the code table, and then converts the text into a bitstring.

    Args:
        text (str): Input text to encode.

    Returns:
        tuple[dict[str, int], str]:
            - frequency table used to rebuild the tree later
            - encoded bitstring made of "0" and "1"
    """
    freq = build_frequency_table(text)
    root = build_huffman_tree(freq)
    codes = build_code_table(root)
    bits = "".join(codes[ch] for ch in text) if text else ""
    return freq, bits


def decode(freq: dict[str, int], bits: str) -> str:
    """
    Decode a Huffman bitstring back into the original text.

    The function rebuilds the Huffman tree from the frequency table
    and then reads the bitstring one bit at a time.

    Args:
        freq (dict[str, int]): Frequency table used to rebuild the tree.
        bits (str): Encoded Huffman bitstring.

    Returns:
        str: The decoded original text.

    Raises:
        ValueError: If the bitstring contains characters other than
        "0" and "1", tries to follow an impossible tree path,
        or ends in the middle of a code.
    """
    root = build_huffman_tree(freq)
    if root is None:
        if bits:
            raise ValueError(
                "Invalid Huffman bitstring for empty frequency table.")
        return ""

    out: list[str] = []
    node = root

    for b in bits:
        if b not in ("0", "1"):
            raise ValueError(
                "Invalid Huffman bitstring: contains characters other than '0' and '1'."
            )

        if b == "0":
            if node.left is None:
                raise ValueError(
                    "Invalid Huffman bitstring: impossible left traversal.")
            node = node.left
        else:
            if node.right is None:
                raise ValueError(
                    "Invalid Huffman bitstring: impossible right traversal.")
            node = node.right

        if node.char is not None:
            out.append(node.char)
            node = root

    if node is not root:
        raise ValueError(
            "Invalid Huffman bitstring: ended unexpectedly (incomplete code).")

    return "".join(out)
