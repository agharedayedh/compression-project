from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from .huffman.codec import decode as huff_decode
from .huffman.codec import encode as huff_encode

from .lz78.codec import decode as lz78_decode
from .lz78.codec import encode as lz78_encode

Algorithm = Literal["huffman", "lz78"]


def compress_text(text: str, algorithm: Algorithm = "huffman") -> bytes:

    if algorithm == "huffman":
        freq, bits = huff_encode(text)
        payload: dict[str, Any] = {
            "algorithm": "huffman", "freq": freq, "bits": bits}
    elif algorithm == "lz78":
        tokens = lz78_encode(text)
        payload = {"algorithm": "lz78", "tokens": tokens}
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def decompress_bytes(data: bytes) -> str:
    payload = json.loads(data.decode("utf-8"))
    algorithm = payload.get("algorithm")

    if algorithm == "huffman":
        freq = payload["freq"]
        bits = payload["bits"]
        return huff_decode(freq, bits)

    if algorithm == "lz78":
        tokens = payload["tokens"]
        return lz78_decode(tokens)

    raise ValueError(
        "Invalid compressed data: missing/unknown 'algorithm' field")


def compress_file(
    input_path: str | Path,
    output_path: str | Path,
    algorithm: Algorithm = "huffman",
) -> None:
    text = Path(input_path).read_text(encoding="utf-8")
    Path(output_path).write_bytes(compress_text(text, algorithm=algorithm))


def decompress_file(input_path: str | Path, output_path: str | Path) -> None:
    data = Path(input_path).read_bytes()
    Path(output_path).write_text(decompress_bytes(data), encoding="utf-8")


if __name__ == "__main__":
    sample = "hello hello hello"
    packed_h = compress_text(sample, algorithm="huffman")
    restored_h = decompress_bytes(packed_h)
    print("HUFFMAN OK" if restored_h == sample else "HUFFMAN FAIL")

    packed_lz = compress_text(sample, algorithm="lz78")
    restored_lz = decompress_bytes(packed_lz)
    print("LZ78 OK" if restored_lz == sample else "LZ78 FAIL")
