# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
from __future__ import print_function

import six
from six.moves import map

from nlgeval.pycocoevalcap.bleu.bleu import Bleu
from nlgeval.pycocoevalcap.cider.cider import Cider
from nlgeval.pycocoevalcap.meteor.meteor import Meteor
from nlgeval.pycocoevalcap.rouge.rouge import Rouge
from nlgeval.pycocoevalcap.spice.spice import Spice

# str/unicode stripping in Python 2 and 3 instead of `str.strip`.
def _strip(s):
    return s.strip()


def compute_metrics(hypothesis, references):
    with open(hypothesis, 'r') as f:
        hyp_list = f.readlines()
    ref_list = []
    for reference in references:
        with open(reference, 'r') as f:
            ref_list.append(f.readlines())
    ref_list = [list(map(_strip, refs)) for refs in zip(*ref_list)]
    refs = {idx: strippedlines for (idx, strippedlines) in enumerate(ref_list)}
    hyps = {idx: [lines.strip()] for (idx, lines) in enumerate(hyp_list)}
    assert len(refs) == len(hyps)

    ret_scores = {}
    scorers = [
        (Bleu(4), ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]),
        (Meteor(), "METEOR"),
        (Rouge(), "ROUGE_L"),
        (Cider(), "CIDEr"),
        (Spice(), "SPICE")
    ]
    for scorer, method in scorers:
        score, _ = scorer.compute_score(refs, hyps)
        if isinstance(method, list):
            for sc, m in zip(score, method):
                print("%s: %0.6f" % (m, sc))
                ret_scores[m] = sc
        else:
            print("%s: %0.6f" % (method, score))
            ret_scores[method] = score
        if isinstance(scorer, Meteor):
            scorer.close()
    del scorers

    return ret_scores


def compute_individual_metrics(ref, hyp):
    assert isinstance(hyp, six.string_types)

    if isinstance(ref, six.string_types):
        ref = ref.split('||<|>||')  # special delimiter for backward compatibility
    ref = [a.strip() for a in ref]
    refs = {0: ref}

    hyps = {0: [hyp.strip()]}

    ret_scores = {}
    scorers = [
        (Bleu(4), ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]),
        (Meteor(), "METEOR"),
        (Rouge(), "ROUGE_L"),
        (Cider(), "CIDEr"),
        (Spice(), "SPICE")            
    ]
    for scorer, method in scorers:
        score, _ = scorer.compute_score(refs, hyps)
        if isinstance(method, list):
            for sc, m in zip(score, method):
                ret_scores[m] = sc
        else:
            ret_scores[method] = score
        if isinstance(scorer, Meteor):
            scorer.close()
    del scorers

    return ret_scores


class NLGEval(object):

    valid_metrics = {
                        'Bleu_1', 'Bleu_2', 'Bleu_3', 'Bleu_4',
                        'METEOR',
                        'ROUGE_L',
                        'CIDEr',
                        'SPICE',
                    }

    def __init__(self, metrics_to_omit=None):
        """
        :param metrics_to_omit: Default: Use all metrics. See `NLGEval.valid_metrics` for all metrics.
            The previous parameters will override metrics in this one if they are set.
            Metrics to omit. Omitting Bleu_{i} will omit Bleu_{j} for j>=i.
        :type metrics_to_omit: Optional[Collection[str]]
        """

        if metrics_to_omit is None:
            self.metrics_to_omit = set()
        else:
            self.metrics_to_omit = set(metrics_to_omit)

        assert len(self.metrics_to_omit - self.valid_metrics) == 0, \
            "Invalid metrics to omit: {}".format(self.metrics_to_omit - self.valid_metrics)

        self.load_scorers()

    def load_scorers(self):
        self.scorers = []

        omit_bleu_i = False
        for i in range(1, 4 + 1):
            if 'Bleu_{}'.format(i) in self.metrics_to_omit:
                omit_bleu_i = True
                if i > 1:
                    self.scorers.append((Bleu(i - 1), ['Bleu_{}'.format(j) for j in range(1, i)]))
                break
        if not omit_bleu_i:
            self.scorers.append((Bleu(4), ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]))

        if 'METEOR' not in self.metrics_to_omit:
            self.scorers.append((Meteor(), "METEOR"))
        if 'ROUGE_L' not in self.metrics_to_omit:
            self.scorers.append((Rouge(), "ROUGE_L"))
        if 'CIDEr' not in self.metrics_to_omit:
            self.scorers.append((Cider(), "CIDEr"))
        if 'SPICE' not in self.metrics_to_omit:
            self.scorers.append((Spice(), "SPICE"))

    def compute_individual_metrics(self, ref, hyp):
        assert isinstance(hyp, six.string_types)
        ref = [a.strip() for a in ref]
        refs = {0: ref}

        hyps = {0: [hyp.strip()]}

        ret_scores = {}
        for scorer, method in self.scorers:
            score, _ = scorer.compute_score(refs, hyps)
            if isinstance(method, list):
                for sc, m in zip(score, method):
                    ret_scores[m] = sc
            else:
                ret_scores[method] = score

        return ret_scores

    def compute_metrics(self, ref_list, hyp_list):
        ref_list = [list(map(_strip, refs)) for refs in zip(*ref_list)]
        refs = {idx: strippedlines for (idx, strippedlines) in enumerate(ref_list)}
        hyps = {idx: [lines.strip()] for (idx, lines) in enumerate(hyp_list)}
        assert len(refs) == len(hyps)

        ret_scores = {}
        for scorer, method in self.scorers:
            score, _ = scorer.compute_score(refs, hyps)
            if isinstance(method, list):
                for sc, m in zip(score, method):
                    ret_scores[m] = sc
            else:
                ret_scores[method] = score

        return ret_scores
