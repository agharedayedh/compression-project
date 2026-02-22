from __future__ import annotations

import argparse
from pathlib import Path

from .storage import Algorithm, compress_file, decompress_file


def _build_parser() -> argparse.ArgumentParser:
    """Build the command-line interface (CLI) parser."""
    parser = argparse.ArgumentParser(
        prog="compression",
        description="Lossless text compression using Huffman coding and LZ78.",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_compress = sub.add_parser(
        "compress", help="Compress a UTF-8 text file into a binary file.")
    p_compress.add_argument(
        "algorithm",
        choices=["huffman", "lz78"],
        help="Compression algorithm to use.",
    )
    p_compress.add_argument(
        "input", type=Path, help="Path to input UTF-8 text file.")
    p_compress.add_argument("output", type=Path,
                            help="Path to output binary file (.bin).")

    p_decompress = sub.add_parser(
        "decompress", help="Decompress a binary file into a UTF-8 text file.")
    p_decompress.add_argument(
        "input", type=Path, help="Path to input binary file (.bin).")
    p_decompress.add_argument(
        "output", type=Path, help="Path to output UTF-8 text file.")

    return parser


def _ensure_parent_dir_exists(path: Path) -> None:
    """Create parent directory for output file if it does not exist."""
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)


def main(argv: list[str] | None = None) -> int:
    """
    Entry point for the CLI.

    Returns:
        Exit code (0 = success, non-zero = error).
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "compress":
            input_path: Path = args.input
            output_path: Path = args.output
            algorithm: Algorithm = args.algorithm

            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")

            _ensure_parent_dir_exists(output_path)

            compress_file(input_path, output_path, algorithm=algorithm)

            in_size = input_path.stat().st_size
            out_size = output_path.stat().st_size
            ratio = out_size / in_size if in_size else 0.0

            print(
                f"Compressed using {algorithm}: {input_path} -> {output_path}")
            print(
                f"Original: {in_size} bytes, Compressed: {out_size} bytes, Ratio: {ratio:.3f}")
            return 0

        if args.command == "decompress":
            input_path: Path = args.input
            output_path: Path = args.output

            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")

            _ensure_parent_dir_exists(output_path)

            decompress_file(input_path, output_path)

            out_size = output_path.stat().st_size
            print(
                f"Decompressed: {input_path} -> {output_path} ({out_size} bytes)")
            return 0

        parser.error("Unknown command")
        return 2

    except Exception as e:
        # Friendly CLI error message; stack traces are not helpful for end users.
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
