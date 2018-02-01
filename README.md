# clef2018-facts-tools
Contains format checker, scorer and baselines for the [CLEF2018-factcheking task](http://alt.qcri.org/clef2018-factcheck/).

## __Results File Format__: 

### Subtask A: 
For this task, results file is a list of claims with the estimated score for check-worthiness. 
    Each line in the results file is in the format:
>line_number <TAB> score

Where _line_number_ is the number of the claim in the debate and _score_ is a number indicating the priority of the claim for fact-checking. Line numbers are provided in the order they should be prioritized for fact-checking. For example:
>1	0.9056 <br/>
>2	0.6862 <br/>
>3	0.7665 <br/>
>4	0.9046 <br/>
>5	0.2598 <br/>
>6	0.6357 <br/>
>7	0.9049 <br/>
>8	0.8721 <br/>
>9	0.5729 <br/>
>10	0.1693 <br/>
>11	0.4115 <br/>
> ...

### Subtask B

For this subtask, participants should estimate the credibility of the fact-checked claims. The results file is in the format:

> claim_number <TAB> label

Where claim_number is the consecutive number only of the fact-checked claims and the label is one of: TRUE, FALSE, HALF-TRUE. For example:

>1  TRUE <br/>
>2	FALSE <br/>
>3	TRUE <br/>
>4	HALF-TRUE <br/>
>5	HALF-TRUE <br/>
>6	HALF-TRUE <br/>
>7	HALF-TRUE <br/>
>8	HALF-TRUE <br/>
>9	FALSE <br/>
>10	TRUE <br/>
> ... 

## Format checkers

The checkers for each subtask are located in the format_checker module of the project.
Each format checker verifies that your generated results file complies with the expected format.
To launch them run: 
> python3 subtaskA.py --pred_file_path=<path_to_your_results_file> <br/>
> python3 subtaskB.py --pred_file_path=<path_to_your_results_file> 

As result, messages about in-/proper formatting will be displayed.

`run_format_checker.sh` includes examples of the output of the checkers when dealing with an ill-formed results file. You can view the results from running run_format_checker.sh in run_format_checker_out.txt

## Scorers 

Launch the scorers for each task as follows:
> python3 subtaskA.py --gold_file_path=<path_to_gold_file> --pred_file_path=<predicted_results_path> <br/>
> python3 subtaskB.py --gold_file_path=<path_to_gold_file> --pred_file=<predicted_results_path> 
    
where __<path_to_gold_file>__ is the path to the file containing the gold annotations for the debate and __<predicted_results_path>__ is the path to the predicted results, which follows the format, described in 'Results File Format' section.

All of the scorers make calls to the format checkers for the corresponding task

For the Subtask A ranking task, the scorer computes R-Precision, Average Precision, Recipocal Rank@k, Precision@k.

For the Subtask B classification task, the scorer computes Accuracy, Macro F1, Macro Recall, and a confusion matrix.

run_scorer.sh provides more examples of using the scorers and the results can be viewed in the run_scorer_out.txt file.
