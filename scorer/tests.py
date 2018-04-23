from unittest import TestCase
from os.path import dirname, join

from scorer import task1, task2

_ROOT_DIR = dirname(dirname(__file__))
_GOLD_FILE_1 = join(_ROOT_DIR, 'data/task1/English/Task1-English-1st-Presidential.txt')
_PRED_FILE_1 = join(_ROOT_DIR, 'scorer/data/task1_random_baseline.txt')
_PRED_FILE_1_NOTFULL = join(_ROOT_DIR, 'scorer/data/task1_not_all_lines.txt')
_GOLD_FILE_2 = join(_ROOT_DIR, 'data/task2/English/Task2-English-1st-Presidential.txt')
_PRED_FILE_2 = join(_ROOT_DIR, 'scorer/data/task2_random_baseline.txt')
_PRED_FILE_2_NOTFULL = join(_ROOT_DIR, 'scorer/data/task2_not_all_claims.txt')


class ScorerTask1(TestCase):
    def test_average_precision(self):
        y_gold_labels = {1: 0, 2: 1, 3: 0, 4: 0, 5: 1}
        y_pred_ranked = [1, 2, 3, 4, 5]
        num_relevant = 2
        avg_p = task1._compute_average_precision(y_gold_labels, y_pred_ranked)
        self.assertEqual(avg_p, (0.5+0.4)/num_relevant)

        y_gold_labels = {1: 1, 2: 0, 3: 1, 4: 0, 5: 1}
        y_pred_ranked = [1, 2, 3, 4, 5]
        num_relevant = 3
        avg_p = task1._compute_average_precision(y_gold_labels, y_pred_ranked)
        self.assertEqual(avg_p, (1 + 2/3 + 3/5)/num_relevant)

        y_gold_labels = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        y_pred_ranked = [1, 2, 3, 4, 5]
        avg_p = task1._compute_average_precision(y_gold_labels, y_pred_ranked)
        self.assertEqual(avg_p, 0)

    def test_precisions(self):
        y_gold_labels = {1: 1, 2: 0, 3: 1, 4: 0, 5: 1}
        y_pred_ranked = [1, 2, 3, 4, 5]
        prec = task1._compute_precisions(y_gold_labels, y_pred_ranked, len(y_pred_ranked))
        self.assertEqual(prec, [1, 0.5, 2/3, 2/4, 3/5])

        y_gold_labels = {1: 0, 2: 0}
        y_pred_ranked = [1, 2]
        prec = task1._compute_precisions(y_gold_labels, y_pred_ranked, len(y_pred_ranked))
        self.assertEqual(prec, [0, 0])

    def test_reciprocal_rank(self):
        y_gold_labels = {1: 1, 2: 0, 3: 1, 4: 0, 5: 1}

        rr = task1._compute_reciprocal_rank(y_gold_labels, [1, 2, 3, 4, 5])
        self.assertEqual(rr, 1)
        rr = task1._compute_reciprocal_rank(y_gold_labels, [5, 4, 3, 2, 1])
        self.assertEqual(rr, 1)
        rr = task1._compute_reciprocal_rank(y_gold_labels, [2, 4, 1, 3, 5])
        self.assertEqual(rr, 1/3)
        rr = task1._compute_reciprocal_rank(y_gold_labels, [2, 5, 4, 1, 3])
        self.assertEqual(rr, 1/2)

    def test_read_gold_and_pred(self):
        gold_labels, pred_ranked = task1._read_gold_and_pred(_GOLD_FILE_1, _PRED_FILE_1)

        self.assertEqual(list(gold_labels.keys()), [p[0] for p in pred_ranked])
        self.assertGreater(len([k for k, v in gold_labels.items() if v == 1]), 20)
        self.assertGreater(len([k for k, v in gold_labels.items() if v == 0]), 1000)

        with self.assertRaises(ValueError):
          task1._read_gold_and_pred(_GOLD_FILE_1, _PRED_FILE_1_NOTFULL)


