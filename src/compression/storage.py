from __future__ import annotations

import struct
from pathlib import Path
from typing import Literal, TypeAlias

from .huffman.codec import decode as huff_decode
from .huffman.codec import encode as huff_encode
from .lz78.codec import decode as lz78_decode
from .lz78.codec import encode as lz78_encode

Algorithm = Literal["huffman", "lz78"]
LZ78Token: TypeAlias = list[int | str]

# Binary container format:
# magic (4 bytes) + version (1 byte) + algorithm_id (1 byte)
# magic = b"CPRJ" (Compression PRoJect)
_MAGIC = b"CPRJ"
_VERSION = 1

_ALG_TO_ID: dict[str, int] = {"huffman": 1, "lz78": 2}
_ID_TO_ALG: dict[int, str] = {1: "huffman", 2: "lz78"}


class StorageError(ValueError):
    """Raised when compressed bytes are invalid or cannot be parsed."""


def _pack_header(algorithm: Algorithm) -> bytes:
    """Pack header: magic + version + algorithm id."""
    return _MAGIC + struct.pack(">BB", _VERSION, _ALG_TO_ID[algorithm])


def _unpack_header(data: bytes) -> tuple[Algorithm, int]:
    """
    Validate and parse the container header.

    Returns:
        (algorithm, payload_start_offset)
    """
    if len(data) < 6:
        raise StorageError("Invalid data: too short for header.")
    if data[:4] != _MAGIC:
        raise StorageError("Invalid data: wrong magic header.")
    version, alg_id = struct.unpack(">BB", data[4:6])
    if version != _VERSION:
        raise StorageError(f"Unsupported format version: {version}")
    if alg_id not in _ID_TO_ALG:
        raise StorageError(f"Unknown algorithm id: {alg_id}")
    return _ID_TO_ALG[alg_id], 6


def pack_bits(bitstring: str) -> tuple[int, bytes]:
    """
    Pack a '0'/'1' bitstring into bytes.

    Returns:
        (bit_length, packed_bytes)
    """
    bit_len = len(bitstring)
    if bit_len == 0:
        return 0, b""

    for ch in bitstring:
        if ch not in ("0", "1"):
            raise StorageError(
                "Invalid bitstring: contains non-binary characters.")

    out = bytearray()
    current = 0
    filled = 0  # how many bits are in current byte

    for b in bitstring:
        current = (current << 1) | (1 if b == "1" else 0)
        filled += 1
        if filled == 8:
            out.append(current)
            current = 0
            filled = 0

    if filled != 0:
        current = current << (8 - filled)  # left-align remaining bits
        out.append(current)

    return bit_len, bytes(out)


def unpack_bits(bit_len: int, data: bytes) -> str:
    """
    Unpack bytes into a '0'/'1' bitstring using the stored bit length.

    Args:
        bit_len: Number of valid bits in the packed data.
        data: Packed bytes (may include padding bits).

    Returns:
        Bitstring of length bit_len.
    """
    if bit_len < 0:
        raise StorageError("Invalid bit length.")
    if bit_len == 0:
        return ""

    needed_bytes = (bit_len + 7) // 8
    if len(data) < needed_bytes:
        raise StorageError(
            "Invalid data: not enough bytes for the declared bit length.")

    bits: list[str] = []
    produced = 0

    for byte in data[:needed_bytes]:
        for shift in range(7, -1, -1):
            if produced == bit_len:
                break
            bits.append("1" if ((byte >> shift) & 1) == 1 else "0")
            produced += 1

    return "".join(bits)


def pack_huffman(freq: dict[str, int], bits: str) -> bytes:
    """
    Pack Huffman-compressed data into the project binary container format.

    Format:
        header
        k (uint32)
        repeated k times:
            char_len (uint16) + char_bytes (UTF-8) + freq (uint32)
        bit_len (uint32)
        packed_bits (bytes)
    """
    payload = bytearray()
    payload += _pack_header("huffman")

    # Deterministic ordering improves reproducibility (useful for comparisons).
    items = sorted(freq.items(), key=lambda x: x[0])

    payload += struct.pack(">I", len(items))

    for ch, f in items:
        if f < 0:
            raise StorageError("Invalid frequency table: negative frequency.")
        ch_bytes = ch.encode("utf-8")
        if len(ch_bytes) > 65535:
            raise StorageError("Character encoding too long to store.")
        payload += struct.pack(">H", len(ch_bytes))
        payload += ch_bytes
        payload += struct.pack(">I", int(f))

    bit_len, packed = pack_bits(bits)
    payload += struct.pack(">I", bit_len)
    payload += packed
    return bytes(payload)


