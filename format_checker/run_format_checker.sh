#!/usr/bin/env bash
PROJ_DIR="$(dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))"
format_checker_tests_path=${PROJ_DIR}'/format_checker/data/'

echo '======= Task 1 OK: Running the format checker with correct output.'
python3 task1.py --pred_file_path=${format_checker_tests_path}task1_OK.txt
echo '======='
echo '======= Task 1 NOT OK: Running the format checker with some missing line_numbers.'
python3 task1.py --pred_file_path=${format_checker_tests_path}task1_NOTOK_MISSING_ID.txt
echo '======='
echo '======= Task 1 NOT OK: Running the format checker where the provided list of line_numbers contains duplicates.'
python3 task1.py --pred_file_path=${format_checker_tests_path}'task1_NOTOK_DUP_LINE_NUM.txt'
echo '======='
echo '======= Task 1 NOT OK: Running the format checker where the line_numbers start from 0'
python3 task1.py --pred_file_path=${format_checker_tests_path}'task1_NOTOK_0.txt'
echo '======='
echo '======= Task 2 OK: Running the format checker with correct output.'
python3 task2.py --pred_file_path=${format_checker_tests_path}task2_OK.txt
echo '======='
echo '======= Task 2 NOT OK: Running the format checker where the labels are different from TRUE, FALSE, HALF-TRUE.'
python3 task2.py --pred_file_path=${format_checker_tests_path}task2_NOTOK_OTHER_LABELS.txt
echo '======='
echo '======= Task 2 WARNING: Running the format checker where some claim_numbers are missing from the file.'
python3 task2.py --pred_file_path=${format_checker_tests_path}task2_WARN_MISSING_LABEL.txt
echo '======='
echo '======= Task 2 NOT OK: Running the format checker where the provided predictions contains duplicate claim_numbers with different labels.'
python3 task2.py --pred_file_path=${format_checker_tests_path}task2_NOTOK_DUP_CLAIM_NUM.txt