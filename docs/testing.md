# Testing Document

## Overview

Testing is an essential part of this project to ensure the correctness and reliability of
lossless compression and decompression. The main testing goal is to verify that all
implemented algorithms are **lossless**, meaning that decompression always reproduces
the original input exactly.

Automated unit tests and end-to-end tests are implemented using `pytest`. Test coverage
is measured with `pytest-cov` and used to identify untested parts of the core logic.


## What Was Tested and How?

### Huffman Coding

Huffman coding was tested using unit tests that verify both individual components and
the full compression–decompression pipeline.

The following aspects were tested:

- **Frequency-based encoding correctness**  
  Small deterministic strings (e.g. `"aaabcc"`) are encoded and checked to ensure that
  symbol frequencies are processed correctly.

- **Tree construction**  
  Tests verify that a valid Huffman tree can be built from frequency tables without
  runtime errors.

- **Encoding and decoding correctness**  
  Encoded bit sequences are decoded and compared against the original input.

- **End-to-end roundtrip testing**  
  Text is compressed and then decompressed, and the result is verified to match the
  original input exactly.

Relevant test files:
- `tests/test_huffman.py`
- `tests/test_end_to_end.py`


### LZ78

LZ78 testing focuses on dictionary-based compression behavior and correctness.

The following aspects were tested:

- **Encoding and decoding correctness**  
  Input strings are encoded into (index, character) pairs and decoded back to text.

- **Dictionary growth behavior**  
  Tests verify that the dictionary is built incrementally and used consistently during
  encoding and decoding.

- **Roundtrip correctness**  
  Compression followed by decompression always reproduces the original input.

Relevant test file:
- `tests/test_lz78.py`


## Types of Inputs Used for Testing

The following types of inputs were used to ensure representative coverage:

- Empty strings
- Very short deterministic strings
- Repeated-pattern text (e.g. `"abababab"`)
- Natural language sentences
- Inputs with varying repetition and symbol distributions

These inputs were chosen to make correctness easy to verify while still exercising the
core algorithmic behavior.


## End-to-End Testing

End-to-end tests verify that the full compression pipeline works correctly from input
text to compressed data and back.

Example test procedure:
1. Compress a text string using the selected algorithm
2. Decompress the produced output
3. Verify that the decompressed text matches the original input exactly

This ensures that the main functionality of the program is observable and correct.


## How Can the Tests Be Reproduced?

All tests can be executed using Poetry and pytest.

Run all tests:
```bash
py -m poetry run pytest
```

Run tests with coverage reporting:

```bash
py -m poetry run pytest --cov --cov-report=term-missing
```

These commands reproduce all test results described in this document.

## Unit Test Coverage Report

Test coverage is tracked using pytest-cov. Coverage reports are generated to identify
unexecuted code paths and guide further testing.

Saved coverage snapshots:

Week 2: `docs/coverage_week2.txt`

Week 3: `docs/coverage_week3.txt`

Week 4: `docs/coverage_week4.txt`

Coverage is used as a diagnostic tool, not as a goal in itself. The emphasis is on
testing correctness-critical parts of the algorithms rather than achieving 100% coverage.

## Empirical Testing Results

At the current stage, empirical performance testing (such as compression ratio or runtime
benchmarks on large files) is limited. The focus has been on algorithmic correctness and
lossless behavior.

Future work may include:

- Compressing and decompressing larger text files
- Comparing compression ratios between Huffman coding and LZ78
- Visualizing performance results graphically
- Testing Summary (Week 4 Status)

By Week 4:

Core compression functionality is fully testable

Both Huffman coding and LZ78 are covered by unit and roundtrip tests

End-to-end testing is in place

Test coverage reporting is included and documented
