================================================================
FCPD corpus for the CLEF-2018 LAB on "Automatic Identification 
and Verification of Claims in Political Debates"
Version 1.0: January 25, 2018 (TRIAL)
================================================================

This file contains the basic information regarding the CLEF2018-factcheck
on Fact Checking Political Debates dataset provided for the CLEF-2018 Lab
on "Automatic Identification and Verification of Claims in Political Debates".
The current TRIAL version (1.0, January 25, 2018) corresponds to the 
release of a part of the training data set.
The full training sets and the test sets will be provided in future versions.
All changes and updates on these data sets are reported in Section 1 of this document.


[1] LIST OF VERSIONS

  v1.0 [2018/01/25]: TRIAL data. Partial distribution of the training data for task 1 and 2, 
                     in English and Arabic: It contains examples extracted from two US Presidential 
                     and one Vice-Presidential debate in 2016.


[2] CONTENTS OF THE DISTRIBUTION v1.0

We provide the following files:

- Main folder

  * README.txt 
    this file

  * CLEF2018-factcheck-v1.0.xlsx
    spreadsheet containing the three debates (in English) with all the annotations for tasks 1 and 2,
    and including some extra information (see the description of the files below). 

  - Subfolder /task1/English/
    Task1-English-1st-Presidential.txt
    Task1-English-2nd-Presidential.txt
    Task1-English-Vice-Presidential.txt

  - Subfolder /task1/Arabic/
    same content as the previous folder but with the Arabic datasets

    Task1-Arabic-1st-Presidential.txt
    Task1-Arabic-2nd-Presidential.txt
    Task1-Arabic-Vice-Presidential.txt

  - Subfolder /task2/English/
    Task2-English-1st-Presidential.txt
    Task2-English-2nd-Presidential.txt
    Task2-English-Vice-Presidential.txt

  - Subfolder /task2/Arabic/
    same content as the previous folder but with the Arabic datasets

    Task2-Arabic-1st-Presidential.txt
    Task2-Arabic-2nd-Presidential.txt
    Task2-Arabic-Vice-Presidential.txt


NOTES:

  This distribution is directly downloadable from the official CLEF-2018 Fact Checking Lab website:
  http://alt.qcri.org/clef2018-factcheck/index.php?id=data-and-tools


[3] LICENSING

  These datasets are free for general research use.


[4] CITATION

Whenever using this resource you should use the CLEF-2018 paper by the organizers describing the Fact Checking Lab. For the moment, the paper is not available. We will update the BIB entry below in subsequent versions of this document.

@InProceedings{,
  author    = {Nakov, Preslav  and  M\`{a}rquez, Llu\'{i}s and  Barr\'{o}n-Cede\~no, Alberto and Zaghouani, Wajdi and Elsayed, Tamer and Suwaileh, Reem and Gencheva, Pepa}, 
  title     = {{CLEF}-2018 Lab on Automatic Identification and Verification of Claims in Political Debates},
  booktitle = {Proceedings of the CLEF-2018},
  year      = {2018},
}


[5] SUBTASKS

For ease of explanation, here we list the tasks:

* Task 1: Check-Worthiness. Predict which claim in a political debate should be prioritized for fact-checking. In particular, given a debate, the goal is to produce a ranked list of its sentences based on their worthiness for fact checking.

* Task 2: Factuality. Checking the factuality of the identified worth-checking claims. In particular, given a sentence that is worth checking, the goal is for the system to determine whether the claim is likely to be true or false, or that it is unsure of its factuality.


[6] DATA FORMAT

The datasets are text files with the information TAB separated. The text encoding is UTF-8.

* For task 1, the format is as follows:

  line_number <TAB> speaker <TAB> text <TAB> label

Where
  line_no: the line number (starting from 1)
  speaker: the person speaking (a candidate, the moderator, or "SYSTEM"; the latter is used for the audience reaction)
  text: a sentence that the speaker said
  label: 1 if this sentence is to be fact-checked, and 0 otherwise


Example:

  ...
  65  TRUMP So we're losing our good jobs, so many of them. 0
  66  TRUMP When you look at what's happening in Mexico, a friend of mine who builds plants said it's the eighth wonder of the world. 0
  67  TRUMP They're building some of the biggest plants anywhere in the world, some of the most sophisticated, some of the best plants. 0
  68  TRUMP With the United States, as he said, not so much.  0
  69  TRUMP So Ford is leaving. 1
  70  TRUMP You see that, their small car division leaving. 1
  71  TRUMP Thousands of jobs leaving Michigan, leaving Ohio. 1
  72  TRUMP They're all leaving.  0
  ...


* For task 2, the format is as follows:

  line_number <TAB> speaker <TAB> text <TAB> claim_number <TAB> normalized_claim <TAB> label

Where
  line_no: the line number (starting from 1)
  speaker: the person speaking (a candidate, the moderator, or "SYSTEM"; the latter is used for the audience reaction)
  text: a sentence that the speaker said
  claim_number: claim number if this claim is to be fact-checked, and 0 otherwise
  normalized_claim: normalized form of the claim, i.e., this is what is to be checked, or "-" otherwise.
  label: TRUE, HALF-TRUE or FALSE (in case the claim is to be checked), or "-" otherwise 


NOTE 1: If the line does NOT contain an interesting claim, then claim_number=='N/A' and normalized_claim, label are missing.

NOTE 2: The same normalized claim (with the same claim number) can be associated with more than one sentence.


Example:

  ...
  65  TRUMP So we're losing our good jobs, so many of them. N/A
  66  TRUMP When you look at what's happening in Mexico, a friend of mine who builds plants said it's the eighth wonder of the world. N/A
  67  TRUMP They're building some of the biggest plants anywhere in the world, some of the most sophisticated, some of the best plants. N/A
  68  TRUMP With the United States, as he said, not so much.  N/A
  69  TRUMP So Ford is leaving. 1 Ford Motor Company is moving their small car division out of the USA. TRUE
  70  TRUMP You see that, their small car division leaving. 1 Ford Motor Company is moving their small car division out of the USA. TRUE
  71  TRUMP Thousands of jobs leaving Michigan, leaving Ohio. 2 Thousands of jobs are being lost in Michigan and Ohio due to Ford Motor Company moving their small car division out of the USA. FALSE
  ...


[7] CREDITS

Lab Organizers:

  Preslav Nakov, Qatar Computing Research Institute, HBKU 
  Lluís Màrquez, Amazon
  Alberto Barrón-Cedeño, Qatar Computing Research Institute, HBKU
  Wajdi Zaghouani, Carnegie Mellon University - Qatar
  Tamer Elsayed, Qatar University
  Reem Suwaileh, Qatar University
  Pepa Gencheva, Sofia University


Task website: http://alt.qcri.org/clef2018-factcheck/

Contact:   clef-factcheck@googlegroups.com
