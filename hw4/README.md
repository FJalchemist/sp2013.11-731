I implemented PRO according to the original paper, also use the MEGAm linear model package mentioned in the paper . 

I use four features. The first three features are the default ones. The other is sentence token count.

The PRO sampling is done by sampling according to the difference of the bleuplus1 (smoothed bleu) score. 
