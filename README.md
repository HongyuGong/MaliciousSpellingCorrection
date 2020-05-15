***************************************************************************************************************************
This repository is currently under reconstruction, and we are refactoring the code for higher efficiency and better readability. We will provide detailed running instructions of our system.
***************************************************************************************************************************


This is the system for the paper "Context-Sensitive Malicious Spelling Error Correction" in the Web Conference WWW 2019. 

## Code structure:
1. add_errors/: the module to add malicious errors;
2. domain_corpus_generation/: the module to process domain corpus such as Perspective data or spam data;
3. context_based_selection/: the module to correct spelling errors based on context;
4. perspective_evaluation/: the module to run baselines spell checkers on Perspective data;
5. spam/: the module on error generation and correction on spam data.

## Data you may need to run spell_checker.py
1. vocab.txt: 
2. vectors.bin: 
3. dict_v1.pkl: https://drive.google.com/open?id=1VzT9u0YdhRcwSAN1vauA63ryvN0E_mJC
4. persective_train_dict.pickle: https://drive.google.com/open?id=1nfl0znt-oO8XK6yUIZ7hLjSltcRcmuqs

Put those files in the right path as shown in spell_checker.py


If you have any questions, please contact Hongyu Gong (hgong6@illinois.edu).

If you use our code, please cite our work:
Hongyu Gong, Yuchen Li, Suma Bhat, Pramod Viswanath. 2019. Context-Sensitive Malicious Spelling Error Correction. In \emph{Proceedings of the 2019 World Wide Web Conference (WWW'19), May 13-17, 2019, San Francisco, CA, USA.

@inproceedings{gong2019context,
  title={Context-Sensitive Malicious Spelling Error Correction},
  author={Gong, Hongyu and Li, Yuchen and Bhat, Suma and Viswanath, Pramod},
  booktitle = {Proceedings of the 2019 World Wide Web Conference (WWW'19)},
  month = {May},
  year={2019}
}
