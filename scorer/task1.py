import logging
import argparse
import os

from format_checker.task1 import check_format
"""
Scoring of Task 1 with the metrics Average Precision, R-Precision, P@N, RR@N. 
"""

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)


MAIN_THRESHOLDS = [1, 3, 5, 10, 20, 50]

def _read_gold_and_pred(gold_fpath, pred_fpath):
    """
    Read gold and predicted data.
    :param gold_fpath: the original annotated gold file, where the last 4th column contains the labels.
    :param pred_fpath: a file with line_number and score at each line.
    :return: {line_number:label} dict; list with (line_number, score) tuples.
    """

    logging.info("Reading gold predictions from file {}".format(gold_fpath))

    gold_labels = {}
    with open(gold_fpath) as gold_f:
        for line_res in gold_f:
            line_number, _, _, label = line_res.strip().split('\t')  # process the line from the res file
            gold_labels[int(line_number)] = int(label)

    logging.info('Reading predicted ranking order from file {}'.format(pred_fpath))

    line_score = []
    with open(pred_fpath) as pred_f:
        for line in pred_f:
            line_number, score = line.split('\t')
            line_number = int(line_number.strip())
            score = float(score.strip())

            if line_number not in gold_labels:
                logging.error('No such line_number: {} in gold file!'.format(line_number))
                quit()
            line_score.append((line_number, score))

    if len(set(gold_labels).difference([tup[0] for tup in line_score])) != 0:
        logging.error('The predictions do not match the lines from the gold file - missing or extra line_no')
        raise ValueError('The predictions do not match the lines from the gold file - missing or extra line_no')

    return gold_labels, line_score


def _compute_average_precision(gold_labels, ranked_lines):
    """ Computes Average Precision. """

    precisions = []
    num_correct = 0
    num_positive = sum([1 if v == 1 else 0 for k, v in gold_labels.items()])

    for i, line_number in enumerate(ranked_lines):
        if gold_labels[line_number] == 1:
            num_correct += 1
            precisions.append(num_correct / (i + 1))
    if precisions:
        avg_prec = sum(precisions) / num_positive
    else:
        avg_prec = 0.0

    return avg_prec


def _compute_reciprocal_rank(gold_labels, ranked_lines):
    """ Computes Reciprocal Rank. """
    rr = 0.0
    for i, line_number in enumerate(ranked_lines):
        if gold_labels[line_number] == 1:
            rr += 1.0 / (i + 1)
            break
    return rr


def _compute_precisions(gold_labels, ranked_lines, threshold):
    """ Computes Precision at each line_number in the ordered list. """
    precisions = [0.0] * threshold
    threshold = min(threshold, len(ranked_lines))

    for i, line_number in enumerate(ranked_lines[:threshold]):
        if gold_labels[line_number] == 1:
            precisions[i] += 1.0

    for i in range(1, threshold): # accumulate
        precisions[i] += precisions[i - 1]
    for i in range(1, threshold): # normalize
        precisions[i] /= i+1
    return precisions


def evaluate(gold_fpath, pred_fpath, thresholds=None):
    """
    Evaluates the predicted line rankings w.r.t. a gold file.
    Metrics are: Average Precision, R-Pr, Reciprocal Rank, Precision@N
    :param gold_fpath: the original annotated gold file, where the last 4th column contains the labels.
    :param pred_fpath: a file with line_number at each line, where the list is ordered by check-worthiness.
    :param thresholds: thresholds used for Reciprocal Rank@N and Precision@N.
    If not specified - 1, 3, 5, 10, 20, 50, len(ranked_lines).
    """
    gold_labels, line_score = _read_gold_and_pred(gold_fpath, pred_fpath)

    ranked_lines = [t[0] for t in sorted(line_score, key=lambda x: x[1], reverse=True)]
    if thresholds is None or len(thresholds) == 0:
        thresholds = MAIN_THRESHOLDS + [len(ranked_lines)]

    # Calculate Metrics
    precisions = _compute_precisions(gold_labels, ranked_lines, len(ranked_lines))
    avg_precision = _compute_average_precision(gold_labels, ranked_lines)
    reciprocal_rank = _compute_reciprocal_rank(gold_labels, ranked_lines)
    num_relevant = len({k for k, v in gold_labels.items() if v == 1})

    return thresholds, precisions, avg_precision, reciprocal_rank, num_relevant


def get_threshold_line_format(thresholds, last_entry_name):
    threshold_line_format = '{:<30}' + "".join(['@{:<9}'.format(ind) for ind in thresholds])
    if last_entry_name:
        threshold_line_format = threshold_line_format + '{:<9}'.format(last_entry_name)
    return threshold_line_format

