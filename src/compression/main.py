from __future__ import annotations

import argparse
from pathlib import Path

from .storage import Algorithm, compress_file, decompress_file


def _build_parser() -> argparse.ArgumentParser:
    """
    This function creates the command-line argument parser for the program.

    The parser supports two commands:
    - compress: compress a text file into a binary file
    - decompress: decompress a binary file back into a text file

    Returns:
        argparse.ArgumentParser: The ready parser for the command-line interface.
    """
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
    """
    This function makes sure that the parent directory of the output file exists.

    If the directory does not exist yet, it is created automatically.

    Args:
        path (Path): Path to the output file.

    Returns:
        None
    """
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)


def main(argv: list[str] | None = None) -> int:
    """
    This is the main function of the command-line interface.

    It reads the command-line arguments and then either compresses
    or decompresses a file based on the selected command.

    Args:
        argv (list[str] | None): Optional list of command-line arguments.
        If None, the program uses the normal command-line input.

    Returns:
        int: Exit code of the program.
        - 0 means success
        - 1 means an error happened
        - 2 means invalid command usage
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

            # Compress the input file using the selected algorithm
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

            # Decompress the binary file back into text
            decompress_file(input_path, output_path)

            out_size = output_path.stat().st_size
            print(
                f"Decompressed: {input_path} -> {output_path} ({out_size} bytes)")
            return 0

        parser.error("Unknown command")
        return 2

    except Exception as e:
        # Print a simple error message for the user
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
