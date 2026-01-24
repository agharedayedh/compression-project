from __future__ import annotations

from dataclasses import dataclass
import heapq
from typing import Optional, Dict


@dataclass
class _Node:
    freq: int
    char: Optional[str] = None
    left: Optional["_Node"] = None
    right: Optional["_Node"] = None


def build_frequency_table(text: str) -> Dict[str, int]:
    freq: Dict[str, int] = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def build_huffman_tree(freq: Dict[str, int]) -> Optional[_Node]:

    if not freq:
        return None

    heap: list[tuple[int, int, _Node]] = []
    counter = 0

    for ch, f in freq.items():
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


def build_code_table(root: Optional[_Node]) -> Dict[str, str]:
    if root is None:
        return {}

    codes: Dict[str, str] = {}

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


def encode(text: str) -> tuple[Dict[str, int], str]:

    freq = build_frequency_table(text)
    root = build_huffman_tree(freq)
    codes = build_code_table(root)
    bits = "".join(codes[ch] for ch in text) if text else ""
    return freq, bits


def decode(freq: Dict[str, int], bits: str) -> str:

    root = build_huffman_tree(freq)
    if root is None:
        return ""

    out: list[str] = []
    node = root

    for b in bits:
        if b == "0":
            node = node.left if node.left is not None else node
        else:
            node = node.right if node.right is not None else node

        if node.char is not None:
            out.append(node.char)
            node = root

    return "".join(out)
