***************************************************************************************************************************
This repository is currently under reconstruction, and we are refactoring the code for higher efficiency and better readability. We will provide detailed running instructions of our system.
***************************************************************************************************************************


This is the system for the paper "Context-Sensitive Malicious Spelling Error Correction" to appear in the Web Conference 2019. 

Code structure:
1. add_errors/: the module to add malicious errors;
2. domain_corpus_generation/: the module to process domain corpus such as Perspective data or spam data;
3. context_based_selection/: the module to correct spelling errors based on context;
4. perspective_evaluation/: the module to run baselines spell checkers on Perspective data;
5. spam/: the module on error generation and correction on spam data.

Data you may need to run spell_checker.py
1. vocab.txt: https://drive.google.com/open?id=1S2jHg7H-XZmL4QHBVEGhCK7TLSq3FOx3
2. vectors.bin: https://drive.google.com/open?id=1zZ49o8OxZ2nPpejkKtyxlOwiDM0zs-QK
3. dict_v1.pkl: https://drive.google.com/open?id=1X4yGKC74AFn8DaminEz8e-kj70Wju3U8
4. persective_train_dict.pickle: https://drive.google.com/open?id=1ytt2J83Is2t__-wDzO9b9wZJEFvTc9on

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
