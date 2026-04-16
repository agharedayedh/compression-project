from __future__ import annotations

import struct
from pathlib import Path
from typing import Literal, TypeAlias

from .huffman.codec import decode as huff_decode
from .huffman.codec import encode as huff_encode
from .lz78.codec import decode as lz78_decode
from .lz78.codec import encode as lz78_encode

# Supported compression algorithms
Algorithm = Literal["huffman", "lz78"]

# LZ78 token type: [index, byte]
LZ78Token: TypeAlias = list[int]

# File format constants
_MAGIC = b"CPRJ"       # magic bytes to identify file format
_VERSION = 1           # format version

# Mapping between algorithm names and IDs stored in file
_ALG_TO_ID: dict[str, int] = {"huffman": 1, "lz78": 2}
_ID_TO_ALG: dict[int, str] = {1: "huffman", 2: "lz78"}

# Bit sizes used in LZ78 storage
_LZ78_MARKER_BITS = 1
_LZ78_BYTE_BITS = 8


class StorageError(ValueError):
    """
    Raised when compressed binary data is invalid
    or cannot be read correctly.
    """


def _pack_header(algorithm: Algorithm) -> bytes:
    """
    Create the file header.

    The header contains:
    - magic bytes
    - version number
    - algorithm identifier

    Args:
        algorithm (Algorithm): Algorithm name.

    Returns:
        bytes: Packed header.
    """
    return _MAGIC + struct.pack(">BB", _VERSION, _ALG_TO_ID[algorithm])


def _unpack_header(data: bytes) -> tuple[Algorithm, int]:
    """
    Read and validate the file header.

    Args:
        data (bytes): Input binary data.

    Returns:
        tuple[Algorithm, int]:
            - detected algorithm
            - position where payload starts

    Raises:
        StorageError: If header is invalid.
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
    Convert a string of bits ("0" and "1") into real bytes.

    Args:
        bitstring (str): Binary string.

    Returns:
        tuple[int, bytes]:
            - number of valid bits
            - packed bytes
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
    filled = 0

    for b in bitstring:
        current = (current << 1) | (1 if b == "1" else 0)
        filled += 1

        if filled == 8:
            out.append(current)
            current = 0
            filled = 0

    # pad remaining bits if needed
    if filled != 0:
        current <<= (8 - filled)
        out.append(current)

    return bit_len, bytes(out)


def unpack_bits(bit_len: int, data: bytes) -> str:
    """
    Convert bytes back into a bitstring.

    Args:
        bit_len (int): Number of valid bits.
        data (bytes): Packed bytes.

    Returns:
        str: Bitstring of length bit_len.
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
            bits.append("1" if ((byte >> shift) & 1) else "0")
            produced += 1

    return "".join(bits)


def _read_bits(bits: str, pos: int, n: int) -> tuple[str, int]:
    """
    Read n bits from a bitstring starting at position pos.

    Args:
        bits (str): Bitstring.
        pos (int): Current position.
        n (int): Number of bits to read.

    Returns:
        tuple[str, int]: (read bits, new position)
    """
    end = pos + n
    if end > len(bits):
        raise StorageError("Invalid bit-packed data: truncated payload.")
    return bits[pos:end], end


def _lz78_index_width(next_index: int) -> int:
    """
    Calculate how many bits are needed to store the current index.

    Args:
        next_index (int): Next dictionary index.

    Returns:
        int: Required bit width.
    """
    return max(1, (next_index - 1).bit_length())


