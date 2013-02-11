#!/usr/bin/env python
import optparse
import sys
from collections import defaultdict

def checkConvergence(t_now, t_old):
    """
    check wether the translation probability is converged.
    returns true if it does.
    """
    THRESHOLD = 0.01;
    if len(t_old) != len(t_now):
        #Second iteration
        return False
    if len(t_now) = 0: 
        #First iteration
        return False
    sumsq = 0.0;
    for key in t_now:
        sumsq += (t_now[key] - t_old[key])**2
    if THRESHOLD > sumsq:
        return True
    else:
        return False

def simpleAlignmentEst(t_prob, e, f):
    """
    a simple, greedy alignment estimation from english to foreign sentence. A decoding method coming from hindi-english-word-alignment (http://code.google.com/p/hindi-english-word-alignment).
    """
    alignment = []
    for i in range(len(e)):
        best_align = (-1.0, -1)
        for j in range(len(f)):
            fword = f[j]
            if t_prob[eword + GIVEN + fword] > best_align[0]:
                best_align[0] = t_prob[eword + GIVEN + fword]
                best_align[1] = i
        alignment.append((j,i))
    return alignment

optparser = optparse.OptionParser()
optparser.add_option("-b", "--bitext", dest="bitext", default="data/dev-test-train.de-en", help="Parallel corpus (default data/dev-test-train.de-en)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()

sys.stderr.write("Training IBM model 1...\n")

INIT_TRANS_PROB = 0.01
GIVEN = "->"

bitext = [[sentence.strip().split() for sentence in pair.split(' ||| ')] for pair in open(opts.bitext)][:opts.num_sents]
cnt = 0
t_now = defaultdict(float)
t_old = defaultdict(float)
set_e = set()
set_f = set()
while not checkConvergence(t_now, t_old):
    count = defaultdict(float)
    total = defaultdict(float)
    """
    In the following, n is the sentence order number (id, int), f is the German sentence (list of string), and e is the English sentence (list of string).
    """
    for (n, (f, e)) in enumerate(bitext):
        #get all unique tokens in e and f.
        set_e.update(set(e))
        set_f.update(set(f))

        s-total = defaultdict(float)
        for eword in e:
            for fword in f:
                if t_now[eword] != 0:
                    s-total[eword] += t_now[eword + GIVEN + fword]
                else:
                    t_now[eword + GIVEN + fword] = INIT_TRANS_PROB
                    s-total(eword) += t_now[eword + GIVEN + fword]
        #E
        for eword in e:
            for fword in f:
                count[eword + GIVEN + fword] += t_now[eword + GIVEN + fword] / s-total[eword]
                total[fword] += t_now[eword + GIVEN + fword] / s-total[eword]
    t_old = t_now
    #M
    for eword in set_e:
        for fword in set_f:
            t_now[eword + GIVEN + fword] = count[eword + GIVEN + fword] / total[fword]


    #  for f_i in set(f):
    #    f_count[f_i] += 1
    #    for e_j in set(e):
    #      fe_count[(f_i,e_j)] += 1
    #  for e_j in set(e):
    #    e_count[e_j] += 1
    #  if n % 500 == 0:
    #    sys.stderr.write(".")


