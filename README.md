# clef2018-facts-tools
Contains format checker, scorer and baselines for the [CLEF2018-factcheking task](http://alt.qcri.org/clef2018-factcheck/).

## __Results File Format__: 

### Subtask A: 
For this task, results file is a list of ranked claims, ordered according to their estimated check-worthiness. 
    Each line in the results file is in the format:
>line_number

Where _line_number_ is the number of the claim in the debate. Line numbers are provided in the order they should be prioritized for fact-checking. For example:
>1328 <br/>
>1225 <br/>
>1222 <br/>
>1103 <br/>
>1098 <br/>
>1086 <br/>
>1062 <br/>
>1061 <br/>
>1060 <br/>
>1002 <br/>
> ...

Where 1328 is the line_number of the claim, which should be checked first, 1225 is the line_number of the claim that should be checked secont, etc.

### Subtask B

For this subtask, participants should estimate the credibility of the fact-checked claims. The results file is in the format:

> claim_number <TAB> label

Where claim_number is the consequtive number only of the fact-checked claims and the label is one of: TRUE, FALSE, HALF-TRUE. For example:

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
