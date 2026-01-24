from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .huffman.codec import decode as huff_decode
from .huffman.codec import encode as huff_encode


def compress_text(text: str) -> bytes:

    freq, bits = huff_encode(text)
    payload: dict[str, Any] = {"freq": freq, "bits": bits}
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def decompress_bytes(data: bytes) -> str:
    payload = json.loads(data.decode("utf-8"))
    freq = payload["freq"]
    bits = payload["bits"]
    return huff_decode(freq, bits)


def compress_file(input_path: str | Path, output_path: str | Path) -> None:
    text = Path(input_path).read_text(encoding="utf-8")
    Path(output_path).write_bytes(compress_text(text))


def decompress_file(input_path: str | Path, output_path: str | Path) -> None:
    data = Path(input_path).read_bytes()
    Path(output_path).write_text(decompress_bytes(data), encoding="utf-8")


if __name__ == "__main__":
    sample = "hello hello hello"
    packed = compress_text(sample)
    restored = decompress_bytes(packed)
    print("OK" if restored == sample else "FAIL")