class ScorerTask2(TestCase):
    def test_accuracy(self):
        conf_matrix = {'true': {'true': 0, 'false': 2, 'half-true': 3},
                       'false': {'true': 2, 'false': 2, 'half-true': 3},
                       'half-true': {'true': 2, 'false': 3, 'half-true': 1}}
        self.assertEqual(task2._compute_accuracy(conf_matrix), 3 / 18)

        conf_matrix = {'true': {'true': 0, 'false': 2, 'half-true': 3},
                       'false': {'true': 2, 'false': 0, 'half-true': 3},
                       'half-true': {'true': 2, 'false': 3, 'half-true': 0}}
        self.assertEqual(task2._compute_accuracy(conf_matrix), 0 / 15)

    def test_recall(self):
        conf_matrix = {'true': {'true': 0, 'false': 2, 'half-true': 3},
                       'false': {'true': 2, 'false': 2, 'half-true': 3},
                       'half-true': {'true': 2, 'false': 3, 'half-true': 1}}
        self.assertEqual(task2._compute_macro_recall(conf_matrix), (0 + 2 / 7 + 1 / 6) / 3)

        conf_matrix = {'true': {'true': 0, 'false': 2, 'half-true': 3},
                       'false': {'true': 2, 'false': 0, 'half-true': 3},
                       'half-true': {'true': 2, 'false': 3, 'half-true': 0}}
        self.assertEqual(task2._compute_macro_recall(conf_matrix), (0 + 0 / 5 + 0 / 5) / 3)

    def test_f1(self):
        conf_matrix = {'true': {'true': 0, 'false': 2, 'half-true': 3},
                       'false': {'true': 2, 'false': 2, 'half-true': 3},
                       'half-true': {'true': 2, 'false': 3, 'half-true': 1}}
        p_true = 0
        r_true = 0
        p_false = 2/7
        r_false = 2/7
        p_half_true = 1/7
        r_half_true = 1/6
        self.assertEqual(task2._compute_macro_f1(conf_matrix),
                         sum([2*p*r/(p+r) for p, r in zip([p_false, p_half_true],[r_false, r_half_true])]) / 3)

        conf_matrix = {'true': {'true': 0, 'false': 1, 'half-true': 0},
                       'false': {'true': 1, 'false': 0, 'half-true': 0},
                       'half-true': {'true': 0, 'false': 1, 'half-true': 0}}

        self.assertEqual(task2._compute_macro_f1(conf_matrix), 0)

    def test_read(self):
        gold_labels, pred_labels = task2._read_gold_and_pred(_GOLD_FILE_2, _PRED_FILE_2, 'pref1-')
        self.assertEqual(gold_labels.keys(), pred_labels.keys())
        self.assertGreater(len(gold_labels), 20)
        self.assertTrue(all([True if claim_id.startswith('pref1-') else False for claim_id in gold_labels.keys()]),
          'Reading function should prefix all claim numbers with the provided prefix')
        self.assertTrue(all([True if claim_id.startswith('pref1-') else False for claim_id in pred_labels.keys()]),
          'Reading function should prefix all claim numbers with the provided prefix')

        with self.assertRaises(ValueError):
          task2._read_gold_and_pred(_GOLD_FILE_2, _PRED_FILE_2_NOTFULL)

    def test_conf_matrix(self):
        gold_labels = {1: 'true', 2: 'true', 3: 'half-true', 4: 'false'}
        pred_labels = {1: 'false', 2: 'true', 3:'false', 4: 'false'}

        conf_matrix = {'true': {'true': 1, 'false': 1, 'half-true': 0},
                       'false': {'true': 0, 'false': 1, 'half-true': 0},
                       'half-true': {'true': 0, 'false': 1, 'half-true': 0}}

        self.assertEqual(task2._compute_confusion_matrix(gold_labels, pred_labels), conf_matrix)

    def test_mean_absolute_error(self):
        conf_matrix = {'true': {'true': 1, 'false': 0, 'half-true': 0},
                       'false': {'true': 0, 'false': 2, 'half-true': 0},
                       'half-true': {'true': 0, 'false': 0, 'half-true': 3}}
        self.assertEqual(task2._compute_mean_absolute_error(conf_matrix), 0)

        conf_matrix = {'true': {'true': 0, 'false': 0, 'half-true': 3},
                       'false': {'true': 0, 'false': 0, 'half-true': 4},
                       'half-true': {'true': 1, 'false': 2, 'half-true': 0}}
        self.assertEqual(task2._compute_mean_absolute_error(conf_matrix), 1)

        conf_matrix = {'true': {'true': 0, 'false': 2, 'half-true': 0},
                       'false': {'true': 1, 'false': 0, 'half-true': 0},
                       'half-true': {'true': 0, 'false': 0, 'half-true': 0}}
        self.assertEqual(task2._compute_mean_absolute_error(conf_matrix), 2)

    def test_macro_averaged_mae(self):
        conf_matrix = {'true': {'true': 1, 'false': 0, 'half-true': 0},
                       'false': {'true': 0, 'false': 2, 'half-true': 0},
                       'half-true': {'true': 0, 'false': 0, 'half-true': 3}}
        self.assertEqual(task2._compute_macro_averaged_mae(conf_matrix), 0)

        conf_matrix = {'true': {'true': 1, 'false': 0, 'half-true': 0},
                       'false': {'true': 0, 'false': 1, 'half-true': 0},
                       'half-true': {'true': 1, 'false': 2, 'half-true': 1}}
        expected = (0 + 0 + 3/4) / 3
        self.assertEqual(task2._compute_macro_averaged_mae(conf_matrix), expected)

        conf_matrix = {'true': {'true': 1, 'false': 0, 'half-true': 1},
                       'false': {'true': 0, 'false': 1, 'half-true': 2},
                       'half-true': {'true': 1, 'false': 0, 'half-true': 1}}
        expected = (1/2 + 2/3 + 1/2) / 3
        self.assertEqual(task2._compute_macro_averaged_mae(conf_matrix), expected)

        conf_matrix = {'true': {'true': 1, 'false': 2, 'half-true': 0},
                       'false': {'true': 1, 'false': 1, 'half-true': 0},
                       'half-true': {'true': 0, 'false': 0, 'half-true': 1}}
        expected = (4/3 + 2/2 + 0) / 3
        self.assertEqual(task2._compute_macro_averaged_mae(conf_matrix), expected)

        conf_matrix = {'true': {'true': 1, 'false': 0, 'half-true': 0},
                       'false': {'true': 1, 'false': 1, 'half-true': 0},
                       'half-true': {'true': 1, 'false': 0, 'half-true': 1}}
        expected = (0 + 2/2 + 1/2) / 3
        self.assertEqual(task2._compute_macro_averaged_mae(conf_matrix), expected)

