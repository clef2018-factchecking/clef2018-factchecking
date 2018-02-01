import argparse
import re
import logging


"""
This script checks whether the results format for Subtask A is correct. 
It also provides some warnings about possible errors.

The correct format of the Subtask A results file is one line_number per line, 
where the list is ordered by the estimated 'check-worthiness'.
"""

_LINE_PATTERN_A = re.compile('^[1-9][0-9]{0,3}$')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def check_format(file_path):
    with open(file_path, encoding='UTF-8') as out:
        file_content = out.read().strip()
        ids = []
        for line in file_content.split('\n'):
            if not _LINE_PATTERN_A.match(line.strip()):
                # 1. Check line format.
                logging.error("Wrong line format: {}".format(line))
                return False

            line_number = int(line.strip())
            if line_number in ids:
                logging.error('Duplicated line_number in ranked line_numbers: {}'.format(line_number))
                quit()

            ids.append(int(line.strip()))

        logging.info("The file looks properly formatted.")

        # 2. Warn if line_numbers are in consecutive order.
        if sorted(ids) == ids:
            logging.warning("Your line_numbers seem not ordered by check-worthiness. They appear in consecutive order.")

        # 3. Check if some ids are missing
        if sorted(ids) != list(range(min(ids), max(ids)+1)):
            logging.warning("You seem to have missing line_numbers in the provided list.")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_file_path", help="The absolute path to the file you want to check.", type=str)
    args = parser.parse_args()
    logging.info("Subtask A: Checking file: {}".format(args.pred_file_path))
    check_format(args.pred_file_path)