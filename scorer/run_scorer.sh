#!/usr/bin/env bash
PROJ_DIR="$(dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))"
export PYTHONPATH=${PROJ_DIR}
scorer_tests_path=${PROJ_DIR}'/scorer/data/'
gold_file_task1=${PROJ_DIR}/data/task1/English/'Task1-English-1st-Presidential.txt'
gold_file_task2=${PROJ_DIR}/data/task2/English/'Task2-English-1st-Presidential.txt'

echo 'Scoring a random baseline for task 1'
python3 task1.py --gold_file_path=${gold_file_task1} --pred_file_path=${scorer_tests_path}task1_random_baseline.txt
echo '**********'
echo 'Scoring the gold predictions for task 1'
python3 task1.py --gold_file_path=${gold_file_task1} --pred_file_path=${scorer_tests_path}task1_gold.txt
echo '**********'
echo 'Scoring BOTH the gold and random baseline for task 1 (only for example purposes, scoring multiple files for 1 debate will lead to wrong metrics)'
python3 task1.py --gold_file_path="${gold_file_task1}, ${gold_file_task1}" --pred_file_path="${scorer_tests_path}task1_gold.txt, ${scorer_tests_path}task1_random_baseline.txt"
echo '**********'
echo 'TEST ERROR: Scoring task 1, where the provided list of line_numbers contains a line_number, which is not in the gold file.'
python3 task1.py --gold_file_path=${gold_file_task1} --pred_file_path=${scorer_tests_path}task1_other_line_number.txt
echo '**********'
echo 'TEST ERROR: Scoring task 1, where the provided list of line_numbers does not contain all lines from the gold file.'
python3 task1.py --gold_file_path=${gold_file_task1} --pred_file_path=${scorer_tests_path}task1_not_all_lines.txt
echo '**********'
echo '**********'
echo 'Scoring the gold predictions for task 2'
python3 task2.py --gold_file_path=${gold_file_task2} --pred_file_path=${scorer_tests_path}task2_gold.txt
echo '**********'
echo 'Scoring a random baseline for task 2'
python3 task2.py --gold_file_path=${gold_file_task2} --pred_file_path=${scorer_tests_path}task2_random_baseline.txt
echo '**********'
echo 'Scoring BOTH the gold and random baseline for task 2 (only for example purposes, scoring multiple files for 1 debate will lead to wrong metrics)'
python3 task2.py --gold_file_path="${gold_file_task2}, ${gold_file_task2}" --pred_file_path="${scorer_tests_path}task2_gold.txt, ${scorer_tests_path}task2_random_baseline.txt"
echo '**********'
echo 'TEST ERROR: Scoring task 2, with predictions that contains a claim_number, which is not present in the gold file.'
python3 task2.py --gold_file_path=${gold_file_task2} --pred_file_path=${scorer_tests_path}task2_other_claim_number.txt
echo '**********'
echo 'TEST ERROR: Scoring task 2, with predictions that do not contain all claims from the gold file.'
python3 task2.py --gold_file_path=${gold_file_task2} --pred_file_path=${scorer_tests_path}task2_not_all_claims.txt
