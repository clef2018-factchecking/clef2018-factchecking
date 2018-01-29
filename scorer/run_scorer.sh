#!/usr/bin/env bash
python3 subtaskA.py --gold_file_path='examples/Task1-English-1st-Presidential.txt' --pred_file_path='examples/subtaskA_random_baseline.txt'
python3 subtaskA.py --gold_file_path='examples/Task1-English-1st-Presidential.txt' --pred_file_path='examples/subtaskA_gold.txt'

python3 subtaskB.py --gold_file_path='examples/Task2-English-1st-Presidential.txt' --pred_file='examples/subtaskB_gold.txt'
python3 subtaskB.py --gold_file_path='examples/Task2-English-1st-Presidential.txt' --pred_file='examples/subtaskB_random_baseline.txt'