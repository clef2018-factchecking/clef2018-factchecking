#!/usr/bin/env bash
PROJ_DIR="$(dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))"
format_checker_tests_path=${PROJ_DIR}'/data/format_checker_tests/'

echo '======= This is an example of running the format checker with correct output for Subtask A.'
python3 subtaskA.py --pred_file_path=${format_checker_tests_path}subtaskA_OK.txt
echo '======='
echo '======= This is an example of running the format checker for subtask A, with some missing/skipper line_numbers.'
python3 subtaskA.py --pred_file_path=${format_checker_tests_path}subtaskA_WARN_MISSING_ID.txt
echo '======='
echo '======= This is an exmaple of running the format checker for subtask A, where line_numbers are separated with commas, not with new lines.'
python3 subtaskA.py --pred_file_path=${format_checker_tests_path}subtaskA_NOTOK_SEP.txt
echo '======='
echo '======= This is an example of running the format checker for subtask A, where the provided list of line_numbers contains duplicates.'
python3 subtaskA.py --pred_file_path=${format_checker_tests_path}'subtaskA_dup_line_number.txt'
echo '======='
echo '======= This is an example of running the format checker with correct output for Subtask B.'
python3 subtaskB.py --pred_file_path=${format_checker_tests_path}subtaskB_OK.txt
echo '======='
echo '======= This is an example of running the format checker on file with predicted labels, where the labels are different from TRUE, FALSE, HALF-TRUE.'
python3 subtaskB.py --pred_file_path=${format_checker_tests_path}subtaskB_NOTOK_OTHER_LABELS.txt
echo '======='
echo '======= This is an example of running the format checker on file with predicted labels, where some claim_numbers are missing from the file.'
python3 subtaskB.py --pred_file_path=${format_checker_tests_path}subtaskB_WARN_MISSING_LABEL.txt
echo '======='
echo '======= This is an example of running the format checker for subtask A, where the provided predictions contains duplicate claim_numners with different labels.'
python3 subtaskB.py --pred_file_path=${format_checker_tests_path}subtaskB_dup_claim_number.txt