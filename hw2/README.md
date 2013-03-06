There are three Python programs here (`-h` for usage):

 - `./evaluate` evaluates pairs of MT output hypotheses relative to a reference translation using counts of matched words
 - `./check` checks that the output file is correctly formatted
 - `./grade` computes the accuracy

The commands are designed to work in a pipeline. For instance, this is a valid invocation:

    ./evaluate | ./check | ./grade


The `data/` directory contains a training set and a test set

 - `data/train.hyp1-hyp2-ref` is a file containing tuples of two translation hypotheses and a human (gold standard) translation.

 - `data/train.gold` contains gold standard human judgements indicating whether the first hypothesis (hyp1) or the second hypothesis (hyp2) is better or equally good/bad.

 - `data/test.hyp1-hyp2-ref` is a blind test set containing tuples of two translation hypotheses and a human (gold standard) translation. You will be graded on how well your predictions correlate with human judgements.

---------------------------------------------------------------------------- Hand in
Algorithm:

I implemented a simple METOER algorithm according to the wikipedia(http://en.wikipedia.org/wiki/METEOR), and used Porter stemmer in nltk to compare the word stems. I also computed chunks of continuous alignments to calculate the penalty. The implementation is straightforward and python's list comprehensions make the code very succinct. 

other ways to improve the algorithm will be to use WordNet to compare the lexical semantic information.

3/5
