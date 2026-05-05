from __future__ import annotations

from compression.storage import _lz78_index_width

import struct

from compression.storage import (
    pack_bits,
    unpack_bits,
    pack_huffman,
    unpack_huffman,
    pack_lz78,
    unpack_lz78,
)


def test_pack_bits_without_padding() -> None:
    """
    Test bit packing when the bitstring length is exactly one byte.

    In this case, no padding bits are needed.
    """
    bits = "10101010"

    bit_len, packed = pack_bits(bits)
    restored = unpack_bits(bit_len, packed)

    assert bit_len == 8
    assert len(packed) == 1
    assert restored == bits


def test_pack_bits_with_padding() -> None:
    """
    Test bit packing when the bitstring length is not a multiple of 8.

    In this case, padding bits are added internally, but unpacking
    should return only the original valid bits.
    """
    bits = "10101"

    bit_len, packed = pack_bits(bits)
    restored = unpack_bits(bit_len, packed)

    assert bit_len == 5
    assert len(packed) == 1
    assert restored == bits


def test_huffman_packed_bits_for_small_case() -> None:
    """
    Test that a small Huffman bitstring is packed correctly.

    The bitstring "1110" should be stored as one byte with padding.
    """
    freq = {"a": 3, "b": 1}
    bits = "1110"

    packed_data = pack_huffman(freq, bits)
    unpacked_freq, unpacked_bits = unpack_huffman(packed_data)

    assert unpacked_freq == freq
    assert unpacked_bits == bits


def test_lz78_exact_bitstream_for_aaa() -> None:
    """
    Test the exact bitstream for a small LZ78 example.

    Tokens for b"aaa" are:
        [0, 97], [1, 97]

    With variable-length indexes, the expected bitstream is:
        0 + 0 + 01100001
        1 + 0 + 01100001
    """
    tokens = [[0, 97], [1, 97]]
    packed_data = pack_lz78(tokens)

    bit_len = struct.unpack(">I", packed_data[10:14])[0]
    payload = packed_data[14:]
    bits = unpack_bits(bit_len, payload)

    expected_bits = (
        "0" + "0" + "01100001"
        + "1" + "0" + "01100001"
    )

    assert bit_len == len(expected_bits)
    assert bits == expected_bits
    assert unpack_lz78(packed_data) == tokens


def test_lz78_exact_bitstream_for_final_leftover_token() -> None:
    """
    Test the exact bitstream when LZ78 uses the final -1 marker.

    Tokens for b"aaaa" are:
        [0, 97], [1, 97], [1, -1]

    The last token uses marker bit 1 and stores no byte after it.
    """
    tokens = [[0, 97], [1, 97], [1, -1]]
    packed_data = pack_lz78(tokens)

    bit_len = struct.unpack(">I", packed_data[10:14])[0]
    payload = packed_data[14:]
    bits = unpack_bits(bit_len, payload)

    expected_bits = (
        "0" + "0" + "01100001"
        + "1" + "0" + "01100001"
        + "01" + "1"
    )

    assert bit_len == len(expected_bits)
    assert bits == expected_bits
    assert unpack_lz78(packed_data) == tokens


def test_lz78_index_width_boundaries() -> None:
    """
    Test that the LZ78 index width calculation is correct.

    The index width depends on how many dictionary entries exist.
    As the dictionary grows, the number of bits needed to store the index increases.

    This test checks key boundary points where the width should increase:
    - 1 → still 1 bit
    - 2 → still 1 bit
    - 3 → becomes 2 bits
    - 5 → becomes 3 bits
    - 9 → becomes 4 bits
    - 17 → becomes 5 bits

    These boundaries are important because errors often happen when
    the bit width increases.
    """
    assert _lz78_index_width(1) == 1
    assert _lz78_index_width(2) == 1
    assert _lz78_index_width(3) == 2
    assert _lz78_index_width(5) == 3
    assert _lz78_index_width(9) == 4
    assert _lz78_index_width(17) == 5
