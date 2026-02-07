# Implementation Document

## Program Structure

The project is implemented as a modular Python package located under the `src/compression`
directory. Each compression algorithm is placed in its own submodule to keep the code
organized and easy to extend.

The Huffman coding implementation contains functionality for frequency analysis, tree
construction, encoding, and decoding. The LZ78 implementation focuses on dictionary-based
compression, where repeated substrings are replaced with references to a dynamically
constructed dictionary.

The file `compression/main.py` serves as the main interface of the program. It connects the
compression algorithms and provides functions for compressing and decompressing text data
and files. This separation allows the algorithms to be tested independently while still
supporting end-to-end execution.

## Achieved Time and Space Complexities

### Huffman Coding

Huffman coding has a time complexity of \(O(n \log n)\), where \(n\) is the number of unique
symbols in the input. This complexity mainly comes from building the Huffman tree using a
priority queue. Encoding and decoding the text run in linear time relative to the input size.

The space complexity is \(O(n)\), as the algorithm needs to store the frequency table,
Huffman tree, and encoded bit representation.

### LZ78

LZ78 encoding and decoding both run in \(O(m)\) time, where \(m\) is the length of the input
string, assuming average constant-time dictionary operations. Each character is processed
once, and dictionary lookups are performed incrementally.

The space complexity is \(O(k)\), where \(k\) is the number of dictionary entries created
during compression. In the worst case, this grows linearly with the input size.

These complexity estimates are based on standard pseudocode descriptions and explanations
from textbooks and online references, rather than empirical measurement.

## Performance and Complexity Comparison

Huffman coding and LZ78 represent two fundamentally different approaches to compression.
Huffman coding is entropy-based and performs well when character frequencies are highly
skewed, while LZ78 is dictionary-based and performs better when the input contains repeated
substrings.

In terms of asymptotic complexity, both algorithms are efficient for practical input sizes.
However, their real-world performance depends strongly on input characteristics such as
repetition and alphabet size. A more detailed empirical comparison may be added later in
the project.

## Possible Shortcomings and Improvements

At the current stage, compressed data is stored in a simple structured format rather than
a fully optimized binary representation. This is sufficient for correctness and testing
but not optimal in terms of storage efficiency.

Other possible improvements include:
- Optimizing dictionary handling in LZ78
- Improving binary serialization of compressed data
- Adding performance benchmarks for larger input files
- Supporting algorithm selection via command-line arguments

These improvements are planned for later stages of the project.

## Use of Large Language Models

Large language models (ChatGPT) were used only to polish and improve the clarity of
documentation text. They were not used to generate algorithm implementations or core
logic. All algorithms and code structures were designed and implemented by the author.

## Sources

The following sources were used during the implementation:

- Cormen et al., *Introduction to Algorithms*
- Wikipedia: Huffman coding
- Wikipedia: LZ78
- *Handbook of Data Compression* by David Salomon
- Stack Overflow discussions related to Huffman tree storage
