"""
regular_check.py

"""
from pyxdameraulevenshtein import damerau_levenshtein_distance as dist

def getCandFromDict(word, raw_corpus, refined_corpus):
    """
    use edit distance to generate candidates
    input: word
    output: a list of candidate words
    """
    cand_words = []
    cur_dist = 0
    while (cand_words == []):
        cur_dist += 1
        for key in refined_corpus: # smaller corpus
            if (dist(key, word) <= cur_dist):
                cand_words.append(key)
    return cand_words


def rawCheckOnDist(sent_list, raw_corpus, refined_corpus):
    """
    enumerate spelling correction candidates based on the edit distance
    """
    sent_token_list = []
    raw_corrections = []
    for sent in sent_list:
        token_list = sent.strip().split()
        corrected_token_list = token_list[:]
        corrections = []
        for ind in range(len(token_list)):
            token = token_list[ind]
            if (len(token) > 30):
                continue
            # spelling error
            if (token not in raw_corpus):
                cand_list = getCandFromDict(token, refined_corpus)
                if (len(cand_list) == 1):
                    cand_token = cand_list[0]
                    corrected_token_list[ind] = cand_token
                    corrections.append((cand_token, token))
        sent_token_list.append(corrected_token_list[:])
        raw_corrections.append(corrections[:])
    print("done stage 1: raw check on edit distance")
    return sent_token_list, raw_corrections   
