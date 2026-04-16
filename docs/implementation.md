# Implementation Document

---

## Program Structure

The project is implemented as a modular Python package located under:

```
src/compression
```

The structure separates compression algorithms, binary storage, and user interaction.

---

## Main Components

### `compression/huffman/codec.py`

Implements **Huffman coding**:

- frequency table construction  
- Huffman tree construction using a priority queue  
- code table generation  
- encoding and decoding functions  
- strict validation during decoding to detect invalid bitstreams  

---

### `compression/lz78/codec.py`

Implements the **LZ78 dictionary-based compression algorithm**:

- operates on raw bytes instead of characters  
- incremental dictionary construction  
- token-based encoding using `(index, byte)` pairs  
- dictionary-driven decoding  
- support for a final token representing leftover phrases  

The implementation uses a **variable-length index representation**, where the number of bits used for dictionary references grows dynamically as the dictionary expands.

---

### `compression/storage.py`

Responsible for binary serialization and deserialization:

- defines a custom binary container format  
- stores algorithm identifier and version  
- packs Huffman bitstrings into bytes  
- stores LZ78 data using bit-level encoding with variable-length indexes  
- automatically detects algorithm during decompression  

---

### `compression/main.py`

Provides the command-line interface:

- `compress` command  
- `decompress` command  
- file-based pipeline  
- compression ratio reporting  

---

## Modular Design Benefits

- independent testing of algorithms  
- clear separation between compression logic and binary storage  
- easy extensibility for additional algorithms in the future  

---

# Achieved Time and Space Complexities

---

## Huffman Coding

Let:

- \( n \) = number of unique symbols  
- \( m \) = total length of input text  

### Time Complexity

- Frequency table construction: \( O(m) \)  
- Huffman tree construction: \( O(n \log n) \)  
- Encoding: \( O(m) \)  
- Decoding: \( O(m) \)  

### Overall

\[
O(m + n \log n)
\]

---

### Space Complexity

- frequency table: \( O(n) \)  
- Huffman tree: \( O(n) \)  
- encoded representation: \( O(m) \)  

### Overall

\[
O(m + n)
\]

---

## LZ78

Let:

- \( m \) = length of input data in bytes  
- \( k \) = number of dictionary entries  

### Time Complexity

#### Encoding

Each byte is processed once, and dictionary lookups are average \( O(1) \):

\[
O(m)
\]

#### Decoding

Each token is processed once:

\[
O(m)
\]

---

### Space Complexity

The dictionary grows dynamically:

\[
O(k) \le O(m)
\]

---

# Performance and Big-O Comparison

Huffman coding and LZ78 represent two fundamentally different approaches:

| Algorithm | Type | Strength |
|----------|------|----------|
| Huffman | Entropy-based | Performs well when character frequencies are skewed |
| LZ78 | Dictionary-based | Performs well when repeated substrings exist |

---

## Asymptotic Comparison

- Huffman: \( O(m + n \log n) \)  
- LZ78: \( O(m) \)  

In practice, both are efficient.

Compression performance depends strongly on:

- character frequency distribution  
- repetition patterns  
- input structure  

---

# Empirical Compression Ratio Comparison

Empirical evaluation was performed using natural-language text collected from multiple independent sources.

### Corpus Sources

- Wikipedia articles  
- Project Gutenberg books  

This avoids artificial repetition and better represents realistic input.

---

## Results Table

| Input | Original (B) | Huffman (B) | LZ78 (B) | H ratio | L ratio |
|------|-------------|-------------|----------|---------|---------|
| 1kB  | 1030        | 817         |      815 | 0.793 | 0.791 |
| 4kB  | 4118        | 2646 | 2886 | 0.643 | 0.701 |
| 16kB | 16525       | 9618 | 10465 | 0.582 | 0.633 |
| 64kB | 66075       | 37490 | 38765 | 0.567 | 0.587 |
| 256kB| 265516      | 148780 | 148122 | 0.560 | 0.558 |
| 1MB  | 1066911     | 586648 | 546885 | 0.550 | 0.513 |
| 4MB  | 4309826     | 2441763 | 2075502 | 0.567 | 0.482 |
| 16MB | 17182048    | 9916013 | 7901506 | 0.577 | 0.460 |

---

## Observations

- Huffman achieves stable compression ratios (~0.55–0.58)  
- LZ78 performs weaker on small inputs due to dictionary overhead  
- LZ78 improves significantly as input size increases  
- For large inputs, LZ78 reaches ~0.45–0.50  
- Variable-length indexes improve LZ78 efficiency  
- Results reflect realistic natural-language behavior  

---

# Binary Storage Design

Compressed data is stored in a custom binary container format.

---

## Header

- magic bytes (`CPRJ`)  
- version number  
- algorithm identifier  

---

## Payload

### Huffman

- symbol count  
- UTF-8 characters with frequencies  
- bit length  
- packed bitstream  

### LZ78

- token count  
- bit-packed token stream  

Each token is encoded as:

- variable-length index  
- 1-bit marker  
- optional 8-bit byte  

This ensures minimal storage overhead.

---

## Bit-Level Encoding

Both algorithms use bit-level packing:

- Huffman → variable-length codes  
- LZ78 → variable-length indexes  

This avoids:

- storing data as text (`"0"` / `"1"`)  
- unnecessary padding  
- fixed-width overhead  

---

# Possible Shortcomings and Improvements

Possible improvements include:

- limiting dictionary size in LZ78  
- canonical Huffman codes  
- stream-based compression  
- additional compression algorithms  

### Limitation

> LZ78 dictionary growth may increase memory usage for very large inputs.

---

# Use of Large Language Models

ChatGPT was used for:

- improving documentation language  
- discussing testing strategy  
- verifying clarity of explanations  

All implementation decisions and code were created and verified independently.

---

# Sources

- Cormen et al., *Introduction to Algorithms*  
- Salomon, D., *Handbook of Data Compression*  
- Wikipedia: Huffman coding  
- Wikipedia: LZ78  
- Python documentation
- Project Gutenberg: https://www.gutenberg.org/  
- Wikipedia Articles: https://www.wikipedia.org/ 

