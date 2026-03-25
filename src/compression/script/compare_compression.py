from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from compression.storage import compress_file


# Different input sizes used in the comparison
SIZES = [
    ("1kB", 1 * 1024),
    ("4kB", 4 * 1024),
    ("16kB", 16 * 1024),
    ("64kB", 64 * 1024),
    ("256kB", 256 * 1024),
    ("1MB", 1 * 1024 * 1024),
    ("4MB", 4 * 1024 * 1024),
    ("16MB", 16 * 1024 * 1024),
]


@dataclass(frozen=True)
class Result:
    """
    This class stores the result of one compression test.

    Attributes:
        label (str): Name of the input size, for example "1kB" or "1MB".
        original (int): Size of the original input file in bytes.
        huffman (int): Size of the Huffman compressed file in bytes.
        lz78 (int): Size of the LZ78 compressed file in bytes.
    """
    label: str
    original: int
    huffman: int
    lz78: int

    @property
    def h_ratio(self) -> float:
        """
        Calculates the compression ratio for Huffman coding.

        Returns:
            float: Compressed size divided by original size.
        """
        return self.huffman / self.original if self.original else 0.0

    @property
    def l_ratio(self) -> float:
        """
        Calculates the compression ratio for LZ78 coding.

        Returns:
            float: Compressed size divided by original size.
        """
        return self.lz78 / self.original if self.original else 0.0


def _read_corpus_text() -> str:
    """
    This function reads the text corpus used in the compression comparison.

    The program expects text files to be placed in:
        data/corpus/*.txt

    The corpus should contain several different natural-language text files.

    Returns:
        str: The combined text from all non-empty corpus files.

    Raises:
        SystemExit: If the corpus directory does not exist or if no usable
        text files are found.
    """
    corpus_dir = Path("data") / "corpus"
    if not corpus_dir.exists():
        raise SystemExit(
            "Missing corpus directory.\n"
            "Create: data/corpus/\n"
            "Add several different UTF-8 text files for realistic comparison."
        )

    parts: list[str] = []
    for path in sorted(corpus_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            parts.append(text)

    if not parts:
        raise SystemExit(
            "No usable corpus files found.\n"
            "Add several non-empty .txt files to data/corpus/."
        )

    return "\n\n".join(parts)


def _safe_prefix_to_size(text: str, target_bytes: int) -> str:
    """
    This function returns a prefix of the text that is about the wanted size
    in bytes, without breaking UTF-8 characters.

    This is useful because some characters may use more than one byte,
    so taking a normal string slice could give the wrong byte size.

    Args:
        text (str): The input text.
        target_bytes (int): Target size in bytes.

    Returns:
        str: A prefix of the text that fits safely into the target byte size.
    """
    if target_bytes <= 0:
        return ""

    raw = text.encode("utf-8")
    if len(raw) <= target_bytes:
        return text

    return raw[:target_bytes].decode("utf-8", errors="ignore")


def main() -> None:
    """
    This function runs the compression comparison.

    It reads the corpus text, creates input files of different sizes,
    compresses them with both Huffman and LZ78, and then prints the results.

    The printed results include:
    - original file size
    - compressed file size with Huffman
    - compressed file size with LZ78
    - compression ratios for both methods

    Returns:
        None
    """
    corpus = _read_corpus_text()
    corpus_bytes = len(corpus.encode("utf-8"))

    # Only test sizes that fit inside the available corpus
    available_sizes = [(label, size)
                       for label, size in SIZES if size <= corpus_bytes]
    if not available_sizes:
        raise SystemExit(
            f"Corpus is too small ({corpus_bytes} bytes) for the smallest target size."
        )

    if corpus_bytes < SIZES[-1][1]:
        print(
            f"Warning: corpus size is {corpus_bytes} bytes, so only sizes up to "
            f"{available_sizes[-1][0]} will be tested."
        )

    out_dir = Path("data") / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)

    results: list[Result] = []

    for label, target in available_sizes:
        text = _safe_prefix_to_size(corpus, target)

        # Save the generated input text into a file
        in_path = out_dir / f"input_{label}.txt"
        in_path.write_text(text, encoding="utf-8")

        # Output files for the two compression algorithms
        h_path = out_dir / f"huffman_{label}.bin"
        l_path = out_dir / f"lz78_{label}.bin"

        # Compress the same input using both methods
        compress_file(in_path, h_path, algorithm="huffman")
        compress_file(in_path, l_path, algorithm="lz78")

        # Store the file sizes for later printing
        results.append(
            Result(
                label=label,
                original=in_path.stat().st_size,
                huffman=h_path.stat().st_size,
                lz78=l_path.stat().st_size,
            )
        )

    print("Compression ratio comparison (representative natural-language corpus)\n")
    print(
        f"{'Input':<6} {'Original(B)':>12} {'Huffman(B)':>12} "
        f"{'LZ78(B)':>12} {'H ratio':>9} {'L ratio':>9}"
    )
    print("-" * 68)

    for result in results:
        print(
            f"{result.label:<6} {result.original:>12} {result.huffman:>12} "
            f"{result.lz78:>12} {result.h_ratio:>9.3f} {result.l_ratio:>9.3f}"
        )


if __name__ == "__main__":
    main()
