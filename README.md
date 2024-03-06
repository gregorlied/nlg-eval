[![Build Status](https://travis-ci.org/Maluuba/nlg-eval.svg?branch=master)](https://travis-ci.org/Maluuba/nlg-eval)

# nlg-eval
Evaluation code for various unsupervised automated metrics for NLG (Natural Language Generation).
It takes as input a hypothesis file, and one or more references files and outputs values of metrics.
Rows across these files should correspond to the same example.

## Metrics ##
- BLEU
- METEOR
- ROUGE
- CIDEr

## Setup ##

Install Java 1.8.0 (or higher).

Install the Python dependencies, run:
```bash
pip install git+https://github.com/Maluuba/nlg-eval.git@master
```

If you are using macOS High Sierra or higher, then run this to allow multithreading:
```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

Simple setup (download required data (e.g. models, embeddings) and external code files), run:
```bash
nlg-eval --setup
```

If you're setting this up from the source code or you're on Windows and not using a Bash terminal, then you might get errors about `nlg-eval` not being found.
You will need to find the `nlg-eval` script.
See [here](https://github.com/Maluuba/nlg-eval/issues/61) for details.

### Custom Setup ###
```bash
# If you don't like the default path (~/.cache/nlgeval) for the downloaded data,
# then specify a path where you want the files to be downloaded.
# The value for the data path is stored in ~/.config/nlgeval/rc.json and can be overwritten by
# setting the NLGEVAL_DATA environment variable.
nlg-eval --setup ${data_path}
```

## Usage ##
Once setup has completed, the metrics can be evaluated with a Python API or in the command line.

Examples of the Python API can be found in [test_nlgeval.py](nlgeval/tests/test_nlgeval.py).

### Standalone ###

    nlg-eval --hypothesis=examples/hyp.txt --references=examples/ref1.txt --references=examples/ref2.txt

where each line in the hypothesis file is a generated sentence and the corresponding
lines across the reference files are ground truth reference sentences for the
corresponding hypothesis.

### functional API: for the entire corpus ###

```python
from nlgeval import compute_metrics
metrics_dict = compute_metrics(hypothesis='examples/hyp.txt',
                               references=['examples/ref1.txt', 'examples/ref2.txt'])
```

### functional API: for only one sentence ###

```python
from nlgeval import compute_individual_metrics
metrics_dict = compute_individual_metrics(references, hypothesis)
```

where `references` is a list of ground truth reference text strings and
`hypothesis` is the hypothesis text string.

### object oriented API for repeated calls in a script - single example ###

```python
from nlgeval import NLGEval
nlgeval = NLGEval()  # loads the models
metrics_dict = nlgeval.compute_individual_metrics(references, hypothesis)
```

where `references` is a list of ground truth reference text strings and
`hypothesis` is the hypothesis text string.

### object oriented API for repeated calls in a script - multiple examples ###

```python
from nlgeval import NLGEval
nlgeval = NLGEval()  # loads the models
metrics_dict = nlgeval.compute_metrics(references, hypothesis)
```

where `references` is a list of lists of ground truth reference text strings and
`hypothesis` is a list of hypothesis text strings. Each inner list in `references`
is one set of references for the hypothesis (a list of single reference strings for
each sentence in `hypothesis` in the same order).

## Reference ##
If you use this code as part of any published research, please cite the following paper:

Shikhar Sharma, Layla El Asri, Hannes Schulz, and Jeremie Zumer.
**"Relevance of Unsupervised Metrics in Task-Oriented Dialogue for Evaluating Natural Language Generation"**
*arXiv preprint arXiv:1706.09799* (2017)

```bibtex
@article{sharma2017nlgeval,
    author  = {Sharma, Shikhar and El Asri, Layla and Schulz, Hannes and Zumer, Jeremie},
    title   = {Relevance of Unsupervised Metrics in Task-Oriented Dialogue for Evaluating Natural Language Generation},
    journal = {CoRR},
    volume  = {abs/1706.09799},
    year    = {2017},
    url     = {http://arxiv.org/abs/1706.09799}
}
```

## Example ##
Running

    nlg-eval --hypothesis=examples/hyp.txt --references=examples/ref1.txt --references=examples/ref2.txt

gives

    Bleu_1: 0.550000
    Bleu_2: 0.428174
    Bleu_3: 0.284043
    Bleu_4: 0.201143
    METEOR: 0.295797
    ROUGE_L: 0.522104
    CIDEr: 1.242192

## Troubleshooting
If you have issues with Meteor then you can try lowering the `mem` variable in meteor.py

## Important Note ##
CIDEr by default (with idf parameter set to "corpus" mode) computes IDF values using the reference sentences provided. Thus,
CIDEr score for a reference dataset with only 1 image (or example for NLG) will be zero. When evaluating using one (or few)
images, set idf to "coco-val-df" instead, which uses IDF from the MSCOCO Vaildation Dataset for reliable results. This has
not been adapted in this code. For this use-case, apply patches from
[vrama91/coco-caption](https://github.com/vrama91/coco-caption).


## External data directory

To mount an already prepared data directory to a Docker container or share it between
users, you can set the `NLGEVAL_DATA` environment variable to let nlg-eval know
where to find its models and data.  E.g.

    NLGEVAL_DATA=~/workspace/nlg-eval/nlgeval/data

This variable overrides the value provided during setup (stored in `~/.config/nlgeval/rc.json`)

## Microsoft Open Source Code of Conduct ##
This project has adopted the [Microsoft Open Source Code of
Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct
FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com)
with any additional questions or comments.

## License ##
See [LICENSE.md](LICENSE.md).
