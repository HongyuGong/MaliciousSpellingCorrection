import enchant
from enchant.checker import SpellChecker
import pickle
from fetch_toxic_score import fetch_toxic_score_online
import matplotlib.pyplot as plt

fn = "output/Correction_All_Sentences_Scores.pickle"
with open(fn, "rb") as handle:
    CASS = pickle.load(handle)

# X_Scores[0..3]: scores for method 0..3
# X_Scores[4]: scores for all methods
Original_Scores = [[],[],[],[],[]]
Revised_Scores = [[],[],[],[],[]]
Corrected_Scores = [[],[],[],[],[]]

for i in range(4):
    for j in range(len(CASS[i])):
        (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, \
        new_word_list, correction_word_list, correction_score, corrected_sentence) = CASS[i][j]
        Original_Scores[i].append(original_score)
        Revised_Scores[i].append(revised_toxic_score)
        Corrected_Scores[i].append(correction_score)
        Original_Scores[4].append(original_score)
        Revised_Scores[4].append(revised_toxic_score)
        Corrected_Scores[4].append(correction_score)
        
title_prefix = 'Original vs. Revised vs. Correction Scores - '
title_suffixes = ['add', 'delete', 'replace', 'permute', 'all']
for i in range(5):
    plt.figure(i)
    plt.plot(range(len(Original_Scores[i])),sorted(Original_Scores[i]), 'r',label='original')
    plt.plot(range(len(Revised_Scores[i])),sorted(Revised_Scores[i]), 'g', label='revised')
    plt.plot(range(len(Corrected_Scores[i])),sorted(Corrected_Scores[i]), 'b', label='corrected')
    plt.legend(loc=0)
    plt.xlabel('Data point')
    plt.ylabel('Score')
    plt.title(title_prefix+title_suffixes[i])
    plt.show()







