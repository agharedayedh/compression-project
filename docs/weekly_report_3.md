# Weekly Report 3

## Time Spent
Approximately 10–12 hours.

## What did I do this week?
This week I focused on developing the core functionality of the project. I completed a working implementation of Huffman coding and began implementing the second compression algorithm, switching from LZ77 to LZ78 based on instructor feedback. The basic structure of the LZ78 encoder and decoder was implemented to support lossless compression and decompression. I also extended the main program so that the core functionality can be executed end-to-end.

In addition, I wrote unit tests for the main algorithmic components and expanded end-to-end tests to verify correct roundtrip behavior. Test coverage was measured and documented.

## How has the program progressed?
The project now has a runnable core that demonstrates its main idea: lossless text compression and decompression. Huffman coding is fully functional and tested, and LZ78 is implemented at a basic but correct level (i suppose). The main program can execute compression and decompression, making the project’s functionality observable. Automated testing and coverage tracking are in place.

## What did I learn this week?
I learned more about dictionary-based compression, particularly how LZ78 builds and uses a growing dictionary during encoding and decoding. I also gained experience designing tests for algorithmic correctness and interpreting coverage reports to identify untested parts of the code. Additionally, switching from LZ77 to LZ78 clarified how algorithm design choices affect implementation complexity.

## What remains unclear or has been challenging?
The most challenging part was designing a clean and correct LZ78 implementation while keeping it simple enough for this stage of the project. Another open question is how compressed data should eventually be represented efficiently in a fully binary format, especially when combining Huffman coding with dictionary-based methods.

## What will I do next?
Next week, I will complete and refine the LZ78 implementation, improve integration between the compression methods, and expand testing further. I will also continue writing the testing documentation and begin working on performance considerations and implementation details for the implementation document.
