I implemented PRO according to the original paper, also use the MEGAm linear model package mentioned in the paper . 

I use four features. The first three features are the default ones. The other is sentence token count.

The PRO sampling is done by sampling according to the difference of the bleuplus1 (smoothed bleu) score. To be specific:

(1). For each pair in one hundred candidate translations, calculate their difference in smoothed BLEU score relateive to the reference translation.

(2). calculate the distribution according to (1) for each pair. This is the sampling probability of each pair.

(3). sample from probability (2), and return both positive and negative training example if the sample is above a threshold of bleu diff > 0.05