def pack_huffman(freq: dict[str, int], bits: str) -> bytes:
    """
    Store Huffman compressed data into binary format.

    Args:
        freq (dict[str, int]): Frequency table.
        bits (str): Encoded bitstring.

    Returns:
        bytes: Binary representation.
    """
    payload = bytearray()
    payload += _pack_header("huffman")

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
    """
    Read Huffman compressed data from binary format.

    Args:
        data (bytes): Input binary data.

    Returns:
        tuple[dict[str, int], str]:
            - frequency table
            - bitstring
    """
    alg, pos = _unpack_header(data)
    if alg != "huffman":
        raise StorageError("Data is not Huffman-compressed.")

    if len(data) < pos + 4:
        raise StorageError("Invalid Huffman data: missing symbol count.")
    (k,) = struct.unpack(">I", data[pos:pos + 4])
    pos += 4

    freq: dict[str, int] = {}

    for _ in range(k):
        if len(data) < pos + 2:
            raise StorageError("Invalid Huffman data: missing char length.")
        (ch_len,) = struct.unpack(">H", data[pos:pos + 2])
        pos += 2

        if len(data) < pos + ch_len + 4:
            raise StorageError(
                "Invalid Huffman data: incomplete char/freq entry.")

        ch_bytes = data[pos:pos + ch_len]
        pos += ch_len

        try:
            ch = ch_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            raise StorageError(
                "Invalid Huffman data: invalid UTF-8 character bytes.") from e

        (f,) = struct.unpack(">I", data[pos:pos + 4])
        pos += 4
        freq[ch] = f

    if len(data) < pos + 4:
        raise StorageError("Invalid Huffman data: missing bit length.")
    (bit_len,) = struct.unpack(">I", data[pos:pos + 4])
    pos += 4

    bits = unpack_bits(bit_len, data[pos:])
    return freq, bits


def pack_lz78(tokens: list[LZ78Token]) -> bytes:
    """
    Store LZ78 tokens in compact binary format.

    Uses:
    - variable-length index
    - marker bit
    - optional byte

    Args:
        tokens (list[LZ78Token]): LZ78 tokens.

    Returns:
        bytes: Packed binary data.
    """
    payload = bytearray()
    payload += _pack_header("lz78")
    payload += struct.pack(">I", len(tokens))

    parts: list[str] = []
    next_index = 1

    for i, tok in enumerate(tokens):
        if not isinstance(tok, list) or len(tok) != 2:
            raise StorageError(
                "Invalid token format for packing. Expected [index, byte].")

        idx, byte_value = tok

        if not isinstance(idx, int):
            raise StorageError("Invalid token index type for packing.")
        if not isinstance(byte_value, int):
            raise StorageError("Invalid token byte type for packing.")
        if idx < 0:
            raise StorageError(
                f"Invalid token index for packing: {idx} must be non-negative.")

        width = _lz78_index_width(next_index)
        max_ref = next_index - 1
        if idx > max_ref:
            raise StorageError(
                f"Invalid token index for packing: {idx} exceeds current dictionary max {max_ref}."
            )

        parts.append(f"{idx:0{width}b}")

        if byte_value == -1:
            if i != len(tokens) - 1:
                raise StorageError(
                    "Invalid token for packing: -1 byte is only allowed in final token.")
            parts.append("1")
        else:
            if not 0 <= byte_value <= 255:
                raise StorageError(
                    f"Invalid token byte for packing: {byte_value} not in 0..255 or -1."
                )
            parts.append("0")
            parts.append(f"{byte_value:08b}")
            next_index += 1

    bit_len, packed = pack_bits("".join(parts))
    payload += struct.pack(">I", bit_len)
    payload += packed
    return bytes(payload)


