#!/usr/bin/env python
import optparse
import sys
from collections import defaultdict

"""
check wether the translation probability is converged.
returns true if it does.
"""
def checkConvergence(t_now, t_old):
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
        set_e.update(set(e))
        set_f.update(set(f))

        s-total = defaultdict(float)
        for eword in e:
            for fword in f:
                if t_now[e] != 0:
                    s-total[e] += t_now[e + GIVEN + f]
                else:
                    t_now[e + GIVEN + f] = INIT_TRANS_PROB
                    s-total(e) += t_now[e + GIVEN + f]
        for eword in e:
            for fword in f:
                count[e + GIVEN + f] += t_now[e + GIVEN + f] / s-total[e]
                total[f] += t_now[e + GIVEN + f] / s-total[e]
    for 

    #  for f_i in set(f):
    #    f_count[f_i] += 1
    #    for e_j in set(e):
    #      fe_count[(f_i,e_j)] += 1
    #  for e_j in set(e):
    #    e_count[e_j] += 1
    #  if n % 500 == 0:
    #    sys.stderr.write(".")