def print_thresholded_metric(title, thresholds, data, last_entry_name=None, last_entry_value=None):
    line_separator = '=' * 120
    threshold_line_format = get_threshold_line_format(thresholds, last_entry_name)
    items = data
    if last_entry_value is not None:
        items = items + [last_entry_value]
    logging.info(threshold_line_format.format(title))
    logging.info('{:<30}'.format("") + "".join(['{0:<10.4f}'.format(item) for item in items]))
    logging.info(line_separator)

def print_single_metric(title, value):
    line_separator = '=' * 120
    logging.info('{:<30}'.format(title) + '{0:<10.4f}'.format(value))
    logging.info(line_separator)

def print_metrics_info(line_separator):
    logging.info('Description of the evaluation metrics: ')
    logging.info('!!! THE OFFICIAL METRIC USED FOR THE COMPETITION RANKING IS MEAN AVERAGE PRECISION (MAP) !!!')
    logging.info('R-Precision is Precision at R, where R is the number of relevant line_numbers for the evaluated set.')
    logging.info('Average Precision is the precision@N, estimated only @ each relevant line_number and then averaged over the number of relevant line_numbers.')
    logging.info('Reciprocal Rank is the reciprocal of the rank of the first relevant line_number in the list of predictions sorted by score (descendingly).')
    logging.info('Precision@N is precision estimated for the first N line_numbers in the provided ranked list.')
    logging.info('The MEAN versions of each metric are provided to average over multiple debates (each with separate prediction file).')
    logging.info(line_separator)
    logging.info(line_separator)


def validate_files(pred_files, gold_files):
    if len(pred_files) != len(gold_files):
        logging.error(
            'Different number of gold files ({}) and pred files ({}) provided. Cannot score.'.format(
                len(gold_files), len(pred_files)
            )
        )
        return False

    if len(pred_files) != len(set(pred_files)):
        logging.error('Same pred file provided multiple times. The pred files should be for different debates.')
        return False

    for pred_file in pred_files:
        if not check_format(pred_file):
            logging.error('Bad format for pred file {}. Cannot score.'.format(pred_file))
            return False

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gold_file_path",
        help="Single string containing a comma separated list of paths to files with gold annotations.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--pred_file_path",
        help="Single string containing a comma separated list of paths to files with ranked line_numbers.",
        type=str,
        required=True
    )
    args = parser.parse_args()

    pred_files = [pred_file.strip() for pred_file in args.pred_file_path.split(",")]
    gold_files = [gold_file.strip() for gold_file in args.gold_file_path.split(",")]
    line_separator = '=' * 120

    if validate_files(pred_files, gold_files):
        logging.info("Started evaluating results for Task 1 ...")
        overall_precisions = [0.0] * len(MAIN_THRESHOLDS)
        mean_r_precision = 0.0
        mean_avg_precision = 0.0
        mean_reciprocal_rank = 0.0

        for (pred_file, gold_file) in zip(pred_files, gold_files):
            thresholds, precisions, avg_precision, reciprocal_rank, num_relevant = evaluate(gold_file, pred_file)
            threshold_precisions = [precisions[th - 1] for th in MAIN_THRESHOLDS]
            r_precision = precisions[num_relevant - 1]

            for idx in range(0, len(MAIN_THRESHOLDS)):
                overall_precisions[idx] += threshold_precisions[idx]
            mean_r_precision += r_precision
            mean_avg_precision += avg_precision
            mean_reciprocal_rank += reciprocal_rank

            filename = os.path.basename(pred_file)
            logging.info('{:=^120}'.format(' RESULTS for {} '.format(filename)))
            print_single_metric('AVERAGE PRECISION:', avg_precision)
            print_single_metric('RECIPROCAL RANK:', reciprocal_rank)
            print_single_metric('R-PRECISION (R={}):'.format(num_relevant), r_precision)
            print_thresholded_metric('PRECISION@N:', MAIN_THRESHOLDS, threshold_precisions)

        debate_count = len(pred_files)
        if debate_count > 1:
            overall_precisions = [item * 1.0 / debate_count for item in overall_precisions]
            mean_r_precision /= debate_count
            mean_avg_precision /= debate_count
            mean_reciprocal_rank /= debate_count
            logging.info('{:=^120}'.format(' AVERAGED RESULTS '))
            print_single_metric('MEAN AVERAGE PRECISION (MAP):', mean_avg_precision)
            print_single_metric('MEAN RECIPROCAL RANK:', mean_reciprocal_rank)
            print_single_metric('MEAN R-PRECISION:', mean_r_precision)
            print_thresholded_metric('MEAN PRECISION@N:', MAIN_THRESHOLDS, overall_precisions)

        print_metrics_info(line_separator)

