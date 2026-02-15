from __future__ import annotations

import struct
from typing import Literal

Algorithm = Literal["huffman", "lz78"]

# Binary container format:
# magic (4 bytes) + version (1 byte) + algorithm_id (1 byte)
# magic = b"CPRJ"  (Compression PRoJect)
_MAGIC = b"CPRJ"
_VERSION = 1

_ALG_TO_ID: dict[str, int] = {"huffman": 1, "lz78": 2}
_ID_TO_ALG: dict[int, str] = {1: "huffman", 2: "lz78"}


class StorageError(ValueError):
    """Raised when compressed bytes are invalid or cannot be parsed."""


def _pack_header(algorithm: Algorithm) -> bytes:
    return _MAGIC + struct.pack(">BB", _VERSION, _ALG_TO_ID[algorithm])


def _unpack_header(data: bytes) -> tuple[Algorithm, int]:
    if len(data) < 6:
        raise StorageError("Invalid data: too short for header.")
    if data[:4] != _MAGIC:
        raise StorageError("Invalid data: wrong magic header.")
    version, alg_id = struct.unpack(">BB", data[4:6])
    if version != _VERSION:
        raise StorageError(f"Unsupported format version: {version}")
    if alg_id not in _ID_TO_ALG:
        raise StorageError(f"Unknown algorithm id: {alg_id}")
    alg = _ID_TO_ALG[alg_id]
    return alg, 6


def pack_bits(bitstring: str) -> tuple[int, bytes]:
    """
    Pack a string like '010011' into bytes.
    Returns (bit_length, packed_bytes).
    """
    bit_len = len(bitstring)
    if bit_len == 0:
        return 0, b""

    # Validate input
    for ch in bitstring:
        if ch not in ("0", "1"):
            raise StorageError(
                "Invalid bitstring: contains non-binary characters.")

    out = bytearray()
    current = 0
    filled = 0  # bits filled into current byte

    for b in bitstring:
        current = (current << 1) | (1 if b == "1" else 0)
        filled += 1
        if filled == 8:
            out.append(current)
            current = 0
            filled = 0

    if filled != 0:
        # shift remaining bits to the left so they occupy the high bits
        current = current << (8 - filled)
        out.append(current)

    return bit_len, bytes(out)


def unpack_bits(bit_len: int, data: bytes) -> str:
    """Unpack bytes back into a '0'/'1' bitstring using the stored bit length."""
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
    Binary format for Huffman:
    header
    k (uint32)
    repeated k times:
        char_len (uint16) + char_bytes + freq (uint32)
    bit_len (uint32)
    packed_bits (bytes)
    """
    payload = bytearray()
    payload += _pack_header("huffman")

    # number of distinct symbols
    payload += struct.pack(">I", len(freq))

    for ch, f in freq.items():
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


def pack_lz78(tokens: list[list[object]]) -> bytes:
    """
    Binary format for LZ78:
    header
    n_tokens (uint32)
    repeated n times:
        index (uint32)
        char_len (uint16) + char_bytes (UTF-8)
    """
    payload = bytearray()
    payload += _pack_header("lz78")
    payload += struct.pack(">I", len(tokens))

    for t in tokens:
        if not isinstance(t, list) or len(t) != 2:
            raise StorageError(
                "Invalid token format for packing. Expected [index, char].")
        idx, ch = t
        if not isinstance(idx, int):
            raise StorageError("Invalid token index type for packing.")
        if not isinstance(ch, str):
            raise StorageError("Invalid token char type for packing.")

        ch_bytes = ch.encode("utf-8")
        if len(ch_bytes) > 65535:
            raise StorageError("Token character encoding too long to store.")

        payload += struct.pack(">I", idx)
        payload += struct.pack(">H", len(ch_bytes))
        payload += ch_bytes

    return bytes(payload)


def unpack_lz78(data: bytes) -> list[list[object]]:
    alg, pos = _unpack_header(data)
    if alg != "lz78":
        raise StorageError("Data is not LZ78-compressed.")

    if len(data) < pos + 4:
        raise StorageError("Invalid LZ78 data: missing token count.")
    (n,) = struct.unpack(">I", data[pos: pos + 4])
    pos += 4

    tokens: list[list[object]] = []
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
    alg, _ = _unpack_header(data)
    return alg
