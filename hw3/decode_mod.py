#!/usr/bin/env python
import argparse
import sys
import models
import heapq
from collections import namedtuple

parser = argparse.ArgumentParser(description='Simple phrase based decoder.')
parser.add_argument('-i', '--input', dest='input', default='data/input', help='File containing sentences to translate (default=data/input)')
parser.add_argument('-t', '--translation-model', dest='tm', default='data/tm', help='File containing translation model (default=data/tm)')
parser.add_argument('-s', '--stack-size', dest='s', default=1, type=int, help='Maximum stack size (default=1)')
parser.add_argument('-n', '--num_sentences', dest='num_sents', default=sys.maxint, type=int, help='Number of sentences to decode (default=no limit)')
parser.add_argument('-l', '--language-model', dest='lm', default='data/lm', help='File containing ARPA-format language model (default=data/lm)')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,  help='Verbose mode (default=off)')
opts = parser.parse_args()

tm = models.TM(opts.tm, sys.maxint)
lm = models.LM(opts.lm)
sys.stderr.write('Decoding %s...\n' % (opts.input,))
input_sents = [tuple(line.strip().split()) for line in open(opts.input).readlines()[:opts.num_sents]]

def getTranslationOptions(f, h):
    """
    Given a sentence to translate and a translation hypothesis, return all possible translation options available - among the words that haven't been translated. 
    (1). Get all chunks of words that haven't been translated. 
    (2). scan through all chunks of words, and then iterate each chunk, and 
    """
    free_indices = [i for i in xrange(0, len(h.t_indices)) if h.t_indices[i] == False]
    free_chunks = []
    c_start = -1
    c_index = -1
    for i in free_indices:
        if c_start == -1:
            c_start = i
            c_index = i
        elif (c_index + 1) == i: #continue
            c_index = i
        else: #break;
            free_chunks.append((c_start, (c_index + 1)))
            c_start = i
            c_index = i
    free_chunks.append((c_start, (c_index + 1)))
    return free_chunks


# added t_words for translated words.. 
hypothesis = namedtuple('hypothesis', 'logprob, lm_state, t_indices, predecessor, phrase')
for f in input_sents:
    # The following code implements a DP monotone decoding
    # algorithm (one that doesn't permute the target phrases).
    # Hence all hypotheses in stacks[i] represent translations of 
    # the first i words of the input sentence.
    # HINT: Generalize this so that stacks[i] contains translations
    # of any i words (remember to keep track of which words those
    # are, and to estimate future costs)
    initial_hypothesis = hypothesis(0.0, lm.begin(), None, [False]*len(f), None)

    # stack of hypothesis by 0 to sentence length, including the empty (initial) hypothesis.. 
    stacks = [{} for _ in f] + [{}]
    stacks[0][lm.begin()] = initial_hypothesis
    for i, stack in enumerate(stacks[:-1]):
        # extend the top s hypotheses in the current stack, only build a heap queue on the fly.. 
        for h in heapq.nlargest(opts.s, stack.itervalues(), key=lambda h: h.logprob): # prune - TBD: may be fraction based prunning is better? 
            free_chunks = getTranslationOptions(h)
            for (s, e) in free_chunks: # not including e.. 
                for j in xrange(1, (e - s)): #range
                    for k in xrange(s, (e-j+1)):
                        if f[k:(k+j)] in tm: #french phrase in the tm.. 
                            for phrase in tm[f[k:(k+j)]]: # english phrases
        #                        sys.stderr.write("%s\n" % (tm[f[i:j]][0][0]))
                                logprob = h.logprob + phrase.logprob
                                lm_state = h.lm_state
                                for word in phrase.english.split():
                                    (lm_state, word_logprob) = lm.score(lm_state, word)
                                    logprob += word_logprob
                                logprob += lm.end(lm_state) if j == len(f) else 0.0

                                t_indices_this = h.t_indices[:] # create a new list
                                for i in xrange(s, e):
                                    t_indices_this[i] = True
                                new_hypothesis = hypothesis(logprob, lm_state, t_indices_this, h, phrase) #TBD
                                
                                if lm_state not in stacks[j] or stacks[j][lm_state].logprob < logprob: # second case is recombination
                                    stacks[j][lm_state] = new_hypothesis 

    # find best translation by looking at the best scoring hypothesis
    # on the last stack
    winner = max(stacks[-1].itervalues(), key=lambda h: h.logprob)
    def extract_english_recursive(h):
        return '' if h.predecessor is None else '%s%s ' % (extract_english_recursive(h.predecessor), h.phrase.english)
    print extract_english_recursive(winner)

    if opts.verbose:
        def extract_tm_logprob(h):
            return 0.0 if h.predecessor is None else h.phrase.logprob + extract_tm_logprob(h.predecessor)
        tm_logprob = extract_tm_logprob(winner)
        sys.stderr.write('LM = %f, TM = %f, Total = %f\n' % 
            (winner.logprob - tm_logprob, tm_logprob, winner.logprob))
