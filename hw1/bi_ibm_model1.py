#!/usr/bin/env python
import optparse
import sys
from collections import defaultdict

"""
This file is the same as the ibm_model1.py, but training the translation probability in both directions, according to section 4.5.3 of the Keohn book.
"""

def checkConvergence(t_now, t_old):
    """
    check wether the translation probability is converged.
    returns true if it does.
    """
    THRESHOLD = 0.15;
    if len(t_now) == 0: 
        #First iteration
        return False
    sumsq = 0.0;
    for key in t_now:
#        sys.stderr.write("%s, %f, " % (key, (t_now[key] - t_old[key])**2))
        sumsq += (t_now[key] - t_old[key])**2
    sys.stderr.write("sumsq: %f.\n" % sumsq)
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
        eword = e[i]
        best_align = (-1.0, -1)
        for j in range(len(f)):
            fword = f[j]
            if t_prob[eword , fword] > best_align[0]:
                best_align = (t_prob[eword , fword], j)
        alignment.append((best_align[1],i))
    return sorted(alignment)

def getBestAlignments(t_prob, bitext):
    """
    Print all best alignments in the training data
    """
    res = []
    for (n, (f, e)) in enumerate(bitext):
        alignment = simpleAlignmentEst(t_prob, e, f)
        res.append(alignment)
    return res

def printCombinedAlignments(align_list1, align_list2):
    """
    use set intersection
    """
    intersec = []
    #reverse the list to make it the same order as list 1.
    align_list2_rev = []
    for i in range(len(align_list2)):
        align_list2_rev.append([])
        for (e_i, f_i) in align_list2[i]:
            align_list2_rev[i].append((f_i, e_i))

    for i in range(len(align_list1)):
        intersec.append([])
        for a_align1 in align_list1[i]:
            for a_align2 in align_list2_rev[i]:
                if a_align1 == a_align2:
                    intersec[i].append(a_align1)
                    break
        intersec[i] = sorted(intersec[i])
    
    res = []
    for i in range(len(align_list1)):
        res.append([])
        for a_align1 in align_list1[i]:
            for a_res_align in intersec[i]:
                if abs(a_res_align[0]-a_align1[0]) + abs(a_res_align[1]-a_align1[1]) <= 2:
                    res[i].append(a_align1)
                    break
        for a_align2 in align_list2_rev[i]:
            for a_res_align in intersec[i]:
                if abs(a_res_align[0]-a_align2[0]) + abs(a_res_align[1]-a_align2[1]) <= 2:
                    res[i].append(a_align2)
                    break
        res[i] = sorted(res[i])

    for i in range(len(res)):
        for (f_i, e_i) in res[i]:
            sys.stdout.write("%i-%i " % (f_i, e_i))
        sys.stdout.write("\n")


def trainIBMModel1(bitext):
    INIT_TRANS_PROB = 0.1
    cnt = 0
    t_now = {}
    t_old = None
    while cnt < 10:
        cnt += 1
        sys.stderr.write("\n%i-th iteration." % cnt)

        count = {}
        total = {}
        """
        In the following, n is the sentence order number (id, int), f is the German sentence (list of string), and e is the English sentence (list of string).
        """
        for (n, (f, e)) in enumerate(bitext):
            s_total = defaultdict(float)
            for eword in e:
                for fword in f:
                    if t_now.get((eword, fword), 0.0) != 0.0:
                        s_total[eword] += t_now[eword, fword]
                    else:
                        t_now[eword, fword] = INIT_TRANS_PROB
                        s_total[eword] += t_now[eword, fword]
            #E
            for eword in e:
                for fword in f:
                    if count.get((eword, fword), 0.0) == 0.0:
                        count[eword, fword] = t_now[eword, fword] / s_total[eword]
                    else:
                        count[eword, fword] += t_now[eword, fword] / s_total[eword]
                    if total.get(fword, 0.0) == 0.0:
                        total[fword] = t_now[eword, fword] / s_total[eword]
                    else:
                        total[fword] += t_now[eword, fword] / s_total[eword]

            if n % 1000 == 0:
                sys.stderr.write(".")
        t_now = {}
        #M
        if cnt == 1:
            sys.stderr.write("count size: %i.\n" % len(count))
        for key in count:
            eword = key[0]
            fword = key[1]
    #        sys.stderr.write("fword: %s.\n" % fword)
            if total.get(fword, 0.0) != 0.0:
                t_now[key] = count[key] / total[fword]
    return getBestAlignments(t_now, bitext) 

optparser = optparse.OptionParser()
optparser.add_option("-b", "--bitext", dest="bitext", default="data/dev-test-train.de-en", help="Parallel corpus (default data/dev-test-train.de-en)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()

sys.stderr.write("Training IBM model 1...\n")

bitext = [[sentence.strip().split() for sentence in pair.split(' ||| ')] for pair in open(opts.bitext)][:opts.num_sents]
bitext_rev = []
for (n, (f, e)) in enumerate(bitext):
    bitext_rev.append((e,f))

align_list1 = trainIBMModel1(bitext)
align_list2 = trainIBMModel1(bitext_rev)

printCombinedAlignments(align_list1, align_list2)
