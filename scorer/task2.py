import logging
import csv
import argparse
from format_checker.task2 import check_format
"""
Scoring of Task 2 with confusion matrix, Acc, Macro F1 and Average Recall. 
"""

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)

_LABELS = ['true', 'false', 'half-true']
# The "distance" for a false-true mistake is 2, and for every other pair - 1
_LABEL_NUMERIC_VALUES = { 'false': 0, 'half-true': 1, 'true': 2 }


def _read_gold_and_pred(gold_file_path, pred_file_path, claim_number_prefix=''):
    logging.info("Reading gold predictions from file {}".format(gold_file_path))

    gold_labels = {}
    with open(gold_file_path) as gold_file:
        gold_reader = csv.DictReader(gold_file, delimiter='\t', fieldnames=['line_number', 'speaker', 'text', 'claim_number', 'normalized_claim', 'label'])

        for row in gold_reader:
            if row['claim_number'] != 'N/A':
                claim_id = claim_number_prefix + row['claim_number']
                gold_labels[claim_id] = row['label']

    logging.info('Reading predicted classification labels from file {}'\
        .format(pred_file_path))

    predicted_labels = {}
    with open(pred_file_path) as pred_file:
        for i, line in enumerate(pred_file):
            claim_number, label = line.strip().split('\t')
            claim_id = claim_number_prefix + claim_number

            if claim_id not in gold_labels:
                logging.error('No such claim_number: {} in gold file!'.format(claim_number))
                quit()

            predicted_labels[claim_id] = label

    if len(set(gold_labels).difference(predicted_labels)) != 0:
        logging.error('The predictions do not match the claims from the gold file - missing or extra claim_number')
        raise ValueError('The predictions do not match the claims from the gold file - missing or extra claim_number')

    return gold_labels, predicted_labels


def _compute_confusion_matrix(gold_labels, pred_labels):
    """ Computes Confusion Matrix. """
    conf_matrix = {'true' : {'true' : 0, 'false' : 0, 'half-true': 0},
                    'false' : {'true' : 0, 'false' : 0, 'half-true': 0},
                    'half-true': {'true' : 0, 'false' : 0, 'half-true': 0}}

    for claim_number, pred_label in pred_labels.items():
        pred_label = pred_label.lower()
        true_label = gold_labels[claim_number].lower()
        conf_matrix[true_label][pred_label] += 1

    return conf_matrix


def _compute_accuracy(conf_matrix):
    """ Computes Accuracy. """
    num_claims = sum([sum(row.values()) for row in conf_matrix.values()])
    correct_claims = sum([conf_matrix[l][l] for l in _LABELS])
    if num_claims:
        return correct_claims / num_claims
    else:
        return 0.0


def _compute_macro_f1(conf_matrix):
    """ Computes Macro F1. """
    # Calculate standard P, R, F1, Acc
    p = {'true': 0, 'false': 0, 'half-true': 0}
    r = {'true': 0, 'false': 0, 'half-true': 0}

    for label in _LABELS:
        all_predicted = sum([conf_matrix[l][label] for l in _LABELS])

        if all_predicted:
            p[label] = conf_matrix[label][label] / all_predicted
        else:
            p[label] = 0.0
        all_gold = sum([conf_matrix[label][l] for l in _LABELS])

        if all_gold == 0:
            raise ValueError('No instances for class {} found!'.format(label))

        r[label] = conf_matrix[label][label] / all_gold
    
    f1 = {'true': 0, 'false': 0, 'half-true': 0}
    for label in _LABELS:
        if p[label] + r[label]:
            f1[label] = 2.0 * p[label] * r[label] / (p[label] + r[label])
        else:
            f1[label] = 0.0

    return sum(f1.values()) / len(f1)


def _compute_macro_recall(conf_matrix):
    """ Computes Macro Recall """
    r = {}
    for label in _LABELS:
        all_gold = sum([conf_matrix[label][l] for l in _LABELS])
        if all_gold == 0:
            raise ValueError('No instances for class {} found!'.format(label))

        r[label] = conf_matrix[label][label] / all_gold
    
    return sum(r.values()) / len(r)


def _compute_mean_absolute_error(conf_matrix):
    """ Computes Mean Absolute Error (MAE). """
    num_claims = sum([sum(row.values()) for row in conf_matrix.values()])
    distance_sum = 0.0
    for gold_label in conf_matrix:
        for pred_label in conf_matrix:
            distance = abs(_LABEL_NUMERIC_VALUES[gold_label] - _LABEL_NUMERIC_VALUES[pred_label])
            distance_sum += conf_matrix[gold_label][pred_label] * distance
    if num_claims:
        return distance_sum / num_claims
    else:
        return 0.0


