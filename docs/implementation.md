# Implementation Document

---

## Program Structure

The project is implemented as a modular Python package located under:

```text
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

---

### `compression/lz78/codec.py`

Implements the **LZ78 dictionary-based compression algorithm**:

- incremental dictionary construction  
- token-based encoding  
- dictionary-driven decoding  

---

### `compression/storage.py`

Responsible for binary serialization and deserialization:

- defines a custom binary container format  
- stores algorithm identifier and version  
- packs Huffman bitstrings into bytes  
- serializes LZ78 tokens into binary form  
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

In typical text input, \( n \) is small compared to \( m \).

---

### Space Complexity

- frequency table: \( O(n) \)  
- Huffman tree: \( O(n) \)  
- encoded bit representation: \( O(m) \)  

### Overall

\[
O(m + n)
\]

---

## LZ78

Let:

- \( m \) = length of input string  
- \( k \) = number of dictionary entries  

### Time Complexity

#### Encoding

Each character is processed once, and dictionary lookups are average \( O(1) \):

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

The dictionary grows dynamically. In the worst case:

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

In practice, both are efficient for typical file sizes.

However, compression ratio depends strongly on:

- character frequency distribution  
- repetition patterns  
- text structure  

---

# Empirical Compression Ratio Comparison

Empirical evaluation was performed using natural-language text collected from multiple sources.

Instead of repeating the same text, a corpus was constructed by combining independent text files such as articles from Wikipedia and books from Project Gutenberg. This avoids artificial repetition and better represents realistic input.

For each target size, a prefix of the corpus was used. Both algorithms were applied to the exact same inputs.

---

## Results Table

Input   Original(B)   Huffman(B)      LZ78(B)   H ratio   L ratio
--------------------------------------------------------------------
1kB            1030          817         2698     0.793     2.619
4kB            4118         2646         8767     0.643     2.129
16kB          16525         9618        29191     0.582     1.766
64kB          66075        37490        99305     0.567     1.503
256kB        265516       148780       349545     0.560     1.316
1MB         1066911       586648      1198010     0.550     1.123
4MB         4309826      2441763      4243675     0.567     0.985
16MB       17182048      9916013     15173153     0.577     0.883

---

## Observations

- Huffman coding consistently achieves stable compression ratios around 0.55–0.58 for larger inputs.
- LZ78 performs poorly on small inputs due to dictionary overhead and fixed-size (32-bit) index storage.
- As input size increases, LZ78 improves and eventually becomes effective for larger files.
- For realistic natural-language input, LZ78 does not achieve extreme compression ratios, unlike when artificial repetition is used.
- The results now reflect real-world behavior, where compression depends on actual structure and repetition in the data.

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
- for each token:
  - index  
  - UTF-8 character bytes  

---

Huffman bitstrings are packed at the bit level into actual bytes.

This ensures:

- true binary storage (no `"0"` / `"1"` strings)  
- independence from runtime structures  
- files remain valid after program exit  

---

# Possible Shortcomings and Improvements

Possible improvements include:

- limiting dictionary size in LZ78  
- Using variable-length or smaller index encoding in LZ78  
- canonical Huffman codes  
- stream-based compression  
- additional compression algorithms  

A key limitation:

> The current LZ78 implementation does not limit dictionary size, which may lead to increased memory usage.

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

Only sources directly relevant to implementation are listed.