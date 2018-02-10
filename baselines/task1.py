import pandas as pd
import random
from os.path import join, dirname

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

from scorer.task1 import evaluate
from format_checker.task1 import check_format

random.seed(0)
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
        ('ngrams', TfidfVectorizer(ngram_range=(1, 1))),
        ('clf', SVC(C=10, gamma=0.1, kernel='rbf', random_state=0))
    ])
    pipeline.fit(train_df['text'], train_df['label'])

    with open(results_fpath, "w") as results_file:
        predicted_distance = pipeline.decision_function(test_df['text'])
        for line_num, dist in zip(test_df['line_number'], predicted_distance):
            results_file.write("{}\t{}\n".format(line_num, dist))


def run_baselines(lang='English'):
    ROOT_DIR = dirname(dirname(__file__))

    gold_data_folder = join(ROOT_DIR, 'data/task1/{}'.format(lang))

    train_debates = [join(gold_data_folder, 'Task1-{}-1st-Presidential.txt'.format(lang)),
                     join(gold_data_folder, 'Task1-{}-Vice-Presidential.txt'.format(lang))]
    test_debate = join(gold_data_folder, 'Task1-{}-2nd-Presidential.txt'.format(lang))

    random_baseline_fpath = join(ROOT_DIR, 'baselines/data/task1_random_baseline_{}.txt'.format(lang))
    run_random_baseline(test_debate, random_baseline_fpath)
    if check_format(random_baseline_fpath):
        evaluate(test_debate, random_baseline_fpath)

    ngram_baseline_fpath = join(ROOT_DIR, 'baselines/data/task1_ngram_baseline_{}.txt'.format(lang))
    run_ngram_baseline(train_debates, test_debate, ngram_baseline_fpath)
    if check_format(ngram_baseline_fpath):
        evaluate(test_debate, ngram_baseline_fpath)


if __name__ == '__main__':
    run_baselines('English')
    run_baselines('Arabic')



