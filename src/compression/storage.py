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
    """
    This error is raised when compressed binary data is invalid
    or cannot be read correctly.
    """


def _pack_header(algorithm: Algorithm) -> bytes:
    """
    This function creates the header for the compressed binary format.

    The header stores:
    - magic bytes to identify the file format
    - version number
    - algorithm id

    Args:
        algorithm (Algorithm): The compression algorithm used.

    Returns:
        bytes: The packed header as bytes.
    """
    return _MAGIC + struct.pack(">BB", _VERSION, _ALG_TO_ID[algorithm])


def _unpack_header(data: bytes) -> tuple[Algorithm, int]:
    """
    This function reads and checks the header of compressed data.

    It makes sure that:
    - the file is long enough
    - the magic header is correct
    - the version is supported
    - the algorithm id is known

    Args:
        data (bytes): The compressed binary data.

    Returns:
        tuple[Algorithm, int]:
            - the algorithm name
            - the position where the actual payload starts

    Raises:
        StorageError: If the header is invalid.
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
    This function packs a bit string made of '0' and '1' into bytes.

    Because bytes store 8 bits each, this function groups the bits
    into bytes and adds padding to the last byte if needed.

    Args:
        bitstring (str): A string containing only '0' and '1'.

    Returns:
        tuple[int, bytes]:
            - the original number of valid bits
            - the packed bytes

    Raises:
        StorageError: If the bit string contains characters other than
        '0' and '1'.
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
    filled = 0  # how many bits are currently stored in this byte

    for b in bitstring:
        current = (current << 1) | (1 if b == "1" else 0)
        filled += 1
        if filled == 8:
            out.append(current)
            current = 0
            filled = 0

    if filled != 0:
        current = current << (8 - filled)  # pad remaining bits on the right
        out.append(current)

    return bit_len, bytes(out)


def unpack_bits(bit_len: int, data: bytes) -> str:
    """
    This function unpacks bytes back into a bit string of '0' and '1'.

    The stored bit length is needed because the last byte may contain
    extra padding bits that should not be included.

    Args:
        bit_len (int): Number of valid bits in the data.
        data (bytes): Packed bytes.

    Returns:
        str: The unpacked bit string.

    Raises:
        StorageError: If the bit length is invalid or there are not enough bytes.
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
    This function stores Huffman compressed data in the project binary format.

    The stored data includes:
    - the file header
    - the frequency table
    - the bit length
    - the packed bit data

    Args:
        freq (dict[str, int]): Frequency table of characters.
        bits (str): Huffman encoded bit string.

    Returns:
        bytes: Huffman compressed data in binary container format.

    Raises:
        StorageError: If the frequency table or character data is invalid.
    """
    payload = bytearray()
    payload += _pack_header("huffman")

    # Sort items to keep the output deterministic
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
    This function reads Huffman compressed data from the binary container.

    It extracts:
    - the frequency table
    - the encoded bit string

    Args:
        data (bytes): The compressed binary data.

    Returns:
        tuple[dict[str, int], str]:
            - the frequency table
            - the Huffman encoded bit string

    Raises:
        StorageError: If the data is incomplete or not valid Huffman data.
    """
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
    This function stores LZ78 tokens in the project binary format.

    The stored data includes:
    - the file header
    - number of tokens
    - each token's index and character

    Args:
        tokens (list[LZ78Token]): List of LZ78 tokens.

    Returns:
        bytes: LZ78 compressed data in binary container format.

    Raises:
        StorageError: If a token is invalid or cannot be stored.
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
    """
    This function reads LZ78 compressed data from the binary container.

    It extracts the list of tokens stored in the file.

    Args:
        data (bytes): The compressed binary data.

    Returns:
        list[LZ78Token]: The unpacked list of LZ78 tokens.

    Raises:
        StorageError: If the data is incomplete or not valid LZ78 data.
    """
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
    """
    This function checks which compression algorithm was used
    in the binary container.

    Args:
        data (bytes): The compressed binary data.

    Returns:
        Algorithm: Either "huffman" or "lz78".
    """
    alg, _ = _unpack_header(data)
    return alg


def compress_bytes(text: str, algorithm: Algorithm = "huffman") -> bytes:
    """
    This function compresses a text string into binary container bytes.

    Depending on the selected algorithm, it uses either Huffman coding
    or LZ78 and then stores the result in the project binary format.

    Args:
        text (str): Input text to compress.
        algorithm (Algorithm): Compression method to use.

    Returns:
        bytes: The compressed data in binary container format.

    Raises:
        ValueError: If the algorithm name is not supported.
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
    This function decompresses binary container data back into text.

    It first detects which algorithm was used and then calls
    the correct decompression method.

    Args:
        data (bytes): The compressed binary data.

    Returns:
        str: The original decompressed text.

    Raises:
        StorageError: If the data format is invalid.
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
    This function compresses a UTF-8 text file into a binary file.

    Args:
        input_path (str | Path): Path to the input text file.
        output_path (str | Path): Path where the compressed file will be saved.
        algorithm (Algorithm): Compression algorithm to use.

    Returns:
        None
    """
    in_path = Path(input_path)
    out_path = Path(output_path)

    text = in_path.read_text(encoding="utf-8")
    out_path.write_bytes(compress_bytes(text, algorithm=algorithm))


def decompress_file(input_path: str | Path, output_path: str | Path) -> None:
    """
    This function decompresses a binary compressed file back into a UTF-8 text file.

    Args:
        input_path (str | Path): Path to the compressed binary file.
        output_path (str | Path): Path where the decompressed text file will be saved.

    Returns:
        None
    """
    in_path = Path(input_path)
    out_path = Path(output_path)

    data = in_path.read_bytes()
    out_path.write_text(decompress_bytes(data), encoding="utf-8")
