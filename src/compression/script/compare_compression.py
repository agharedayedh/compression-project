from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from compression.storage import compress_file

# Required input sizes for the empirical comparison (in bytes)
SIZES: list[tuple[str, int]] = [
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
    label: str
    original: int
    huffman: int
    lz78: int

    @property
    def h_ratio(self) -> float:
        return self.huffman / self.original if self.original else 0.0

    @property
    def l_ratio(self) -> float:
        return self.lz78 / self.original if self.original else 0.0


def _slug(label: str) -> str:
    """Make a safe filename suffix from labels like '256kB' or '4MB'."""
    return label.lower()


def build_text_to_size(base: str, target_bytes: int) -> str:
    """
    Build a UTF-8 text string that is approximately target_bytes in size
    by repeating base text.

    We slice bytes and decode with errors='ignore' to keep valid UTF-8.
    This means the final file may be slightly smaller than target_bytes,
    but with large targets it is effectively the requested size.
    """
    if not base.strip():
        raise ValueError("Base text must not be empty.")

    # Repeat until we are comfortably above the target in bytes.
    text = base
    while len(text.encode("utf-8")) < target_bytes + 1024:
        text += base

    encoded = text.encode("utf-8")
    sliced = encoded[:target_bytes]
    return sliced.decode("utf-8", errors="ignore")


def main() -> None:
    # You should provide a natural-language file here (public domain / your own text).
    base_path = Path("data") / "base_text.txt"
    if not base_path.exists():
        raise SystemExit(
            "Missing data/base_text.txt.\n"
            "Create it and paste natural-language text there (public domain or your own writing)."
        )

    base_text = base_path.read_text(encoding="utf-8")

    out_dir = Path("data") / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)

    results: list[Result] = []

    for label, target in SIZES:
        suffix = _slug(label)

        text = build_text_to_size(base_text, target)
        in_path = out_dir / f"input_{suffix}.txt"
        in_path.write_text(text, encoding="utf-8")

        h_path = out_dir / f"huffman_{suffix}.bin"
        l_path = out_dir / f"lz78_{suffix}.bin"

        compress_file(in_path, h_path, algorithm="huffman")
        compress_file(in_path, l_path, algorithm="lz78")

        results.append(
            Result(
                label=label,
                original=in_path.stat().st_size,
                huffman=h_path.stat().st_size,
                lz78=l_path.stat().st_size,
            )
        )

    # Print a clean table for pasting into docs.
    print("\nCompression ratio comparison (same natural-language input)\n")
    print(
        f"{'Input':<6} {'Original(B)':>12} {'Huffman(B)':>12} {'LZ78(B)':>10} "
        f"{'H ratio':>9} {'L ratio':>9}"
    )
    print("-" * 64)
    for r in results:
        print(
            f"{r.label:<6} {r.original:>12} {r.huffman:>12} {r.lz78:>10} "
            f"{r.h_ratio:>9.3f} {r.l_ratio:>9.3f}"
        )

    # Also print Markdown table rows to paste directly into implementation.md
    print("\nMarkdown rows (paste into docs/implementation.md):\n")
    for r in results:
        print(
            f"| {r.label} | {r.original} | {r.huffman} | {r.lz78} | "
            f"{r.h_ratio:.3f} | {r.l_ratio:.3f} |"
        )


if __name__ == "__main__":
    main()
