import logging
import argparse
from format_checker.subtaskA import check_format
"""
Scoring of Subtask A with the metrics Average Precision, R-Precision, P@N, RR@N. 
"""

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


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

    if len(gold_labels) != len(line_score):
        logging.warning('You have missed some line_numbers in your prediction file.')

    return gold_labels, line_score


def _compute_average_precision(gold_labels, ranked_lines, threshold):
    """ Computes Average Precision. """

    precisions = []
    num_correct = 0
    threshold = min(threshold, len(ranked_lines))

    for i, line_number in enumerate(ranked_lines[:threshold]):
        if gold_labels[line_number] == 1:
            num_correct += 1
            precisions.append(num_correct / (i + 1))
    if precisions:
        avg_prec = sum(precisions) / len(precisions)
    else:
        avg_prec = 0.0

    return avg_prec


def _compute_reciprocal_rank(gold_labels, ranked_lines, threshold):
    """ Computes Mean Reciprocal Rank. """
    rr = 0.0
    threshold = min(threshold, len(ranked_lines))
    for i, line_number in enumerate(ranked_lines[:threshold]):
        if gold_labels[line_number] == 1:
            rr += 1.0 / (i + 1)
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
    Metrics are: Average Precision, R-Pr, Reciprocal Rank@N, Precision@N
    :param gold_fpath: the original annotated gold file, where the last 4th column contains the labels.
    :param pred_fpath: a file with line_number at each line, where the list is ordered by check-worthiness.
    :param thresholds: thresholds used for Reciprocal Rank@N and Precision@N.
    If not specified - 1, 3, 5, 10, 20, 50, len(ranked_lines).
    """
    gold_labels, line_score = _read_gold_and_pred(gold_fpath, pred_fpath)

    ranked_lines = [t[0] for t in sorted(line_score, key=lambda x: x[1], reverse=True)]

    if thresholds is None or len(thresholds) == 0:
        thresholds = [1, 3, 5, 10, 20, 50, len(ranked_lines)]

    # Calculate Metrics
    precisions = _compute_precisions(gold_labels, ranked_lines, len(ranked_lines))
    avg_precisions = [_compute_average_precision(gold_labels, ranked_lines, th) for th in thresholds]
    reciprocal_ranks = [_compute_average_precision(gold_labels, ranked_lines, th) for th in thresholds]
    num_relevant = len({k for k, v in gold_labels.items() if v == 1})

    # Log Results
    threshold_line_format = '{:<25}' + "".join(['@{:<9}'.format(ind) for ind in thresholds])
    lines_separator = '=' * 120

    logging.info('{:=^120}'.format('RESULTS'))
    logging.info('{:<25}'.format('R-PRECISION (R={}):'.format(num_relevant))
                 + '{0:.4f}'.format(precisions[num_relevant - 1]))
    logging.info(lines_separator)

    logging.info(threshold_line_format.format('AVERAGE PRECISION:'))
    logging.info('{:<25}'.format("") + "".join(['{0:<10.4f}'.format(r) for r in avg_precisions]))
    logging.info(lines_separator)

    logging.info(threshold_line_format.format('RECIPROCAL RANK@N:'))
    logging.info('{:<25}'.format("") + "".join(['{0:<10.4f}'.format(r) for r in reciprocal_ranks]))
    logging.info(lines_separator)

    logging.info(threshold_line_format.format('PRECISION@N:'))
    logging.info('{:<25}'.format("") + "".join(['{0:<10.4f}'.format(precisions[r-1]) for r in thresholds]))
    logging.info(lines_separator)

    logging.info('Description of the evaluation metrics: ')
    logging.info('R-Precision is Precision at R, where R is the number of relevant line_numbers for the evaluated set.')
    logging.info('Average Precision@N is precision, estimated at each relevant line_number, averaged for all relevant line_numbers up to the N-th.')
    logging.info('Reciprocal Rank@N is the sum of the reciprocal ranks of the relevant line_numbers (up to the N-th), according to the ranked list.')
    logging.info('Precision@N is precision estimated for the first N line_numbers in the provided ranked list.')
    logging.info(lines_separator)
    logging.info(lines_separator)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold_file_path", help="The absolute path to the file with gold annotations.", type=str)
    parser.add_argument("--pred_file_path", help="The absolute path to the file with ranked line_numbers.", type=str)
    args = parser.parse_args()

    logging.info("Started evaluating results for Subtask A ...")
    check_format(args.pred_file_path)
    evaluate(args.gold_file_path, args.pred_file_path)
