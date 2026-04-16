# Specification Document  
**Lossless Text Compression Using Huffman Coding and LZ78**

---

- **Study program:** Bachelor of Science (BSc)
- **Documentation language:** English

# Problem Being Solved

This project solves the problem of lossless text compression. The goal is to reduce the storage size of UTF-8 text files while preserving all information exactly, so that the original text can be reconstructed without any loss during decompression.

Text compression is important because text files can contain redundancy, repeated patterns, and uneven symbol frequencies. Compression algorithms use these properties to represent the same information more compactly.

The project compares two different compression approaches:

- Huffman coding, which is based on symbol frequencies  
- LZ78, which is based on repeated phrases stored in a dictionary  

The purpose is not only to implement compression and decompression correctly, but also to compare how these algorithms behave on realistic natural-language input.

---

# Core of the Project

The core of the project is the implementation and evaluation of compression algorithms, especially the encoding and decoding logic of Huffman coding and LZ78.

The most important part is not the command-line interface or file handling, but the algorithmic logic itself:

- building Huffman frequency tables, trees, and prefix codes  
- building and using the LZ78 dictionary  
- designing a binary storage format for compressed output  
- reconstructing the original text exactly during decompression  
- comparing the compression effectiveness of the two algorithms  

Most of the project development time is spent on implementing, testing, and evaluating these algorithmic components.

---

# Algorithms and Data Structures

## 1. Huffman Coding

Huffman coding is a greedy compression algorithm that assigns shorter bit codes to more frequent symbols and longer bit codes to less frequent symbols.

### Main steps:

- count symbol frequencies  
- build a Huffman tree  
- generate prefix codes by traversing the tree  
- encode the input into a bitstream  
- decode by traversing the same tree structure  

### Data structures used:

- dictionary / hash map for frequency counting  
- priority queue (heap) for building the Huffman tree  
- binary tree for the code structure  
- dictionary for mapping symbols to codes  

---

## 2. LZ78

LZ78 is a dictionary-based compression algorithm. It scans the input and stores previously seen phrases in a dictionary. Each output token references an earlier phrase and extends it with one new byte.

### Main steps:

- scan the input from left to right  
- keep extending the current phrase while it is already in the dictionary  
- output a token when a new extension is found  
- add the new phrase to the dictionary  
- rebuild the dictionary in the same order during decompression  

In the final implementation, LZ78 operates on raw bytes rather than characters, and uses variable-length indexes to reduce storage overhead.

### Data structures used:

- dictionary / hash map for phrase-to-index mapping during encoding  
- dictionary / hash map for index-to-phrase mapping during decoding  
- list of tokens for the compressed representation  

---

## 3. Binary Storage Format

The project also includes a custom binary storage layer that stores compressed data in a file format containing:

- magic bytes  
- version number  
- algorithm identifier  
- algorithm-specific payload  

For Huffman coding, the payload stores:

- frequency table  
- encoded bit length  
- packed bitstream  

For LZ78, the payload stores:

- token count  
- bit-packed token stream using variable-length indexes  

This part is necessary because the project should not only compress in memory, but also save compressed data into files and decompress it later.

---

# Inputs and Their Use

The program receives the following inputs:

## 1. Text File for Compression

The input is a UTF-8 encoded text file. The file contents are read into memory and used as the data to compress.

### Use in the algorithms:

- Huffman uses the text to calculate character frequencies and build codes  
- LZ78 converts the text into UTF-8 bytes and compresses the byte sequence  

---

## 2. Compressed Binary File for Decompression

The program can also receive a compressed binary file previously produced by the program.

### Use during decompression:

- the storage layer reads the header to detect the algorithm  
- Huffman reconstructs the tree from the stored frequency data  
- LZ78 reconstructs the original bytes from the stored token stream  
- the bytes are converted back into UTF-8 text and written to file  

---

## 3. Corpus Files for Performance Evaluation

The project includes a natural-language corpus made from multiple independent text files.

### Use in evaluation:

- create realistic inputs of different sizes  
- compare compressed output sizes of Huffman and LZ78  
- measure compression ratio on representative text rather than artificial repetition  

---

# Expected Time and Space Complexities

The purpose of this section is to understand the algorithmic cost of the main parts of the project.

---

## Huffman Coding

Let:

- 𝑚 = length of the input  
- 𝑛 = number of distinct symbols  

### Time Complexity

Frequency counting:  
each input symbol is processed once  

```
𝑂(𝑚)
```

Building the priority queue and Huffman tree:  
there are 𝑛 distinct symbols, and combining nodes in the heap takes logarithmic time  

```
𝑂(𝑛 log 𝑛)
```

Encoding:  
once the code table is built, each input symbol is replaced by its code  

```
𝑂(𝑚)
```

Decoding:  
the encoded bitstream is processed one bit at a time, reconstructing the original data  

```
𝑂(𝑚)

```

in asymptotic discussion, decoding is linear in the size of the encoded data, which is proportional to the input size  

### Overall Time Complexity

```
𝑂(𝑚 + 𝑛 log 𝑛)
```

---

### Space Complexity

frequency table:

```
𝑂(𝑛)
```

Huffman tree:

```
𝑂(𝑛)
```

encoded representation:

```
𝑂(𝑚)
```

### Overall Space Complexity

```
𝑂(𝑚 + 𝑛)
```

### Why this complexity occurs:

- the full input must be examined to count frequencies  
- the heap operations determine the 𝑛 log 𝑛 term  
- the encoded result and decoded output are both proportional to input size  

---

## LZ78

Let:

- 𝑚 = number of input bytes    
- 𝑘 = number of dictionary entries created during compression  

### Time Complexity

Encoding:  
each byte is processed once, and dictionary lookup is average  

```
𝑂(1)
```

using a hash map  

```
𝑂(𝑚)
```

Decoding:  
each token is processed once and the dictionary is rebuilt in the same order  

```
𝑂(𝑚)
```

### Overall Time Complexity

```
𝑂(𝑚)
```

---

### Space Complexity

dictionary storage:

```
𝑂(𝑘)
```

output token list:  
proportional to number of phrases, which is at most linear in the input size  

```
𝑂(𝑚)
```

### Overall Space Complexity

```
𝑂(𝑘) ≤ 𝑂(𝑚)
```

### Why this complexity occurs:

- the algorithm scans the input from left to right once  
- each new phrase is inserted into the dictionary once  
- dictionary operations are efficient on average with hashing  

---

# Why These Algorithms Were Chosen

These two algorithms were selected because they represent two different and important ideas in compression:

- Huffman coding uses frequency-based prefix coding  
- LZ78 uses phrase reuse through a growing dictionary  

Comparing them makes the project more interesting algorithmically, because they behave differently depending on the structure of the input data. This also makes it possible to study how theoretical ideas appear in practical compression results.

---

# Expected Output

The project should produce:

- a compressed binary file when given a text input file  
- a restored text file when given a compressed binary input  
- compression statistics such as compressed size and compression ratio  
- empirical comparison output for different file sizes and algorithms  

The decompressed output must always match the original input exactly.

---

# Planned Testing Approach

The project will be tested through:

- unit tests for Huffman and LZ78  
- invalid-input tests  
- end-to-end tests for compress/decompress pipelines  
- file-based tests  
- tests using realistic natural-language input  
- empirical comparison of compression ratios on a corpus  

Testing focuses on both:

- correctness  
- practical compression behavior  

---

# Sources Intended to Be Used

The following sources are used to understand and implement the algorithms:

- Wikipedia articles on:
  - Huffman coding
  - LZ77 compression
- Python documentation  
- GeeksforGeeks (algorithm explanations and examples)
- Codecademy (background on compression concepts)
- ScienceDirect articles related to data compression
- *Introduction to Algorithms* (CLRS), Chapter 16
- MATLAB Central documentation and discussions
- *Handbook of Data Compression* by David Salomon
- Project Gutenberg texts for corpus material  
- Wikipedia articles for corpus material  

