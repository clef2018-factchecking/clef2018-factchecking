import logging
import csv
import argparse

"""
Scoring of Subtask B with confusion matrix, Acc, Macro F1 and Average Recall. 
"""

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

_LABELS = ['true', 'false', 'half-true']


def _read_gold_and_pred(gold_file_path, pred_file_path):
    logging.info("Reading gold predictions from file {}".format(gold_file_path))

    gold_labels = {}
    with open(gold_file_path) as gold_file:
        gold_reader = csv.DictReader(gold_file, delimiter='\t', fieldnames=['line_number', 'speaker', 'text', 'claim_number', 'normalized_claim', 'label'])

        for row in gold_reader:
            if row['claim_number'] != 'N/A':
                gold_labels[int(row['claim_number'])] = row['label']

    logging.info('Reading predicted classification labels from file {}'\
        .format(pred_file_path))

    predicted_labels = {}
    for i, line in enumerate(open(pred_file_path)):
        claim_number, label = line.strip().split('\t')
        claim_number = int(claim_number)

        if int(claim_number) not in gold_labels:
            logging.error('No such claim_number: {} in gold file!'.format(claim_number))
            quit()

        predicted_labels[claim_number] = label

    if len(gold_labels) != len(predicted_labels):
        logging.warning('You have missed some line_numbers in your prediction file.')

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
    """ Computer Accuracy. """
    num_claims = sum([sum(row.values()) for row in conf_matrix.values()])
    correct_claims = sum([conf_matrix[l][l] for l in _LABELS])
    return correct_claims / num_claims


def _compute_macro_f1(conf_matrix):
    """ Computes Macro F1. """
    # Calculate standard P, R, F1, Acc
    p = {'true': 0, 'false': 0, 'half-true': 0}
    r = {'true': 0, 'false': 0, 'half-true': 0}

    for label in _LABELS:
        p[label] = conf_matrix[label][label] / sum([conf_matrix[l][label] for l in _LABELS])
        r[label] = conf_matrix[label][label] / sum([conf_matrix[label][l] for l in _LABELS])
    
    f1 = {'true': 0, 'false': 0, 'half-true': 0}
    for label in _LABELS:
        f1[label] = 2.0 * p[label] * r[label] / (p[label] + r[label])

    return sum(f1.values()) / len(f1)


def _compute_macro_recall(conf_matrix):
    """ Computes Macro Recall """
    r = {'true': 0, 'false': 0, 'half-true': 0}

    for label in _LABELS:
        r[label] = conf_matrix[label][label] / sum([conf_matrix[label][l] for l in _LABELS])
    
    return sum(r.values()) / len(r)


def evaluate(gold_fpath, pred_fpath):
    """
    Evaluates the predicted labels for claim_numbers w.r.t. a gold file.
    Metrics are: confusion matrix, Acc, Macro F1 and Average Recall
    :param gold_fpath: the original annotated gold file.
    :param pred_fpath: a file with 'claim_number <TAB> label' at each line.
    """
    gold_labels, pred_labels = _read_gold_and_pred(gold_fpath, pred_fpath)
   
    # Calculate Metrics
    conf_matrix = _compute_confusion_matrix(gold_labels, pred_labels)
    accuracy = _compute_accuracy(conf_matrix)
    macro_f1 = _compute_macro_f1(conf_matrix)
    macro_recall = _compute_macro_recall(conf_matrix)
    
    # Log Results
    lines_separator = '=' * 120
    logging.info('{:=^120}'.format('RESULTS'))

    logging.info('{:<25}'.format('ACC:') + '{0:.4f}'.format(accuracy))
    logging.info(lines_separator)

    logging.info('{:<25}'.format('MACRO F1:') + '{0:.4f}'.format(macro_f1))
    logging.info(lines_separator)

    logging.info('{:<25}'.format('MACRO RECALL:') + '{0:.4f}'.format(macro_recall))
    logging.info(lines_separator)

    logging.info('{:<25}'.format('CONFUSION MATRIX:'))
    logging.info(' '*10 + ''.join(['{:>15}'.format(l) for l in _LABELS]))
    for true_label in _LABELS:
        predicted_labels = conf_matrix[true_label]
        logging.info('{:<10}'.format(true_label) + ''.join(['{:>15}'.format(predicted_labels[l]) for l in _LABELS]))
    logging.info(lines_separator)

    logging.info('Description of the evaluation metrics: ')
    logging.info('Accuracy computes the percentage of correctly predicted classes.')
    logging.info('Macro F1 computes the F1 score for each of the classes and takes their average.')
    logging.info('Macro Recall computes Recall for each of the classes and takes its average.')
    logging.info('Confusion Matrix computes the distribution of predicted classes, where rows are true labels and columns are predicted ones.')
    logging.info(lines_separator)
    logging.info(lines_separator)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold_file_path", help="The absolute path to the file with gold annotations.", type=str)
    parser.add_argument("--pred_file_path", help="The absolute path to the file with ranked line_numbers.", type=str)
    args = parser.parse_args()

    logging.info("Started evaluating results for Subtask B ...")
    evaluate(args.gold_file_path, args.pred_file_path)