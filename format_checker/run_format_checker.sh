#!/usr/bin/env bash
python3 subtaskA.py --file_path=examples/subtaskA_OK.txt
echo '======='
python3 subtaskA.py --file_path=examples/subtaskA_WARN_MISSING_ID.txt
echo '======='
python3 subtaskA.py --file_path=examples/subtaskA_NOTOK_SEP.txt
echo '======='
python3 subtaskB.py --file_path=examples/subtaskB_OK.txt
echo '======='
python3 subtaskB.py --file_path=examples/subtaskB_NOTOK_OTHER_LABELS.txt
echo '======='
python3 subtaskB.py --file_path=examples/subtaskB_WARN_MISSING_LABEL.txt