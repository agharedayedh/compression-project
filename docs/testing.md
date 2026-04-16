# Testing Document

---

## Overview

Testing ensures that the implemented compression algorithms are correct, reliable, and lossless.

The primary correctness requirement of this project is:

> After compressing and decompressing input, the restored output must match the original exactly.

---

## Testing Tools

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

- Total coverage: approximately **75–80%**  
- Core algorithm files (Huffman and LZ78 codecs): **~99–100%**  
- Storage layer: majority covered  
- CLI logic: partly covered  

Coverage was used as a **diagnostic tool**, not as a goal.  
The focus was on testing correctness-critical logic.

A coverage snapshot is saved as:

```
docs/coverage_week6.txt
```

---

## Final Results Summary

Compression performance was re-evaluated after implementing the final improvements to the LZ78 algorithm.


- All tests pass successfully (35 passed)  
- Huffman compression remains stable across all input sizes  
- LZ78 compression performance improved significantly compared to earlier versions  

Results now align with expected real-world behavior for natural-language compression

---

## Impact of Changes

The improvement is mainly due to:

- switching to byte-based encoding  
- using variable-length index representation  
- applying bit-level packing for token storage  

These changes reduce overhead and make the algorithm significantly more efficient.

---

## Output Snapshot

A coverage snapshot is saved as:

```
docs/coverage_final.txt
```

A comparison snapshot is saved as:

```
docs/comparison_output.txt
```

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

---

#### Edge Cases

- empty string  
- single repeated character (e.g. `"aaaaaa"`)  
- Unicode text  

---

#### Invalid Input Handling

The decoder is tested to ensure it raises errors for:

- bitstrings containing characters other than `"0"` and `"1"`  
- incomplete encoded bitstrings  
- invalid traversal paths in the Huffman tree  

This ensures strict validation of corrupted or malformed compressed data.

---

### 2. LZ78

**Test file:** `tests/test_lz78.py`

#### Implementation Details

The final LZ78 implementation operates on **raw bytes**, not Python strings.  
This avoids UTF-8 overhead and improves compression efficiency.

Each token has the form:

```
[index, byte]
```

Where:

- `index` is a reference to a previously seen phrase  
- `byte` is an integer in the range `0–255`  
- a special value `-1` is used only in the final token  

---

#### Roundtrip Correctness

Example:

```python
data = b"abracadabra"
tokens = encode(data)
restored = decode(tokens)
assert restored == data
```

---

#### Additional Cases

- repetitive input  
- structured text  
- UTF-8 encoded text  

---

#### Token Validation

The tests verify that:

- tokens are lists  
- each token has exactly two elements  
- both elements are integers  

---

#### Invalid Token Handling

The decoder is tested against invalid inputs:

- non-list tokens  
- wrong token length  
- non-integer index  
- non-integer byte  
- invalid dictionary references  
- incorrect placement of final token marker  

---

### 3. End-to-End Pipeline Testing

**Test file:** `tests/test_end_to_end.py`

These tests verify the full in-memory pipeline:

1. compress text using a selected algorithm  
2. decompress the result  
3. compare it with the original text  

This ensures:

- correct integration of algorithm and storage  
- correct algorithm detection during decompression  
- lossless behavior  

Invalid compressed data is also tested to ensure safe failure.

---

### 4. File-Based Integration Testing

**Test file:** `tests/test_file_pipeline.py`

These tests verify the file-based workflow:

1. write a UTF-8 text file  
2. compress it  
3. decompress it  
4. compare the restored output  

This ensures that the complete file-processing pipeline works correctly for both algorithms.

---

### 5. Realistic Natural-Language Testing

**Test file:** `tests/test_realistic_input.py`

A realistic text file is used:

```
tests/data/realistic_text.txt
```

#### Procedure

1. read the file  
2. compress using both algorithms  
3. decompress  
4. verify exact equality  

This provides an integration-style test with real-world input.

---

### 6. Compression Ratio Testing

**Test file:** `tests/test_compression_ratio.py`

These tests verify realistic compression performance.

---

#### Natural-Language Corpus

A corpus is constructed from multiple independent text files:

```
data/corpus/
```

This avoids artificial repetition and better represents real input.

---

#### Procedure

For each target size:

1. take a prefix of the corpus  
2. compress it  
3. measure compressed size  
4. compute compression ratio  

---

#### Expected Behavior

- Huffman should consistently reduce file size  
- LZ78 should:
  - perform poorly on very small inputs  
  - improve as input size increases  
  - achieve good compression for large inputs  

---

#### Purpose

These tests ensure that:

- compression is effective in practice  
- implementation choices (e.g. variable-length indexes) improve performance  
- results align with theoretical expectations  

---

## Representativeness of Inputs

The tests include:

- empty strings  
- small deterministic inputs  
- single-character repetition  
- repetitive patterns  
- Unicode text (emoji, Arabic, etc.)  
- realistic natural-language text  
- large structured inputs  

Two categories are clearly separated:

### 1. Artificial Inputs

Used for:

- correctness testing  
- edge cases  

### 2. Natural-Language Inputs

Used for:

- realistic performance evaluation  

Artificial repetition of natural-language text is avoided because it can produce misleading results, especially for dictionary-based compression.

---

## How Can the Tests Be Reproduced?

From the project root:

### Run all tests

```bash
poetry run pytest
```

### Run with coverage

```bash
poetry run pytest --cov --cov-report=term-missing
```

### Run a specific file

```bash
poetry run pytest tests/test_lz78.py
```

---

## Empirical Testing Results

Empirical comparison is performed using:

```
src/compression/script/compare_compression.py
```

Run with:

```bash
poetry run python -m compression.script.compare_compression
```

The script:

- reads a natural-language corpus  
- evaluates increasing input sizes  
- compares both algorithms  
- reports compression ratios  

---

## Summary of Testing Approach

The project includes:

- unit tests for algorithm correctness  
- strict invalid-input testing  
- integration tests  
- end-to-end tests  
- file-based tests  
- realistic input testing  
- empirical compression evaluation  
- coverage analysis  

---

## Testing Focus

- correctness  
- lossless behavior  
- robustness against invalid data  
- realistic performance  

The combination of unit testing and broader empirical evaluation provides strong confidence that the compression system is correctly implemented.