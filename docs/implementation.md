# Implementation Document

## Program Structure

The project is implemented as a modular Python package located under:

```
src/compression
```

The structure follows a clear separation of concerns between algorithms, storage handling, and user interface.

### Main Components

#### `compression/huffman/codec.py`

Implements **Huffman coding**:

- Frequency table construction  
- Huffman tree construction using a priority queue  
- Code table generation  
- Encoding and decoding functions  

---

#### `compression/lz78/codec.py`

Implements the **LZ78 dictionary-based compression algorithm**:

- Incremental dictionary construction  
- Token-based encoding  
- Dictionary-driven decoding  

---

#### `compression/storage.py`

Responsible for **binary serialization and deserialization**:

- Defines a custom binary container format  
- Stores algorithm identifier and version  
- Packs Huffman bitstrings into actual bytes  
- Serializes LZ78 tokens into structured binary format  
- Automatically detects algorithm during decompression  

---

#### `compression/main.py`

Provides the **command-line interface**:

- `compress` command  
- `decompress` command  
- File-based pipeline  
- Compression ratio reporting  

---

### Modular Design Benefits

- Independent testing of algorithms  
- Clear separation between compression logic and binary storage  
- Easy extensibility for additional algorithms in the future  

---

# Achieved Time and Space Complexities

---

## Huffman Coding

Let:

- \( n \) = number of unique symbols  
- \( m \) = total length of input text  

### Time Complexity

1. **Frequency table construction**  
   \( O(m) \)

2. **Building the Huffman tree using a priority queue**  
   \( O(n \log n) \)

3. **Encoding the text**  
   \( O(m) \)

4. **Decoding the bitstring**  
   \( O(m) \)

### Overall Complexity

\[
O(m + n \log n)
\]

In typical text input, \( n \) (unique characters) is small compared to \( m \).

---

### Space Complexity

- Frequency table: \( O(n) \)  
- Huffman tree: \( O(n) \)  
- Encoded bit representation: \( O(m) \)  

### Overall

\[
O(m + n)
\]

---

## LZ78

Let:

- \( m \) = length of input string  
- \( k \) = number of dictionary entries  

---

### Time Complexity

#### Encoding

- Each character processed once  
- Dictionary lookups are average \( O(1) \)

\[
O(m)
\]

#### Decoding

- Each token processed once  
- Dictionary reconstruction incremental  

\[
O(m)
\]

---

### Space Complexity

- Dictionary grows dynamically  
- Worst case: one new entry per character  

\[
O(k) \le O(m)
\]

---

# Performance and Big-O Comparison

Huffman coding and LZ78 represent two fundamentally different approaches:

| Algorithm | Type | Strength |
|-----------|------|----------|
| Huffman | Entropy-based | Performs well when character frequencies are skewed |
| LZ78 | Dictionary-based | Performs well when repeated substrings exist |

---

## Asymptotic Comparison

- **Huffman:** \( O(m + n \log n) \)  
- **LZ78:** \( O(m) \)

In practice, both are efficient for realistic file sizes.

However, actual compression ratio depends strongly on input characteristics:

- Alphabet size  
- Repetition patterns  
- Text structure  

---

# Empirical Compression Ratio Comparison 

Empirical evaluation was performed using natural-language text.

For each target size (1kB–16MB), the same base text was repeated to generate equal-sized inputs. Both algorithms were applied to the exact same files.

| Input size | Original (B) | Huffman (B) | LZ78 (B) | Huffman ratio | LZ78 ratio |
|------------|-------------|-------------|----------|----------------|------------|
| 1kB | 1039 | 849 | 2823 | 0.817 | 2.717 |
| 4kB | 4159 | 2618 | 8935 | 0.629 | 2.148 |
| 16kB | 16639 | 9407 | 26805 | 0.565 | 1.611 |
| 64kB | 66561 | 36546 | 74769 | 0.549 | 1.123 |
| 256kB | 266245 | 145117 | 190514 | 0.545 | 0.716 |
| 1MB | 1064978 | 579392 | 440534 | 0.544 | 0.414 |
| 4MB | 4259917 | 2316497 | 950570 | 0.544 | 0.223 |
| 16MB | 17039666 | 9264901 | 1973586 | 0.544 | 0.116 |

---

## Observations

- Huffman stabilizes around **~0.54 compression ratio** for larger inputs.  
- LZ78 performs poorly on small files due to dictionary overhead.  
- LZ78 improves significantly as file size increases.  
- For large repeated natural-language text, LZ78 achieves better ratios than Huffman.  

Runtime benchmarking was not performed, Python is not optimized for performance benchmarking.

---

# Binary Storage Design

Compressed data is stored in a **custom binary container format**.

## Header

- Magic bytes (`CPRJ`)  
- Version number  
- Algorithm identifier  

---

## Payload

### Huffman

- Symbol count  
- UTF-8 encoded characters with frequencies  
- Bit length  
- Packed bitstream (true bit-level packing into bytes)  

### LZ78

- Token count  
- For each token:
  - Index  
  - UTF-8 character bytes  

Huffman bitstrings are packed at the bit level into actual bytes, ensuring real binary storage instead of textual `"0"` / `"1"` strings.

This guarantees that compressed files:

- Remain valid after program exit  
- Contain no JSON or text-based structures  
- Are independent of runtime memory structures  

---

# Possible Shortcomings and Improvements

While the implementation satisfies correctness, possible improvements include:

- More memory-efficient dictionary structures for LZ78  
- Canonical Huffman codes for better determinism  
- Stream-based compression (currently whole-file based)  
- Runtime benchmarking for research purposes  
- Adding additional compression algorithms for broader comparison  

---

# Use of Large Language Models

ChatGPT (GPT-4 class model) was used for:

- Reviewing and refining documentation language  
- Discussing test strategy improvements  
- Clarifying theoretical complexity reasoning  

Large language models were **not** used to generate final algorithm implementations.

All compression logic, storage design, and testing structure were designed and implemented independently by the author.

---

# Sources

The following sources were used:

- Cormen et al., *Introduction to Algorithms*  
- Salomon, D., *Handbook of Data Compression*  
- Wikipedia: Huffman coding  
- Wikipedia: LZ78  
- Python documentation  
- Stack Overflow discussions related to Huffman tree storage

Only sources directly relevant to the implementation and algorithm design are listed.

