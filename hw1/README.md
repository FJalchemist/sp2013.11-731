11-731 Machine Translation Spring 2013 

Yibin Lin

Feb. 12 2013

Algorithm description: 

The main idea I had doing this project is from the "Statistical Machine Translation" book, sections 4.1, 4.2 and especially 4.5. 

IBM model 1 is implemented first, then according to section 4.5, the reverse translation probability (from f to e) by IBM is also trained. Then we have two sets of alignments: alignmentA that is the alignment from e to f and alignmentB that is the alignment from f to e. 

Then the intersection of alignmentA and alignmentB is computed. We compare alignmentA and alignmentB with the computed intersection again, and add any element in A and B that has edit distance of less than 2 to the element of the intersection to the final result. The distance number 2 is determined by experiments.

The edit distance is defined as follows: for alignment (i-j) and (m-n):
edit distance = |i-m| + |j-n|.
I.e. the sum of absolute values of the difference of index in each language sentence.

---------------------------------------------------------------------- original README CONTENT
There are three Python programs here (`-h` for usage):

 - `./align` aligns words using Dice's coefficient.
 - `./check` checks for out-of-bounds alignment points.
 - `./grade` computes alignment error rate.

The commands are designed to work in a pipeline. For instance, this is a valid invocation:

    ./align -t 0.9 -n 1000 | ./check | ./grade -n 5


The `data/` directory contains a fragment of the German/English Europarl corpus.

 - `data/dev-test-train.de-en` is the German/English parallel data to be aligned. The first 150 sentences are for development; the next 150 is a blind set you will be evaluated on; and the remainder of the file is unannotated parallel data.

 - `data/dev.align` contains 150 manual alignments corresponding to the first 150 sentences of the parallel corpus. When you run `./check` these are used to compute the alignment error rate. You may use these in any way you choose. The notation `i-j` means the word at position *i* (0-indexed) in the German sentence is aligned to the word at position *j* in the English sentence; the notation `i?j` means they are "probably" aligned.

