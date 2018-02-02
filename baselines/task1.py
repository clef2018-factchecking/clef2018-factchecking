import pandas as pd
import random
from os.path import join, dirname

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

from scorer.task1 import evaluate
from format_checker.task1 import check_format

random.seed(1)
_COL_NAMES = ['line_number', 'speaker', 'text', 'label']

def run_random_baseline(gold_fpath, results_fpath):
    gold_df = pd.read_csv(gold_fpath, names=_COL_NAMES, sep='\t')
    with open(results_fpath, "w") as results_file:
        for i, line in gold_df.iterrows():
            results_file.write('{}\t{}\n'.format(line['line_number'], random.random()))


def run_ngram_baseline(train_debates, test_debate, results_fpath):
    test_df = pd.read_csv(test_debate, names=_COL_NAMES, sep='\t')

    train_list = []
    for train_debate in train_debates:
        df = pd.read_csv(train_debate, index_col=None, header=None, names=_COL_NAMES, sep='\t')
        train_list.append(df)
    train_df = pd.concat(train_list)

    pipeline = Pipeline([
        ('ngrams', TfidfVectorizer()),
        ('clf', SVC(C=1, kernel='rbf', random_state=0))
    ])
    pipeline.fit(train_df['text'], train_df['label'])

    with open(results_fpath, "w") as results_file:
        predicted_distance = pipeline.decision_function(test_df['text'])
        for line_num, dist in zip(test_df['line_number'], predicted_distance):
            results_file.write("{}\t{}\n".format(line_num, dist))


if __name__ == '__main__':
    ROOT_DIR = dirname(dirname(__file__))
    gold_data_folder = join(ROOT_DIR, 'gold_data/task1/English')

    train_debates = [join(gold_data_folder, 'Task1-English-1st-Presidential.txt'),
                     join(gold_data_folder, 'Task1-English-Vice-Presidential.txt')]
    test_debate = join(gold_data_folder, 'Task1-English-2nd-Presidential.txt')

    random_baseline_fpath = join(ROOT_DIR, 'baselines/data/task1_random_baseline.txt')
    run_random_baseline(test_debate, random_baseline_fpath)
    if check_format(random_baseline_fpath):
        evaluate(test_debate, random_baseline_fpath)

    ngram_baseline_fpath = join(ROOT_DIR, 'baselines/data/task1_ngram_baseline.txt')
    run_ngram_baseline(train_debates, test_debate, ngram_baseline_fpath)
    if check_format(ngram_baseline_fpath):
        evaluate(test_debate, ngram_baseline_fpath)


