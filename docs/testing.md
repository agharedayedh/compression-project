# Testing Document

## Overview

Testing ensures that the implemented compression algorithms are correct, reliable, and truly lossless.

The primary correctness requirement of this project is:

> After compressing and decompressing a file, the output must match the original input exactly, byte-for-byte.

Testing was implemented using:

- `pytest` for automated unit and integration tests  
- `pytest-cov` for coverage measurement  

The testing strategy combines:

- Unit testing  
- Integration testing  
- End-to-end testing  
- Empirical compression ratio testing  

---

# Unit Testing Coverage Report

Coverage was measured using:

```bash
poetry run pytest --cov --cov-report=term-missing
```

### Week 6 Coverage Summary

- **Total coverage:** approximately 75–80%  
- **Core algorithm files (Huffman and LZ78 codecs):** ~99–100%  
- **Storage layer:** majority covered  
- **CLI logic:** partially covered  

Coverage is used as a diagnostic tool rather than a goal.  
All correctness-critical logic is covered by tests.

A coverage snapshot is saved as:

```
docs/coverage_week6.txt
```

---

# What Was Tested and How?

---

## 1. Huffman Coding

**Test file:** `tests/test_huffman.py`

### Roundtrip Correctness

Example:

```python
text = "aaabcc"
freq, bits = encode(text)
out = decode(freq, bits)
assert out == text
```

Verifies:

- Frequency table creation  
- Huffman tree construction  
- Correct encoding  
- Correct decoding  

### Edge Cases

- Empty string  
- Single-character repetition (e.g. `"aaaaaa"`)  

### Invalid Bit Input

Tests verify that invalid bitstrings (characters other than `"0"` or `"1"`) raise a `ValueError`.

---

## 2. LZ78

**Test file:** `tests/test_lz78.py`

### Roundtrip Correctness

Example:

```python
text = "abracadabra"
tokens = encode(text)
restored = decode(tokens)
assert restored == text
```

### Repetitive Input

Large repetitive patterns were tested to ensure dictionary growth works correctly.

### Unicode Support

Example:

```python
text = "Agharid 😊😊 hello مرحبا"
```

Ensures UTF-8 characters are handled correctly.

### Token Structure Validation

Tests verify:

- Tokens are lists  
- Each token has length 2  
- First element is integer  
- Second element is string  

### Invalid Token Handling

Tests verify decoding raises `ValueError` for:

- Non-list tokens  
- Wrong token length  
- Non-integer index  
- Non-string character  
- Invalid dictionary reference  

---

## 3. End-to-End Pipeline Testing

**Test file:** `tests/test_end_to_end.py`

This verifies the full pipeline:

1. Compress text using selected algorithm  
2. Decompress resulting binary  
3. Compare to original text  

Example:

```python
data = compress_text(text, algorithm="huffman")
out = decompress_bytes(data)
assert out == text
```

This ensures:

- Storage layer correctness  
- Algorithm detection during decompression  
- Full system integration  

---

## 4. File-Based Integration Testing

**Test file:** `tests/test_file_pipeline.py`

Tests actual file system behavior:

1. Write UTF-8 file  
2. Compress to `.bin`  
3. Decompress to new file  
4. Compare file contents  

Example:

- Both algorithms were used to compress a realistic multi-paragraph text file.  
- The restored file was verified to match exactly.  

---

## 5. Realistic Natural-Language Testing

**Test file:** `tests/test_realistic_input.py`

A real natural-language text file located in:

```
tests/data/realistic_text.txt
```

Procedure:

1. Read realistic text  
2. Compress using both algorithms  
3. Decompress  
4. Verify exact match  

This ensures representative real-world input coverage.

---

## 6. Compression Ratio Testing (Empirical Testing)

**Test file:** `tests/test_compression_ratio.py`

These tests verify expected compression behavior.

### Highly Repetitive Input

Example:

```python
text = "a" * 200_000
```

Ensures compressed size is smaller than original.

### Large Natural-Language Input

Multi-paragraph realistic text repeated thousands of times.

Verifies that Huffman compression reduces file size for sufficiently large natural-language input.

---

# Types of Inputs Used for Testing

To ensure representativeness, the following inputs were used:

- Empty strings  
- Single-character repetition  
- Small deterministic strings  
- Repetitive patterns (e.g. `"abcabcabc"`)  
- Unicode text (emojis and Arabic characters)  
- Multi-paragraph natural-language text  
- Large realistic input files (MB-scale)  
- Highly repetitive long strings  

This ensures:

- Branch coverage  
- Edge-case coverage  
- Realistic workload testing  

---

# How Can the Tests Be Reproduced?

From the project root:

### Run all tests

```bash
poetry run pytest
```

### Run tests with coverage

```bash
poetry run pytest --cov --cov-report=term-missing
```

### Run a specific test file

```bash
poetry run pytest tests/test_huffman.py
```

All results described in this document can be reproduced using these commands.

---

# Empirical Testing Results

In addition to automated unit tests, empirical comparison was performed using the script:

```
compression/script/compare_compression.py
```

Run with:

```bash
poetry run python -m compression.script.compare_compression
```

The script:

- Generates natural-language inputs from 1kB to 16MB  
- Compresses using both algorithms  
- Measures compressed file size  
- Reports compression ratios  

### Results Show

- Huffman stabilizes around ~0.54 compression ratio  
- LZ78 performs poorly for very small files  
- LZ78 improves significantly for larger inputs  

Runtime benchmarking was not performed, as it was not required by course feedback.

---

# Summary of Testing Approach

The project includes:

- Unit tests for algorithm correctness  
- Error-condition testing  
- Integration tests  
- End-to-end pipeline tests  
- File-based tests  
- Realistic input tests  
- Empirical compression ratio analysis  
- Coverage measurement  

Testing focuses on:

- Correctness  
- Lossless behavior  
- Representative inputs  
- Practical validation  

The combination of unit testing and empirical evaluation ensures the reliability of the implemented compression system.