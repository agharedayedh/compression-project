from __future__ import annotations

from pathlib import Path

from compression.storage import compress_file


def _load_natural_language_corpus() -> str:
    corpus_dir = Path("data") / "corpus"
    parts: list[str] = []

    for path in sorted(corpus_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            parts.append(text)

    if not parts:
        raise AssertionError("No usable files found in data/corpus/.")

    return "\n\n".join(parts)


def _safe_prefix_to_size(text: str, target_bytes: int) -> str:
    raw = text.encode("utf-8")
    if len(raw) <= target_bytes:
        return text
    return raw[:target_bytes].decode("utf-8", errors="ignore")


def _compressed_size(tmp_path: Path, text: str, algorithm: str) -> tuple[int, int]:
    in_path = tmp_path / f"{algorithm}_input.txt"
    out_path = tmp_path / f"{algorithm}_output.bin"

    in_path.write_text(text, encoding="utf-8")
    compress_file(in_path, out_path, algorithm=algorithm)

    return in_path.stat().st_size, out_path.stat().st_size


def test_huffman_compresses_real_natural_language_text(tmp_path: Path) -> None:
    corpus = _load_natural_language_corpus()
    text = _safe_prefix_to_size(corpus, 100 * 1024)

    original_size, compressed_size = _compressed_size(
        tmp_path, text, "huffman")
    ratio = compressed_size / original_size

    assert compressed_size < original_size
    assert ratio < 0.65, f"Unexpected Huffman ratio: {ratio:.3f}"


def test_lz78_compresses_1kb_natural_language_reasonably(tmp_path: Path) -> None:
    corpus = _load_natural_language_corpus()
    text = _safe_prefix_to_size(corpus, 1 * 1024)

    original_size, compressed_size = _compressed_size(tmp_path, text, "lz78")
    ratio = compressed_size / original_size

    assert compressed_size < original_size
    assert ratio < 0.80, f"Expected LZ78 to compress 1kB text, got ratio {ratio:.3f}"


def test_lz78_compresses_100kb_natural_language_well(tmp_path: Path) -> None:
    corpus = _load_natural_language_corpus()
    text = _safe_prefix_to_size(corpus, 100 * 1024)

    original_size, compressed_size = _compressed_size(tmp_path, text, "lz78")
    ratio = compressed_size / original_size

    assert compressed_size < original_size
    assert ratio < 0.60, f"Expected LZ78 ratio below 0.60 at 100kB, got {ratio:.3f}"
