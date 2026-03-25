# Testing Document

## Overview

Testing ensures that the implemented compression algorithms are correct, reliable, and lossless.

The primary correctness requirement of this project is:

> After compressing and decompressing input, the restored output must match the original exactly.

Testing was implemented using:

- `pytest` for automated tests
- `pytest-cov` for coverage measurement

The testing strategy combines:

- unit testing
- integration testing
- end-to-end testing
- empirical compression-ratio evaluation

---

## Unit Testing Coverage Report

Coverage was measured using:

```bash
poetry run pytest --cov --cov-report=term-missing
```

### Week 6 Coverage Summary

- Total coverage: approximately 75–80%  
- Core algorithm files (Huffman and LZ78 codecs): about 99–100%  
- Storage layer: majority covered  
- CLI logic: only partly covered  

Coverage was used as a diagnostic tool, not as the only goal. The main focus was testing correctness-critical logic.

A coverage snapshot is saved as:

```
docs/coverage_week6.txt
```

---

## What Was Tested and How?

---

### 1. Huffman Coding

**Test file:** `tests/test_huffman.py`

#### Roundtrip Correctness

Example:

```python
text = "aaabcc"
freq, bits = encode(text)
out = decode(freq, bits)
assert out == text
```

This verifies:

- correct frequency counting  
- valid Huffman tree construction  
- correct encoding  
- correct decoding  

#### Edge Cases

The following special cases were tested:

- empty string  
- single repeated character (e.g. `"aaaaaa"`)  
- Unicode text  

#### Invalid Input Handling

The tests verify that the decoder raises `ValueError` for:

- bitstrings containing characters other than `"0"` and `"1"`  
- incomplete encoded bitstrings  

---

### 2. LZ78

**Test file:** `tests/test_lz78.py`

#### Roundtrip Correctness

Example:

```python
text = "abracadabra"
tokens = encode(text)
restored = decode(tokens)
assert restored == text
```

#### Additional Cases

The tests include:

- repetitive input  
- spaces and punctuation  
- Unicode input  

#### Token Validation

The tests verify that produced tokens have the expected structure:

- token is a list  
- length is 2  
- first value is an integer  
- second value is a string  

#### Invalid Token Handling

The decoder is tested against invalid inputs, such as:

- non-list tokens  
- wrong token length  
- non-integer index  
- non-string character  
- invalid dictionary reference  

---

### 3. End-to-End Pipeline Testing

**Test file:** `tests/test_end_to_end.py`

These tests verify the full in-memory pipeline:

1. compress text using a selected algorithm  
2. decompress the result  
3. compare it with the original text  

This ensures that:

- compression and decompression work together correctly  
- the storage layer is correct  
- algorithm detection during decompression works  

The tests also include empty input and invalid compressed data.

---

### 4. File-Based Integration Testing

**Test file:** `tests/test_file_pipeline.py`

These tests verify the file-based pipeline:

1. write a UTF-8 text file  
2. compress it to a binary file  
3. decompress it to a new text file  
4. compare the restored text with the original  

This validates that the complete file-processing workflow behaves correctly for both algorithms.

---

### 5. Realistic Natural-Language Testing

**Test file:** `tests/test_realistic_input.py`

A realistic text file is stored in:

```
tests/data/realistic_text.txt
```

#### Procedure

1. read the text file  
2. compress it using both algorithms  
3. decompress the result  
4. verify exact equality with the original  

This gives an integration-style test using realistic natural-language input rather than only short artificial strings.

---

### 6. Compression Ratio Testing

**Test file:** `tests/test_compression_ratio.py`

These tests verify expected compression behavior.

#### Highly Repetitive Input

Example:

```python
text = "a" * 200_000
```

This input is intentionally highly repetitive. It is used to verify that both algorithms reduce size where compression should clearly help.

#### Large Structured Text Input

Another test uses a larger structured text input to verify that Huffman compression reduces file size on non-trivial text.

This test is useful for checking compression behavior, but it is not treated as the main source of realistic performance evaluation.

---

## Representativeness of Inputs

Particular care was taken to use inputs that reveal different aspects of correctness.

The tests include:

- empty strings  
- small deterministic strings  
- single-character repetition  
- repetitive patterns (e.g. `"abcabcabc"`)  
- Unicode text (including emoji and Arabic characters)  
- realistic natural-language text files  
- longer structured text inputs  
- highly repetitive long strings  

Realistic natural-language inputs were used to represent practical use cases.

Highly repetitive inputs were also tested separately because they help understand algorithm behavior in ideal compression conditions.

These two categories were kept conceptually separate. Artificial repetition of the same natural-language text was avoided in performance evaluation because it can create unrealistic results, especially for dictionary-based compression algorithms such as LZ78.

---

## How Can the Tests Be Reproduced?

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

All results described in this document can be reproduced with these commands.

---

## Empirical Testing Results

In addition to automated tests, empirical comparison was performed using:

```
src/compression/script/compare_compression.py
```

Run with:

```bash
poetry run python -m compression.script.compare_compression
```

The script:

- reads a corpus consisting of multiple different natural-language text files  
- takes prefixes of increasing size  
- compresses them using both algorithms  
- measures compressed size  
- reports compression ratios  

This comparison is intended to study how the algorithms behave on representative natural-language input.

---

## Summary of Testing Approach

The project includes:

- unit tests for algorithm correctness  
- invalid-input tests  
- integration tests  
- end-to-end tests  
- file-based tests  
- realistic input tests  
- empirical compression-ratio evaluation  
- coverage measurement  

### Testing Focus

- correctness  
- lossless behavior  
- representative inputs  
- practical validation  

The combination of unit testing and broader empirical evaluation provides strong confidence that the compression system is correctly implemented.