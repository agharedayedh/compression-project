# Lossless Text Compression Project

This project implements and evaluates lossless text compression algorithms with a focus on
algorithmic correctness, efficiency, and practical usability. The objective is to reduce the
size of natural language text files by encoding them into a compact binary representation
while guaranteeing that the original input can be fully reconstructed through decompression.

The project emphasizes the implementation of non-trivial algorithms beyond basic data
structures and standard library functionality, as well as systematic testing and
documentation of the implemented solutions.

---

## Implemented Algorithms

The project currently includes the following compression methods:

### Huffman Coding
Huffman coding is an entropy-based compression algorithm that assigns variable-length
prefix codes to characters based on their frequencies in the input. Characters that occur
more frequently are represented with shorter codes, resulting in efficient compression
for text with skewed frequency distributions.

### LZ78 (Lempel–Ziv 1978)
LZ78 is a dictionary-based compression algorithm that builds a dictionary of previously seen
phrases while reading the input. It outputs references to dictionary entries together with new
symbols, allowing repeated patterns to be represented compactly.

The project allows comparing these two fundamentally different approaches to lossless
compression in terms of compression ratio, behavior, and algorithmic structure. Both algorithms are implemented from scratch without relying on external compression libraries.

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
git clone git@github.com:agharedyedh
compression-project.git
cd compression-project
py -m poetry install
```

---

## Running the Program

The main program can be executed using:

```bash
py -m poetry run python -m compression.main
```

The program supports compressing and decompressing text files using the implemented
algorithms. Detailed usage instructions, command-line options, and examples are provided
in the User Guide located in docs/user_guide.md.

---

## Testing

Automated tests are implemented using pytest and include both unit tests and end-to-end
tests.

Run all tests:

```bash
py -m poetry run pytest
```

Run tests with coverage reporting:

```bash
py -m poetry run pytest --cov
```


Testing focuses on:

- Correctness of compression and decompression
- Algorithm-specific functionality
- End-to-end validation using realistic text inputs

A detailed description of the testing strategy and coverage is available in
docs/testing.md.

---

## Documentation

Comprehensive project documentation is provided in the docs/ directory:

- Weekly Reports – documented development progress and reflections
- [Specification](docs/specification.md) – problem definition, algorithms, and expected complexity
- [Implementation](docs/implementation.md) – program structure and design decisions
- [Testing](docs/testing.md) – testing methodology and coverage analysis
- [User Guide](docs/user_guide.md) – instructions for running and using the program

---

## Weekly reports

Documented development progress and reflections:

- [Weekly Report 1](docs/weekly_report_1.md)
- [Weekly Report 2](docs/weekly_report_2.md)

## Author

Agharid Ayedh
Bachelor of Science – Data Science / Computer Science


