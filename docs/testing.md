# Testing Document

## Week 2 Testing Status

Testing has been started alongside the development of the project’s core functionality.  
At this stage, the focus is on verifying the correctness of the Huffman coding implementation using unit tests and a simple end-to-end roundtrip test.

The testing effort will be expanded in later weeks as more functionality (such as LZ77 compression and file-based processing) is implemented.

---

### Huffman Coding – Unit Tests
- **Frequency-based encoding correctness**  
  Small deterministic input strings (e.g. `"aaabcc"`) are encoded using Huffman coding.
- **Roundtrip correctness**  
  The encoded output is decoded and verified to match the original input exactly.
- **Tree construction behavior**  
  Tests ensure that valid Huffman trees can be built from character frequency tables without runtime errors.

These tests are implemented as unit tests using `pytest` and are located in:

- `tests/test_huffman.py`

---

### End-to-End Pipeline Test
- A simple pipeline test verifies that a short input string can be:
  1. Compressed using the Huffman encoder
  2. Decompressed back to text
  3. Compared against the original input

This ensures that the core compression–decompression workflow functions correctly at a basic level.

The end-to-end test is located in:

- `tests/test_end_to_end.py`

---

## Test Inputs Used

The current tests use:
- Short, deterministic strings (e.g. `"aaabcc"`, `"This is a test."`)
- Inputs chosen to be small and predictable, making it easier to verify correctness manually

Larger files and randomized inputs will be introduced in later testing phases.

---

## How to Run the Tests

All tests can be executed in bash using:

```bash
py -m poetry run pytest
```

## Test Coverage

Test coverage is tracked using pytest-cov. To run tests with coverage reporting:

```bash
py -m poetry run pytest --cov --cov-report=term-missing
```

A saved coverage report for Week 2 is available at:

- `docs/coverage_week2.txt`


## Testing Status (Week 3)

Automated unit testing is used to verify the correctness of the core compression algorithms.
Testing focuses on lossless behavior, meaning that decompression must exactly reproduce the
original input.

### What is tested?

- Huffman coding:
  - Encoding and decoding correctness
  - End-to-end roundtrip tests
- LZ78:
  - Encoding and decoding using dictionary-based compression
  - Roundtrip tests with simple and representative text inputs

### Types of inputs used

- Empty strings
- Short deterministic strings
- Repeated-pattern text
- Natural language sentences

### How to run tests

```bash
py -m poetry run pytest
```

### Coverage tracking

Test coverage is measured using pytest-cov:

- `py -m poetry run pytest --cov --cov-report=term-missing`

A snapshot of the Week 3 coverage report is saved in:

- `docs/coverage_week3.txt`

Coverage is used to identify untested parts of the core logic rather than to maximize percentage.

