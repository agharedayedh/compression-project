# Specification Document  
**Lossless Text Compression Project**

---

- **Study program:** Bachelor of Science (BSc)
- **Documentation language:** English

## 1. Programming Language and Peer-Review Languages

The project is implemented using **Python**.

Python was selected because it offers strong support for data structures, file handling, and automated testing, while still allowing full control over algorithmic implementations.

I am proficient in **Python** to the extent that I can peer-review projects written in Python. I am not sufficiently proficient in other programming languages to peer-review projects written in them.

---

## 2. Problem Description

The problem addressed in this project is **lossless text compression**.

Text data often contains redundancy, such as repeated characters and repeated substrings. This redundancy increases storage requirements and transmission costs. The goal of this project is to reduce the size of text files while still allowing the original text to be reconstructed **exactly** after decompression.

The project focuses on implementing classical compression algorithms and evaluating their behavior on real text input.

---

## 3. Algorithms and Data Structures

The project implements the following lossless compression algorithms:

### Huffman Coding

Huffman coding is an entropy-based compression algorithm that assigns shorter binary codes to frequently occurring characters and longer codes to less frequent characters.

**Data structures used:**
- Frequency table
- Priority queue (min-heap)
- Binary tree (Huffman tree)
- Mapping from characters to binary codes

### LZ77 (Lempel–Ziv 1977)

LZ77 is a dictionary-based compression algorithm that replaces repeated substrings with references to earlier occurrences within a sliding window.

**Data structures used:**
- Sliding window over the input text
- Tuples representing compression tokens (offset, length, next character)
- Lists or arrays for storing tokens

All algorithms are implemented **from scratch**, without using external compression libraries.

---

## 4. Program Inputs and Outputs

### Inputs
- A text file containing the data to be compressed
- Command-line arguments specifying:
  - Compression or decompression mode
  - Algorithm to use (Huffman or LZ77)
  - Input file path
  - Output file path

### Outputs
- A compressed binary file when running in compression mode
- A decompressed text file when running in decompression mode

The decompressed output must be identical to the original input text.

---

## 5. Expected Time and Space Complexity

The complexity estimates are based on standard theoretical analyses.

### Huffman Coding
- **Time complexity:**
  - Frequency table construction: \( O(n) \)
  - Huffman tree construction: \( O(k \log k) \), where \( k \) is the number of distinct characters
  - Encoding: \( O(n) \)

  Overall time complexity:  
  **\( O(n + k \log k) \)**

- **Space complexity:**
  - Huffman tree and code tables: \( O(k) \)
  - Encoded output proportional to input size

### LZ77
- **Time complexity:**
  - Worst-case complexity can approach \( O(n^2) \) for naive matching
  - With a fixed window size, practical performance is close to linear

- **Space complexity:**
  - Sliding window and token storage proportional to input size

These estimates guide implementation decisions such as window size and data structure choice.

---

## 6. Core of the Project

The core of this project is the **correct implementation of Huffman coding and LZ77 compression and decompression algorithms**.

This includes:
- Building the required data structures
- Encoding text into a compressed representation
- Decoding compressed data back to the original text without loss

Most development time is spent on implementing and validating these algorithms. Supporting components such as file handling, command-line interfaces, and testing exist to support and verify the core functionality.

---

## 7. Sources

The following sources are used to understand and implement the algorithms:

- Wikipedia articles on:
  - Huffman coding
  - LZ77 compression
- GeeksforGeeks (algorithm explanations and examples)
- Codecademy (background on compression concepts)
- ScienceDirect articles related to data compression
- *Introduction to Algorithms* (CLRS), Chapter 16
- MATLAB Central documentation and discussions
- *Handbook of Data Compression* by David Salomon

