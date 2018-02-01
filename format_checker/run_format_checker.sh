#!/usr/bin/env bash
PROJ_DIR="$(dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))"
format_checker_tests_path=${PROJ_DIR}'/data/format_checker_tests/'

echo '======= Subtask A OK: Running the format checker with correct output.'
python3 subtaskA.py --pred_file_path=${format_checker_tests_path}subtaskA_OK.txt
echo '======='
echo '======= Subtask A NOT OK: Running the format checker with some missing line_numbers.'
python3 subtaskA.py --pred_file_path=${format_checker_tests_path}subtaskA_NOTOK_MISSING_ID.txt
echo '======='
echo '======= Subtask A NOT OK: Running the format checker where the provided list of line_numbers contains duplicates.'
python3 subtaskA.py --pred_file_path=${format_checker_tests_path}'subtaskA_NOTOK_DUP_LINE_NUM.txt'
echo '======='
echo '======= Subtask A NOT OK: Running the format checker where the line_numbers start from 0'
python3 subtaskA.py --pred_file_path=${format_checker_tests_path}'subtaskA_NOTOK_0.txt'
echo '======='
echo '======= Subtask B OK: Running the format checker with correct output.'
python3 subtaskB.py --pred_file_path=${format_checker_tests_path}subtaskB_OK.txt
echo '======='
echo '======= Subtask B NOT OK: Running the format checker where the labels are different from TRUE, FALSE, HALF-TRUE.'
python3 subtaskB.py --pred_file_path=${format_checker_tests_path}subtaskB_NOTOK_OTHER_LABELS.txt
echo '======='
echo '======= Subtask B WARNING: Running the format checker where some claim_numbers are missing from the file.'
python3 subtaskB.py --pred_file_path=${format_checker_tests_path}subtaskB_WARN_MISSING_LABEL.txt
echo '======='
echo '======= Subtask B NOT OK: Running the format checker where the provided predictions contains duplicate claim_numbers with different labels.'
python3 subtaskB.py --pred_file_path=${format_checker_tests_path}subtaskB_NOTOK_DUP_CLAIM_NUM.txt