def unpack_lz78(data: bytes) -> list[LZ78Token]:
    """
    Read LZ78 tokens from binary format.

    Args:
        data (bytes): Input binary data.

    Returns:
        list[LZ78Token]: List of tokens.
    """
    alg, pos = _unpack_header(data)
    if alg != "lz78":
        raise StorageError("Data is not LZ78-compressed.")

    if len(data) < pos + 4:
        raise StorageError("Invalid LZ78 data: missing token count.")
    (n,) = struct.unpack(">I", data[pos:pos + 4])
    pos += 4

    if len(data) < pos + 4:
        raise StorageError("Invalid LZ78 data: missing payload bit length.")
    (bit_len,) = struct.unpack(">I", data[pos:pos + 4])
    pos += 4

    bits = unpack_bits(bit_len, data[pos:])
    bit_pos = 0
    tokens: list[LZ78Token] = []
    next_index = 1

    for token_i in range(n):
        width = _lz78_index_width(next_index)

        idx_bits, bit_pos = _read_bits(bits, bit_pos, width)
        marker_bits, bit_pos = _read_bits(bits, bit_pos, _LZ78_MARKER_BITS)

        idx = int(idx_bits, 2)
        marker = int(marker_bits, 2)

        max_ref = next_index - 1
        if idx > max_ref:
            raise StorageError(
                "Invalid LZ78 data: token index exceeds current dictionary.")

        if marker == 1:
            if token_i != n - 1:
                raise StorageError(
                    "Invalid LZ78 data: final-token marker used before the end.")
            tokens.append([idx, -1])
            continue

        byte_bits, bit_pos = _read_bits(bits, bit_pos, _LZ78_BYTE_BITS)
        byte_value = int(byte_bits, 2)
        tokens.append([idx, byte_value])
        next_index += 1

    if any(bit != "0" for bit in bits[bit_pos:]):
        raise StorageError("Invalid LZ78 data: non-zero trailing bits.")

    return tokens


def detect_algorithm(data: bytes) -> Algorithm:
    """
    Detect which algorithm was used for compression.

    Args:
        data (bytes): Input binary data.

    Returns:
        Algorithm: Detected algorithm name.
    """
    alg, _ = _unpack_header(data)
    return alg


def compress_bytes(text: str, algorithm: Algorithm = "huffman") -> bytes:
    """
    Compress text into binary format.

    Args:
        text (str): Input text.
        algorithm (Algorithm): Compression method.

    Returns:
        bytes: Compressed binary data.
    """
    if algorithm == "huffman":
        freq, bits = huff_encode(text)
        return pack_huffman(freq, bits)

    if algorithm == "lz78":
        raw = text.encode("utf-8")
        tokens = lz78_encode(raw)
        return pack_lz78(tokens)

    raise ValueError(f"Unknown algorithm: {algorithm}")


def decompress_bytes(data: bytes) -> str:
    """
    Decompress binary data back into text.

    Args:
        data (bytes): Compressed data.

    Returns:
        str: Decompressed text.
    """
    alg = detect_algorithm(data)

    try:
        if alg == "huffman":
            freq, bits = unpack_huffman(data)
            return huff_decode(freq, bits)

        if alg == "lz78":
            tokens = unpack_lz78(data)
            raw = lz78_decode(tokens)
            return raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise StorageError(
            "Invalid compressed data: decompressed bytes are not valid UTF-8.") from e
    except ValueError as e:
        raise StorageError(f"Invalid compressed data: {e}") from e

    raise StorageError(
        "Invalid compressed data: missing/unknown algorithm field.")


def compress_file(
    input_path: str | Path,
    output_path: str | Path,
    algorithm: Algorithm = "huffman",
) -> None:
    """
    Compress a text file and save the result.

    Args:
        input_path (str | Path): Input file path.
        output_path (str | Path): Output file path.
        algorithm (Algorithm): Compression method.

    Returns:
        None
    """
    in_path = Path(input_path)
    out_path = Path(output_path)

    text = in_path.read_text(encoding="utf-8")
    out_path.write_bytes(compress_bytes(text, algorithm=algorithm))


def decompress_file(input_path: str | Path, output_path: str | Path) -> None:
    """
    Decompress a binary file and save the restored text.

    Args:
        input_path (str | Path): Compressed file path.
        output_path (str | Path): Output file path.

    Returns:
        None
    """
    in_path = Path(input_path)
    out_path = Path(output_path)

    data = in_path.read_bytes()
    out_path.write_text(decompress_bytes(data), encoding="utf-8")
