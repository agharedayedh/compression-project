from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Optional


@dataclass
class _Node:
    freq: int
    char: Optional[str] = None
    left: Optional["_Node"] = None
    right: Optional["_Node"] = None


def build_frequency_table(text: str) -> dict[str, int]:
    freq: dict[str, int] = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def build_huffman_tree(freq: dict[str, int]) -> Optional[_Node]:
    if not freq:
        return None

    heap: list[tuple[int, int, _Node]] = []
    counter = 0

    for ch, f in sorted(freq.items()):
        heap.append((f, counter, _Node(freq=f, char=ch)))
        counter += 1

    heapq.heapify(heap)

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
    if root is None:
        return {}

    codes: dict[str, str] = {}

    def dfs(node: _Node, prefix: str) -> None:
        if node.char is not None:
            codes[node.char] = prefix or "0"
            return
        if node.left is not None:
            dfs(node.left, prefix + "0")
        if node.right is not None:
            dfs(node.right, prefix + "1")

    dfs(root, "")
    return codes


def encode(text: str) -> tuple[dict[str, int], str]:
    freq = build_frequency_table(text)
    root = build_huffman_tree(freq)
    codes = build_code_table(root)
    bits = "".join(codes[ch] for ch in text) if text else ""
    return freq, bits


def decode(freq: dict[str, int], bits: str) -> str:
    """
    Decode a Huffman bitstring strictly.

    Raises:
        ValueError: For non-binary characters, impossible tree paths,
        or incomplete codes.
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