def unpack_huffman(data: bytes) -> tuple[dict[str, int], str]:
    """Unpack Huffman frequency table and bitstring from container bytes."""
    alg, pos = _unpack_header(data)
    if alg != "huffman":
        raise StorageError("Data is not Huffman-compressed.")

    if len(data) < pos + 4:
        raise StorageError("Invalid Huffman data: missing symbol count.")
    (k,) = struct.unpack(">I", data[pos: pos + 4])
    pos += 4

    freq: dict[str, int] = {}
    for _ in range(k):
        if len(data) < pos + 2:
            raise StorageError("Invalid Huffman data: missing char length.")
        (ch_len,) = struct.unpack(">H", data[pos: pos + 2])
        pos += 2

        if len(data) < pos + ch_len + 4:
            raise StorageError(
                "Invalid Huffman data: incomplete char/freq entry.")

        ch_bytes = data[pos: pos + ch_len]
        pos += ch_len
        ch = ch_bytes.decode("utf-8")

        (f,) = struct.unpack(">I", data[pos: pos + 4])
        pos += 4
        freq[ch] = f

    if len(data) < pos + 4:
        raise StorageError("Invalid Huffman data: missing bit length.")
    (bit_len,) = struct.unpack(">I", data[pos: pos + 4])
    pos += 4

    bits = unpack_bits(bit_len, data[pos:])
    return freq, bits


def pack_lz78(tokens: list[LZ78Token]) -> bytes:
    """
    Pack LZ78 tokens into the project binary container format.

    Format:
        header
        n_tokens (uint32)
        repeated n times:
            index (uint32)
            char_len (uint16) + char_bytes (UTF-8)
    """
    payload = bytearray()
    payload += _pack_header("lz78")
    payload += struct.pack(">I", len(tokens))

    for tok in tokens:
        if not isinstance(tok, list) or len(tok) != 2:
            raise StorageError(
                "Invalid token format for packing. Expected [index, char].")

        idx, ch = tok
        if not isinstance(idx, int):
            raise StorageError("Invalid token index type for packing.")
        if idx < 0:
            raise StorageError(
                "Invalid token index for packing: negative index.")
        if not isinstance(ch, str):
            raise StorageError("Invalid token char type for packing.")

        ch_bytes = ch.encode("utf-8")
        if len(ch_bytes) > 65535:
            raise StorageError("Token character encoding too long to store.")

        payload += struct.pack(">I", idx)
        payload += struct.pack(">H", len(ch_bytes))
        payload += ch_bytes

    return bytes(payload)


def unpack_lz78(data: bytes) -> list[LZ78Token]:
    """Unpack LZ78 token list from container bytes."""
    alg, pos = _unpack_header(data)
    if alg != "lz78":
        raise StorageError("Data is not LZ78-compressed.")

    if len(data) < pos + 4:
        raise StorageError("Invalid LZ78 data: missing token count.")
    (n,) = struct.unpack(">I", data[pos: pos + 4])
    pos += 4

    tokens: list[LZ78Token] = []
    for _ in range(n):
        if len(data) < pos + 4 + 2:
            raise StorageError("Invalid LZ78 data: incomplete token header.")

        (idx,) = struct.unpack(">I", data[pos: pos + 4])
        pos += 4

        (ch_len,) = struct.unpack(">H", data[pos: pos + 2])
        pos += 2

        if len(data) < pos + ch_len:
            raise StorageError(
                "Invalid LZ78 data: incomplete token char bytes.")

        ch_bytes = data[pos: pos + ch_len]
        pos += ch_len
        ch = ch_bytes.decode("utf-8")

        tokens.append([idx, ch])

    return tokens


def detect_algorithm(data: bytes) -> Algorithm:
    """Detect which algorithm was used for the given container bytes."""
    alg, _ = _unpack_header(data)
    return alg


def compress_bytes(text: str, algorithm: Algorithm = "huffman") -> bytes:
    """
    Compress a string into container bytes (binary format).

    Args:
        text: Input text.
        algorithm: "huffman" or "lz78".

    Returns:
        Compressed bytes in the container format.
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
    Decompress container bytes back into the original string.
    """
    alg = detect_algorithm(data)

    if alg == "huffman":
        freq, bits = unpack_huffman(data)
        return huff_decode(freq, bits)

    if alg == "lz78":
        tokens = unpack_lz78(data)
        return lz78_decode(tokens)

    raise StorageError(
        "Invalid compressed data: missing/unknown algorithm field.")


def compress_file(input_path: str | Path, output_path: str | Path, algorithm: Algorithm = "huffman") -> None:
    """
    Compress a UTF-8 text file into a binary compressed file.
    """
    in_path = Path(input_path)
    out_path = Path(output_path)

    text = in_path.read_text(encoding="utf-8")
    out_path.write_bytes(compress_bytes(text, algorithm=algorithm))


def decompress_file(input_path: str | Path, output_path: str | Path) -> None:
    """
    Decompress a binary compressed file into a UTF-8 text file.
    """
    in_path = Path(input_path)
    out_path = Path(output_path)

    data = in_path.read_bytes()
    out_path.write_text(decompress_bytes(data), encoding="utf-8")
