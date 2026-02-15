from __future__ import annotations

from pathlib import Path
from typing import Literal

from .huffman.codec import decode as huff_decode
from .huffman.codec import encode as huff_encode
from .lz78.codec import decode as lz78_decode
from .lz78.codec import encode as lz78_encode
from .storage import (
    StorageError,
    detect_algorithm,
    pack_huffman,
    pack_lz78,
    unpack_huffman,
    unpack_lz78,
)

Algorithm = Literal["huffman", "lz78"]


def compress_text(text: str, algorithm: Algorithm = "huffman") -> bytes:
    """
    Compress text and return bytes in a binary container format.
    The output remains compressed on disk and can be decompressed later.
    """
    if algorithm == "huffman":
        freq, bits = huff_encode(text)
        return pack_huffman(freq, bits)

    if algorithm == "lz78":
        tokens = lz78_encode(text)
        return pack_lz78(tokens)

    raise ValueError(f"Unknown algorithm: {algorithm}")


def decompress_bytes(data: bytes) -> str:
    """
    Decompress bytes produced by compress_text().
    Raises ValueError if data is invalid or unsupported.
    """
    try:
        alg = detect_algorithm(data)
        if alg == "huffman":
            freq, bits = unpack_huffman(data)
            return huff_decode(freq, bits)
        if alg == "lz78":
            tokens = unpack_lz78(data)
            return lz78_decode(tokens)
        raise ValueError("Unknown algorithm in compressed data.")
    except StorageError as exc:
        raise ValueError(str(exc)) from exc


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
    for algo in ("huffman", "lz78"):
        # type: ignore[arg-type]
        packed = compress_text(sample, algorithm=algo)
        restored = decompress_bytes(packed)
        print(f"{algo.upper()} OK" if restored ==
              sample else f"{algo.upper()} FAIL")
