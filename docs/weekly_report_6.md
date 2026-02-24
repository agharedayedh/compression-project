Weekly Report 6

## Time spent  

Approximately 25 hours.


## What did I do this week?

This week I focused on finalizing the project and preparing it for submission.

The main tasks I completed:

- Finalized the binary storage format with a structured container including magic header, version, and algorithm identifier.
- Ensured bit-level packing for Huffman encoding works correctly with padding handling.
- Verified that compressed files remain valid and decompress correctly after the program exits.
- Cleaned and finalized the project structure to clearly separate algorithms, storage logic, and CLI.
- Updated all tests to import from the storage layer instead of the CLI.
- Expanded correctness tests for both Huffman and LZ78.
- Verified compression behavior across multiple input sizes (1 kB – 16 MB).
- Generated empirical compression ratio results for comparison between Huffman and LZ78.
- Finalized Implementation Document.
- Finalized Testing Document.
- Finalized User Guide.
- Ensured test coverage is satisfactory and all tests pass using plain pytest.


## How has the program progressed?

The project is now complete and ready for submission.

The program:
- Compresses and decompresses UTF-8 text files.
- Stores compressed data in a custom binary container format.
- Correctly reconstructs Huffman trees from stored frequency tables.
- Correctly reconstructs LZ78 dictionaries from stored tokens.
- Automatically detects the algorithm during decompression.
- Passes comprehensive unit and integration tests.
- Includes realistic input testing.
- Includes compression ratio verification.
- Includes empirical comparison between the algorithms.
- Contains clear documentation and structured code.


## What did I learn this week/today?

The most challenging aspects were:

- Designing a clean and deterministic binary storage format.
- Ensuring proper bit-packing without introducing decoding errors.
- Deciding how extensive empirical comparison should be.
- Balancing theoretical complexity analysis with practical testing.

While runtime benchmarking was considered, it was determined to be unnecessary.


## What remains unclear or has been challenging?

One challenging part was determining how extensive empirical testing should be. While I implemented compression ratio tests, I am still considering whether runtime benchmarking is necessary for this topic.

Another challenge was ensuring that the tests are representative enough to be considered convincing according to the grading criteria.


## What will I do next?

Next I will:

- Complete the second peer review.
- Make minor refinements if feedback suggests improvements.
- Perform a final review of documentation.

The core implementation, testing, and documentation are now complete.