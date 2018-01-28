import argparse
import re
import logging

"""
This script checks whether the results format for Subtask B is correct. 
It also provides some warnings about possible errors.

The correct format of the Subtask B results file is:
claim_number <TAB> label
where claim_number is only the number of the claims, which are fact-checked (Not N/A).
"""

_LINE_PATTERN_B = re.compile('^[1-9][0-9]{0,3}\t(TRUE|FALSE|HALF-TRUE)$', re.IGNORECASE)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def check_format(file_path):
    with open(file_path, encoding='UTF-8') as out:
        file_content = out.read().strip()

        id_label = []
        for line in file_content.split('\n'):
            if not _LINE_PATTERN_B.match(line.strip()):
                # 1. Check line format
                logging.error("Wrong line format: {}".format(line))
                return False

            _cols = line.split('\t')
            id_label.append((int(_cols[0].strip()), _cols[1].strip()))

        ids = [_id_label[0] for _id_label in id_label]
        labels = [_id_label[1] for _id_label in id_label]

        # 2. Check if some ids are missing
        if sorted(ids) != list(range(min(ids), max(ids) + 1)):
            logging.error("You seem to have missing line_numbers in the provided list.")
            return False

        logging.info("The file looks properly formatted.")

        # 3. Check if some labels are missing
        if len(set(labels)) < 3:
            logging.warning("It seems you have missed a class in the predicted labels.")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="The absolute path to the file you want to check.", type=str)
    args = parser.parse_args()
    logging.info("Subtask B: Checking file: {}".format(args.file_path))
    check_format(args.file_path)