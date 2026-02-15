# User Guide  
**Lossless Text Compression Project**

---

## 1. Overview

This program implements two classical lossless text compression algorithms:

- **Huffman Coding**
- **LZ78**

The program allows users to:

- Compress a UTF-8 encoded text file
- Decompress a previously compressed file
- Choose which compression algorithm to use

The decompressed output is guaranteed to match the original input exactly.

---

## 2. Requirements

- Python 3.11+
- Poetry
- Git (optional, for cloning repository)

Install dependencies:

```bash
poetry install
```

---

## 3. Running the Program
The program is executed from the command line using Poetry.

General format:

```bash
poetry run python -m compression.main <command> <algorithm> <input_path> <output_path>
```

---

## 4. Compressing a File
