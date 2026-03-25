# Lossless Text Compression Project

This project implements and evaluates **lossless text compression algorithms** with a focus on correctness, efficiency, and practical usability. The objective is to reduce the size of UTF-8 text files by encoding them into a compact binary representation while guaranteeing that the original input can be reconstructed exactly.

The project compares two different compression approaches:

- **Huffman coding**
- **LZ78**

Both algorithms are implemented from scratch without using external compression libraries.

---

## Implemented Algorithms

### Huffman Coding

Huffman coding is an entropy-based compression algorithm that assigns variable-length prefix codes to characters based on their frequencies in the input. Frequent symbols receive shorter codes.

### LZ78

LZ78 is a dictionary-based compression algorithm that builds a dictionary of previously seen phrases while processing the input. It outputs references to dictionary entries together with new characters.

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
poetry install
```

---

## Running the Program

Run the program with:

```bash
poetry run python -m compression.main
```

### Example Usage

```bash
poetry run python -m compression.main compress huffman input.txt output.bin
poetry run python -m compression.main compress lz78 input.txt output.bin
poetry run python -m compression.main decompress output.bin restored.txt
```

More detailed usage instructions are provided in:

```
docs/user_guide.md
```

---

## Testing

Automated tests are implemented using `pytest` and include:

- unit tests  
- integration tests  
- end-to-end tests  
- realistic input tests  

### Run all tests

```bash
poetry run pytest
```

### Run tests with coverage

```bash
poetry run pytest --cov
```

A detailed description of the testing strategy is available in:

```
docs/testing.md
```

---

## Performance Evaluation

The project also includes an empirical comparison of compression ratios using a corpus made from multiple different natural-language texts.

Run the comparison script with:

```bash
poetry run python -m compression.script.compare_compression
```

The results are discussed in:

```
docs/implementation.md
```

---

## Documentation

Project documentation is provided in the `docs/` directory:

- Specification  
- Implementation  
- Testing  
- User Guide  

### Weekly Reports

- Weekly Report 1  
- Weekly Report 2  
- Weekly Report 3  
- Weekly Report 4  
- Weekly Report 5  
- Weekly Report 6  

---

## Author

**Agharid Ayedh**  
Bachelor of Science – Data Science / Computer Science