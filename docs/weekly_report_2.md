# Weekly Report 2

## Time spent
Approximately 16–18 hours.

## What did I do this week?
During this week, I started the actual implementation of the core algorithm of the project. I focused exclusively on implementing **Huffman coding**, which is one of the two compression algorithms planned for the project.

I implemented the Huffman encoding and decoding logic from scratch, including frequency table construction, tree building, code generation, and bit-level encoding of the input text. The implementation is placed under the `compression` package and is structured so that encoding and decoding are clearly separated and testable.

In addition to the algorithm itself, I set up the initial testing infrastructure using `pytest`. I wrote unit tests that verify the correctness of the Huffman codec on small, deterministic inputs, as well as an end-to-end test that checks that a text can be compressed and then decompressed back to its original form without loss.

I also ensured that the project runs correctly inside the Poetry environment and that tests can be executed consistently through Poetry commands.

## How has the program progressed?
The project has moved from planning to actual implementation. The Huffman coding core is now functional and produces correct results for the tested cases. The program can already perform a complete compression–decompression roundtrip for text input using Huffman coding.


## What did I learn this week?
I deepened my understanding of how Huffman coding works in practice, especially how the theoretical description translates into concrete data structures such as trees and code tables. Implementing the algorithm myself clarified many details that are easy to overlook when only reading about it.

I also learned more about structuring a Python project for testing, including how to design code so that it is easy to unit test and how to use pytest together with Poetry. Writing tests in parallel with the implementation helped catch mistakes early.

## What remains unclear or has been challenging?
One challenging aspect has been deciding how much functionality is sufficient at this stage without over-implementing features too early. In particular, handling edge cases such as empty input and very small alphabets required careful thought.

Another open question is how to best represent compressed data in a fully binary format when the project is extended further, especially when comparing Huffman coding with LZ77 later on.

## What will I do next?
Next week, I will continue developing the project by extending testing, refining the Huffman implementation if needed, and starting the implementation of the second compression algorithm, LZ77. I will also begin documenting the implementation and testing strategy more thoroughly in the corresponding documentation files.

If time allows, I will also start thinking about how to fairly compare the two algorithms in terms of compression ratio and behavior on different types of input.
