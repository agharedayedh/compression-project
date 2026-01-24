# Lossless Text Compression Project

This project implements and evaluates lossless text compression algorithms with a focus on
algorithmic efficiency, correctness, and practical applicability. The goal is to compress
natural language text into a compact binary representation and restore it exactly to its
original form through decompression.

The project is developed as part of an algorithms-focused exercise project, emphasizing
the implementation, testing, and comparison of non-trivial algorithms beyond basic data
structures and standard library functionality.

---

## Implemented Algorithms

The project currently includes the following compression methods:

- **Huffman Coding**
  - Entropy-based prefix coding algorithm
  - Variable-length codes derived from character frequencies
  - Efficient for natural language text with skewed frequency distributions

- **LZ77 (Lempel–Ziv 1977)**
  - Dictionary-based compression algorithm
  - Replaces repeated substrings with backward references
  - Forms the basis of many practical compression formats

Both algorithms are implemented from scratch without relying on external compression libraries.

---

## Project Structure

compression-project/
├── src/
│ └── compression/
│ ├── init.py
│ └── main.py
├── tests/
│ ├── test_huffman.py
│ ├── test_lz77.py
│ └── test_end_to_end.py
├── data/
│ ├── sample_small.txt
│ └── sample_large.txt
├── docs/
│ ├── specification.md
│ ├── implementation.md
│ ├── testing.md
│ ├── user_guide.md
│ ├── weekly_report_1.md
│ └── weekly_report_2.md
├── README.md
├── pyproject.toml
└── .gitignore

---

## Requirements

- Python 3.11+
- Poetry 
- Git

All dependencies are managed through Poetry and specified in `pyproject.toml`.

---

## Installation

Clone the repository and install dependencies:

```bash
git clone git@github.com:agharedyedh/compression-project.git
cd compression-project
py -m poetry install
