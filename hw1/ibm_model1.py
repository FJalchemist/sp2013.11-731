#!/usr/bin/env python
import optparse
import sys
from collections import defaultdict

optparser = optparse.OptionParser()
optparser.add_option("-b", "--bitext", dest="bitext", default="data/dev-test-train.de-en", help="Parallel corpus (default data/dev-test-train.de-en)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()

sys.stderr.write("Training IBM model 1...\n")

INIT_TRANS_PROB = 0.01

bitext = [[sentence.strip().split() for sentence in pair.split(' ||| ')] for pair in open(opts.bitext)][:opts.num_sents]
f_count = defaultdict(int)
e_count = defaultdict(int)
fe_count = defaultdict(int)
"""
In the following, n is the sentence order number (id, int), f is the German sentence (list of string), and e is the English sentence (list of string).
"""
for (n, (f, e)) in enumerate(bitext):
    print n
    print f
    print e
#  for f_i in set(f):
#    f_count[f_i] += 1
#    for e_j in set(e):
#      fe_count[(f_i,e_j)] += 1
#  for e_j in set(e):
#    e_count[e_j] += 1
#  if n % 500 == 0:
#    sys.stderr.write(".")