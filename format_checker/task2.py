import argparse
import re
import logging

"""
This script checks whether the results format for Task 2 is correct. 
It also provides some warnings about possible errors.

The correct format of the Task 2 results file is:
claim_number <TAB> label
where claim_number is only the number of the claims, which are fact-checked (Not N/A).
"""

_LINE_PATTERN_B = re.compile('^[1-9][0-9]{0,3}\t(TRUE|FALSE|HALF-TRUE)$', re.IGNORECASE)
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)


def check_format(file_path):
    with open(file_path, encoding='UTF-8') as out:
        file_content = out.read().strip()

        id_label = {}
        for line in file_content.split('\n'):
            if not _LINE_PATTERN_B.match(line.strip()):
                # 1. Check line format
                logging.error("Wrong line format: {}".format(line))
                return False

            _cols = line.split('\t')
            claim_number = int(_cols[0].strip())
            label = _cols[1].strip()

            if claim_number in id_label and id_label[claim_number] != label:
                logging.error(
                    'There is an already predicted label for claim_number {} and it is different!'.format(claim_number))
                return False

            id_label[claim_number] = label

        ids = list(id_label.keys())
        labels = list(id_label.values())

        # 2. Check if some ids are missing
        if sorted(ids) != list(range(1, max(ids) + 1)):
            logging.error("You seem to have missing claim_numbers in the provided list.")
            return False

        # 3. Check if some labels are missing
        if len(set(labels)) < 3:
            logging.warning("It seems you have missed a class in the predicted labels.")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_file_path", help="The absolute path to the file you want to check.", type=str)
    args = parser.parse_args()
    logging.info("Task 2: Checking file: {}".format(args.pred_file_path))
    check_format(args.pred_file_path)
