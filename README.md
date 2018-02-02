# CLEF2018-factchecking
This repository contains the _dataset_ for the [CLEF2018-factcheking task](http://alt.qcri.org/clef2018-factcheck/).

It also contains the _format checker, scorer and baselines_ for the task.

================================================================ <br>
FCPD corpus for the CLEF-2018 LAB on "Automatic Identification 
and Verification of Claims in Political Debates"
Version 1.0: February 25, 2018 (TRIAL) <br>
================================================================

This file contains the basic information regarding the CLEF2018-factcheck
on Fact Checking Political Debates dataset provided for the CLEF-2018 Lab
on "Automatic Identification and Verification of Claims in Political Debates".
The current TRIAL version (1.0, January 25, 2018) corresponds to the 
release of a part of the training data set.
The full training sets and the test sets will be provided in future versions.
All changes and updates on these data sets are reported in Section 1 of this document.


## LIST OF VERSIONS

* __v1.0 [2018/01/25]__ -  TRIAL data. Partial distribution of the training data for task 1 and 2, in English and Arabic: It contains examples extracted from two US Presidential and one Vice-Presidential debate in 2016. 


## CONTENTS OF THE DISTRIBUTION v1.0

We provide the following files:

- Main folder: [GOLD_DATA](GOLD_DATA)

  * [README.txt](README.md) <br/>
    this file

  - Subfolder [/task1/English/](GOLD_DATA/task1/English) <br/>
    [Task1-English-1st-Presidential.txt](GOLD_DATA/task1/English/Task1-English-1st-Presidential.txt) <br/>
    [Task1-English-2nd-Presidential.txt](GOLD_DATA/task1/English/Task1-English-2nd-Presidential.txt) <br/>
    [Task1-English-Vice-Presidential.txt](GOLD_DATA/task1/English/Task1-English-Vice-Presidential.txt) <br/>

  - Subfolder [/task1/Arabic/](GOLD_DATA/task1/Arabic) <br/>
    same content as the previous folder but with the Arabic datasets

    [Task1-Arabic-1st-Presidential.txt](GOLD_DATA/task1/Arabic/Task1-Arabic-1st-Presidential.txt) <br/>
    [Task1-Arabic-2nd-Presidential.txt](GOLD_DATA/task1/Arabic/Task1-Arabic-2nd-Presidential.txt) <br/>
    [Task1-Arabic-Vice-Presidential.txt](GOLD_DATA/task1/Arabic/Task1-Arabic-Vice-Presidential.txt) <br/>

  - Subfolder [/task2/English/](/GOLD_DATA/task2/English) <br/>
    [Task2-English-1st-Presidential.txt](GOLD_DATA/task2/English/Task2-English-1st-Presidential.txt) <br/>
    [Task2-English-2nd-Presidential.txt](GOLD_DATA/task2/English/Task2-English-2nd-Presidential.txt) <br/>
    [Task2-English-Vice-Presidential.txt](GOLD_DATA/task2/English/Task2-English-Vice-Presidential.txt) <br/>

  - Subfolder [/task2/Arabic/](/GOLD_DATA/task2/Arabic) <br/>
    same content as the previous folder but with the Arabic datasets

    [Task2-Arabic-1st-Presidential.txt](/GOLD_DATA/task2/Arabic/Task2-Arabic-1st-Presidential.txt) <br/>
    [Task2-Arabic-2nd-Presidential.txt](/GOLD_DATA/task2/Arabic/Task2-Arabic-2nd-Presidential.txt) <br/>
    [Task2-Arabic-Vice-Presidential.txt](/GOLD_DATA/task2/Arabic/Task2-Arabic-Vice-Presidential.txt) <br/>

## SUBTASKS

For ease of explanation, here we list the tasks:

* __Task 1__: __Check-Worthiness__. Predict which claim in a political debate should be prioritized for fact-checking. In particular, given a debate, the goal is to produce a ranked list of its sentences based on their worthiness for fact checking.

* __Task 2__: __Factuality__. Checking the factuality of the identified worth-checking claims. In particular, given a sentence that is worth checking, the goal is for the system to determine whether the claim is likely to be true or false, or that it is unsure of its factuality.

## DATA FORMAT

The datasets are text files with the information TAB separated. The text encoding is UTF-8.

### For task 1:

> line_number <TAB> speaker <TAB> text <TAB> label

Where: <br>
* line_no: the line number (starting from 1) <br/>
* speaker: the person speaking (a candidate, the moderator, or "SYSTEM"; the latter is used for the audience reaction) <br/>
* text: a sentence that the speaker said <br/>
* label: 1 if this sentence is to be fact-checked, and 0 otherwise 


Example:

>  ... <br/>
>  65  TRUMP So we're losing our good jobs, so many of them. 0 <br/>
>  66  TRUMP When you look at what's happening in Mexico, a friend of mine who builds plants said it's the eighth wonder of the world. 0 <br/>
>  67  TRUMP They're building some of the biggest plants anywhere in the world, some of the most sophisticated, some of the best plants. 0 <br/>
>  68  TRUMP With the United States, as he said, not so much.  0 <br/>
>  69  TRUMP So Ford is leaving. 1 <br/> 
>  70  TRUMP You see that, their small car division leaving. 1 <br/>
>  71  TRUMP Thousands of jobs leaving Michigan, leaving Ohio. 1 <br/>
>  72  TRUMP They're all leaving.  0 <br/>
>  ...


### For task 2:

>  line_number <TAB> speaker <TAB> text <TAB> claim_number <TAB> normalized_claim <TAB> label

Where: <br/>
*  line_no: the line number (starting from 1) <br/>
*  speaker: the person speaking (a candidate, the moderator, or "SYSTEM"; the latter is used for the audience reaction) <br/>
*  text: a sentence that the speaker said <br/>
*  claim_number: claim number if this claim is to be fact-checked, and 0 otherwise <br/>
*  normalized_claim: normalized form of the claim, i.e., this is what is to be checked, or "-" otherwise. <br/>
*  label: TRUE, HALF-TRUE or FALSE (in case the claim is to be checked), or "-" otherwise <br/>


_NOTE 1_: If the line does NOT contain an interesting claim, then claim_number=='N/A' and normalized_claim, label are missing.

_NOTE 2_: The same normalized claim (with the same claim number) can be associated with more than one sentence.


Example:

>  ... <br/>
  65  TRUMP So we're losing our good jobs, so many of them. N/A <br/>
  66  TRUMP When you look at what's happening in Mexico, a friend of mine who builds plants said it's the eighth wonder of the world. N/A <br/>
  67  TRUMP They're building some of the biggest plants anywhere in the world, some of the most sophisticated, some of the best plants. N/A <br/>
  68  TRUMP With the United States, as he said, not so much.  N/A <br/>
  69  TRUMP So Ford is leaving. 1 Ford Motor Company is moving their small car division out of the USA. TRUE <br/>
  70  TRUMP You see that, their small car division leaving. 1 Ford Motor Company is moving their small car division out of the USA. TRUE <br/>
  71  TRUMP Thousands of jobs leaving Michigan, leaving Ohio. 2 Thousands of jobs are being lost in Michigan and Ohio due to Ford Motor Company moving their small car division out of the USA. FALSE <br/>
  ...

## __Results File Format__: 

### Task 1: 
For this task, the expected results file is a list of claims with the estimated score for check-worthiness. 
    Each line contains a tab-separated line with:
>line_number <TAB> score

Where _line_number_ is the number of the claim in the debate and _score_ is a number indicating the priority of the claim for fact-checking. For example:
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

### Task 2:

For this subtask, participants should estimate the credibility of the fact-checked claims. The results file contains one tab-separeted line per instance with:

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

The checkers for each subtask are located in the [format_checker](format_checker) module of the project.
Each format checker verifies that your generated results file complies with the expected format.
To launch them run: 
> python3 subtaskA.py --pred_file_path=<path_to_your_results_file> <br/>
> python3 subtaskB.py --pred_file_path=<path_to_your_results_file> 

`run_format_checker.sh` includes examples of the output of the checkers when dealing with an ill-formed results file. 
Its output can be seen in [run_format_checker_out.txt](format_checker/run_format_checker_out.txt)

## Scorers 

Launch the scorers for each task as follows:
> python3 subtaskA.py --gold_file_path=<path_to_gold_file> --pred_file_path=<predicted_results_path> <br/>
> python3 subtaskB.py --gold_file_path=<path_to_gold_file> --pred_file=<predicted_results_path> 
    
where __<path_to_gold_file>__ is the path to the file containing the gold annotations for a debate and __<predicted_results_path>__ is the path to the predicted results, which follows the format, described in the 'Results File Format' section.

The scorers call the format checkers for the corresponding task to verify the output is properly shaped.

`run_scorer.sh` provides examples on using the scorers and the results can be viewed in the [run_scorer_out.txt](scorer/run_scorer_out.txt) file.

### Evaluation metrics

For Task 1 (ranking): R-Precision, Average Precision, Recipocal Rank@k, Precision@k.

For Task 2 (classification): Accuracy, Macro F1, Macro Recall (+ confusion matrix).


## Baselines

The [baselines](/baselines) module contains a random and a simple ngram baseline for each of the tasks.

If you execute any of the scripts, both of the baselines will be trained on the 1st Presidential and the Vice-Presidential debates and evaluated on the 2nd Presidential debate.
The performance of both baselines will be displayed.

## NOTES:

* This distribution is directly downloadable from the official CLEF-2018 Fact Checking Lab repository:
  https://github.com/clef2018-factchecking/clef2018-factchecking
 

## LICENSING

  These datasets are free for general research use.


## CITATION

Whenever using this resource you should use the CLEF-2018 paper by the organizers describing the Fact Checking Lab. For the moment, the paper is not available. We will update the BIB entry below in subsequent versions of this document.

```bib
@InProceedings{,
    author    = {Nakov, Preslav  and  M\`{a}rquez, Llu\'{i}s and  Barr\'{o}n-Cede\~no, Alberto and Zaghouani, Wajdi and Elsayed, Tamer and Suwaileh, Reem and Gencheva, Pepa},  <br/>
    title     = {{CLEF}-2018 Lab on Automatic Identification and Verification of Claims in Political Debates}, <br>
    booktitle = {Proceedings of the CLEF-2018}, <br/>
    year      = {2018}, <br/>
}
```

## CREDITS

Lab Organizers:

* Preslav Nakov, Qatar Computing Research Institute, HBKU <br/>
* Lluís Màrquez, Amazon <br/>
* Alberto Barrón-Cedeño, Qatar Computing Research Institute, HBKU <br/>
* Wajdi Zaghouani, Carnegie Mellon University - Qatar <br/>
* Tamer Elsayed, Qatar University <br/>
* Reem Suwaileh, Qatar University <br/>
* Pepa Gencheva, Sofia University


Task website: http://alt.qcri.org/clef2018-factcheck/

Contact:   clef-factcheck@googlegroups.com