def _compute_macro_averaged_mae(conf_matrix):
    """ Computes Macro-averaged Mean Absolute Error. """
    mae = {}
    for label in _LABELS:
        all_gold = sum([conf_matrix[label][l] for l in _LABELS])
        distance_sum = 0.0
        gold_label_value = _LABEL_NUMERIC_VALUES[label]
        for pred_label in conf_matrix[label]:
            distance = abs(gold_label_value - _LABEL_NUMERIC_VALUES[pred_label])
            distance_sum += conf_matrix[label][pred_label] * distance
        if all_gold == 0:
            raise ValueError('No instances for class {} found!'.format(label))
        mae[label] = distance_sum / all_gold
    return sum(mae.values()) / len(mae)


def evaluate(gold_labels, pred_labels):
    """
    Evaluates the predicted labels for claim_numbers w.r.t. a gold file.
    Metrics are: confusion matrix, Acc, Macro F1, Average Recall, MAE, Macro MAE
    :param gold_labels: a dictionary with gold label for each claim_id
    :param pred_labels: a dictionary with predicted label for each claim_id
    """

    # Calculate Metrics
    conf_matrix = _compute_confusion_matrix(gold_labels, pred_labels)
    mae = _compute_mean_absolute_error(conf_matrix)
    macro_mae = _compute_macro_averaged_mae(conf_matrix)
    accuracy = _compute_accuracy(conf_matrix)
    macro_f1 = _compute_macro_f1(conf_matrix)
    macro_recall = _compute_macro_recall(conf_matrix)
    
    # Log Results
    lines_separator = '=' * 120
    higher_better = '     (higher is better)'
    lower_better = '     (lower is better)'
    logging.info('{:=^120}'.format(' RESULTS '))

    logging.info('{:<30}'.format('MEAN ABSOLUTE ERROR (MAE):') + '{0:.4f}'.format(mae) + lower_better)
    logging.info(lines_separator)

    logging.info('{:<30}'.format('MACRO-AVERAGE MAE:') + '{0:.4f}'.format(macro_mae) + lower_better)
    logging.info(lines_separator)

    logging.info('{:<30}'.format('ACCURACY:') + '{0:.4f}'.format(accuracy) + higher_better)
    logging.info(lines_separator)

    logging.info('{:<30}'.format('MACRO-AVERAGE F1:') + '{0:.4f}'.format(macro_f1) + higher_better)
    logging.info(lines_separator)

    logging.info('{:<30}'.format('MACRO-AVERAGE RECALL:') + '{0:.4f}'.format(macro_recall) + higher_better)
    logging.info(lines_separator)

    logging.info('{:<30}'.format('CONFUSION MATRIX:'))
    logging.info(' '*10 + ''.join(['{:>15}'.format(l) for l in _LABELS]))
    for true_label in _LABELS:
        predicted_labels = conf_matrix[true_label]
        logging.info('{:<10}'.format(true_label) + ''.join(['{:>15}'.format(predicted_labels[l]) for l in _LABELS]))
    logging.info(lines_separator)

    logging.info('Description of the evaluation metrics: ')
    logging.info('!!! THE OFFICIAL METRIC USED FOR THE COMPETITION RANKING IS MEAN ABSOLUTE ERROR !!!')
    logging.info('Mean Absolute Error (MAE) computes the mean "distance" between the predicted and gold labels.')
    logging.info('  For correct predictions the distance is 0.')
    logging.info('  For mistakes between FALSE and TRUE classes it is 2, and for all other mistakes it is 1.')
    logging.info('Macro-average MAE computes MAE for each of the (gold) classes and takes the average.')
    logging.info('Accuracy computes the percentage of correctly predicted classes.')
    logging.info('Macro-average F1 computes the F1 score for each of the classes and takes their average.')
    logging.info('Macro-average Recall computes Recall for each of the classes and takes its average.')
    logging.info('Confusion Matrix computes the distribution of predicted classes, where rows are true labels and columns are predicted ones.')
    logging.info(lines_separator)
    logging.info(lines_separator)


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
        help="Single string containing a comma separated list of paths to files with classified claims.",
        type=str,
        required=True
    )
    args = parser.parse_args()

    pred_files = [pred_file.strip() for pred_file in args.pred_file_path.split(",")]
    gold_files = [gold_file.strip() for gold_file in args.gold_file_path.split(",")]

    if validate_files(pred_files, gold_files):
        logging.info("Started evaluating results for Task 2 ...")
        all_gold_labels = {}
        all_pred_labels = {}
        for idx, (pred_file, gold_file) in enumerate(zip(pred_files, gold_files)):
            gold_labels, pred_labels = _read_gold_and_pred(gold_file, pred_file, 'file-{}-claim-number-'.format(idx))
            all_gold_labels.update(gold_labels)
            all_pred_labels.update(pred_labels)

        evaluate(all_gold_labels, all_pred_labels)
