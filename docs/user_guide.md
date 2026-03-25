# User Guide

---

## Overview

This program provides **lossless text compression** using two algorithms:

- **Huffman coding**
- **LZ78**

The program can:

- Compress a UTF-8 text file into a binary file  
- Decompress a binary file back into the original text  

The compression is **lossless**, meaning the original file is recovered exactly after decompression.

---

## Requirements

- Python 3.11+  
- Poetry  

### Install dependencies

```bash
poetry install
```

---

## Running the Program

The program is executed using the command-line interface:

```bash
poetry run python -m compression.main
```

---

## Commands

### 1. Compress a File

```bash
poetry run python -m compression.main compress <algorithm> <input> <output>
```

#### Arguments

- `<algorithm>`: `huffman` or `lz78`  
- `<input>`: path to a UTF-8 text file  
- `<output>`: path to output compressed `.bin` file  

#### Example

```bash
poetry run python -m compression.main compress huffman input.txt output.bin
poetry run python -m compression.main compress lz78 input.txt output.bin
```

---

### 2. Decompress a File

```bash
poetry run python -m compression.main decompress <input> <output>
```

#### Arguments

- `<input>`: compressed `.bin` file  
- `<output>`: restored UTF-8 text file  

#### Example

```bash
poetry run python -m compression.main decompress output.bin restored.txt
```

---

## Input Requirements

- Input files must be valid UTF-8 text files  
- The program reads the entire file into memory (not streaming)  

---

## Output Format

Compressed files are stored in a **custom binary format** that includes:

- A header (magic bytes, version, algorithm)  
- Encoded data (Huffman or LZ78)  

These files are **not human-readable**.

---

## Example Workflow

### Step 1: Create input file

```
Hello world! Hello world!
```

### Step 2: Compress

```bash
poetry run python -m compression.main compress huffman input.txt compressed.bin
```

Example output:

```
Compressed using huffman: input.txt -> compressed.bin
Original: 28 bytes, Compressed: XX bytes, Ratio: X.XXX
```

---

### Step 3: Decompress

```bash
poetry run python -m compression.main decompress compressed.bin restored.txt
```

---

### Step 4: Verify

The file `restored.txt` will be identical to `input.txt`.

---

## Error Handling

The program provides user-friendly error messages.

### Examples

- Input file does not exist:  
  ```
  Error: Input file not found
  ```

- Invalid compressed file:  
  ```
  Error: Invalid data: wrong magic header
  ```

- Corrupted data:  
  ```
  Error: Invalid compressed data
  ```

---

## Running Tests

### Run all tests

```bash
poetry run pytest
```

### Run with coverage

```bash
poetry run pytest --cov
```

---

## Compression Comparison 

You can compare algorithm performance using:

```bash
poetry run python -m compression.script.compare_compression
```

This script:

- Uses a natural-language text corpus from `data/corpus/`  
- Generates different input sizes  
- Compares compression ratios of both algorithms  

---

## Notes

- Compression efficiency depends on input characteristics  
- Huffman works well with skewed character frequencies  
- LZ78 works well when repeated substrings exist  
- Results vary depending on the input text  

---

## Summary

This program allows you to:

- Compress text files using Huffman or LZ78  
- Decompress files back to original form  
- Compare compression behavior on realistic input  

The system is designed for:

- correctness  
- clarity  
- demonstration of algorithm behavior  