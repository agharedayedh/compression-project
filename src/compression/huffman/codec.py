from __future__ import annotations

from dataclasses import dataclass
import heapq
from typing import Optional


@dataclass
class _Node:
    """
    This class represents one node in the Huffman tree.

    A node can either store:
    - a character and its frequency, or
    - just a frequency if it is an internal parent node

    Attributes:
        freq (int): Frequency of the character or combined frequency of child nodes.
        char (Optional[str]): The character stored in the node. Internal nodes use None.
        left (Optional[_Node]): Left child node.
        right (Optional[_Node]): Right child node.
    """
    freq: int
    char: Optional[str] = None
    left: Optional["_Node"] = None
    right: Optional["_Node"] = None


def build_frequency_table(text: str) -> dict[str, int]:
    """
    This function creates a frequency table for the input text.

    It counts how many times each character appears in the text.

    Args:
        text (str): The input text.

    Returns:
        dict[str, int]: A dictionary where the key is a character
        and the value is the number of times it appears.
    """
    freq: dict[str, int] = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def build_huffman_tree(freq: dict[str, int]) -> Optional[_Node]:
    """
    This function builds the Huffman tree from a frequency table.

    The tree is built by repeatedly taking the two nodes with the
    smallest frequencies and combining them into a new parent node.

    Args:
        freq (dict[str, int]): A dictionary that maps each character
        to its frequency.

    Returns:
        Optional[_Node]: The root node of the Huffman tree.
        If the frequency table is empty, the function returns None.
    """
    if not freq:
        return None

    heap: list[tuple[int, int, _Node]] = []
    counter = 0

    for ch, f in sorted(freq.items()):
        heap.append((f, counter, _Node(freq=f, char=ch)))
        counter += 1

    heapq.heapify(heap)

    # Special case: if there is only one different character,
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
    This function builds the Huffman code table from the Huffman tree.

    It goes through the tree and gives each character a binary code.
    Going left adds '0' and going right adds '1'.

    Args:
        root (Optional[_Node]): The root node of the Huffman tree.

    Returns:
        dict[str, str]: A dictionary that maps each character
        to its Huffman code.
    """
    if root is None:
        return {}

    codes: dict[str, str] = {}

    def dfs(node: _Node, prefix: str) -> None:
        """
        Recursive helper function for traversing the tree.

        Args:
            node (_Node): Current node in the tree.
            prefix (str): Current binary code built during traversal.

        Returns:
            None
        """
        if node.char is not None:
            # If there is only one character in the whole text,
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
    This function encodes a text string using Huffman coding.

    First it creates the frequency table, then it builds the
    Huffman tree and code table. After that, it converts the
    text into a binary string using the generated codes.

    Args:
        text (str): The input text to encode.

    Returns:
        tuple[dict[str, int], str]:
            - the frequency table
            - the encoded bit string made of '0' and '1'

    Note:
        The frequency table is returned because it is needed later
        to rebuild the Huffman tree during decoding.
    """
    freq = build_frequency_table(text)
    root = build_huffman_tree(freq)
    codes = build_code_table(root)
    bits = "".join(codes[ch] for ch in text) if text else ""
    return freq, bits


def decode(freq: dict[str, int], bits: str) -> str:
    """
    This function decodes a Huffman encoded bit string back into text.

    It rebuilds the Huffman tree from the frequency table and then
    reads the bit string one bit at a time until the original text
    is reconstructed.

    Args:
        freq (dict[str, int]): The frequency table used to rebuild the tree.
        bits (str): The encoded bit string containing only '0' and '1'.

    Returns:
        str: The decoded original text.

    Raises:
        ValueError: If the bit string contains characters other than
        '0' and '1', or if the bit string ends in the middle of a code.
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

    # If decoding does not end at the root, the last code is incomplete.
    if node is not root:
        raise ValueError(
            "Invalid Huffman bitstring: ended unexpectedly (incomplete code).")

    return "".join(out)
