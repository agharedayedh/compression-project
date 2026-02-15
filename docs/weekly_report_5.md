# Weekly Report 5

## Time spent  

Approximately 20 hours.


## What did I do this week?

This week I focused on improving the project based on peer review feedback and aligning it more closely with the official course requirements.

The main tasks I completed:

- Fixed issues in `pyproject.toml`, including adding the missing authors field.
- Refactored the compression system so that compressed data is stored in a proper binary format instead of JSON.
- Ensured that compressed files remain usable even after the program exits.
- Cleaned up the project structure and removed unused or empty files.
- Improved the LZ78 implementation by refining type annotations and validation.
- Added integration-level file tests for compression and decompression.
- Added realistic input tests using large natural-language text.
- Implemented compression ratio tests to verify that compression reduces file size for representative inputs.
- Reviewed branch coverage setup and ensured core algorithm logic is tested.
- Updated documentation (Testing Document and User Guide).


## How has the program progressed?

The core functionality of the project is now complete and stable.

The program now:

- Compresses and decompresses files using Huffman coding and LZ78.
- Stores compressed data in a binary format.
- Automatically detects the correct algorithm during decompression.
- Passes comprehensive unit tests.
- Includes integration and realistic input tests.
- Verifies that compression reduces file size for appropriate inputs.
- Has structured and updated documentation.

At this stage, the project satisfies the requirement that compressed data must remain compressed outside runtime.


## What did I learn this week/today?

This week I learned that testing a compression algorithm is not only about verifying roundtrip correctness. It is also important to test whether compression behaves as expected in realistic situations, such as reducing file size for repetitive or natural-language text.

I also learned more about:

- Binary file handling in Python.
- Designing representative test inputs.
- Structuring integration tests.
- Aligning implementation with formal course grading requirements.

I improved my understanding of how to justify testing decisions instead of just writing many tests.


## What remains unclear or has been challenging?

One challenging part was determining how extensive empirical testing should be. While I implemented compression ratio tests, I am still considering whether runtime benchmarking is necessary for this topic.

Another challenge was ensuring that the tests are representative enough to be considered convincing according to the grading criteria.


## What will I do next?

Next week I plan to:

- Review branch coverage to ensure no important logic is untested.
- Refine and polish the Implementation and Testing documents.
- Double-check that documentation clearly reflects the final implementation.
- Prepare for the second peer review.
- Finalize the project for submission.
