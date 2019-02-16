from ekphrasis.classes.spellcorrect import SpellCorrector

import pickle
import matplotlib.pyplot as plt

import requests


'''
Helper Functions
'''

'''
This function returns the toxic score of a comment on www.perspectiveapi.com,
given an input comment.
The score is fetched from www.perspectiveapi.com using request.
input:
    sentence - the input comment
output:
    toxic_score - the toxic score of sentence (-1 if error)
'''
def fetch_toxic_score_online(sentence):
    # the variable "sessionId" is a random value written arbitrarily
    try:
        r = requests.post('http://www.perspectiveapi.com/check', json={"comment":sentence, "sessionId":"10002022"})
    except:
        print('fetch_toxic_score_online: r = requests.post() bug')
        print(sentence)
        return 0 # regarded as successfully deceiving Perspective API

    # The json variable is of the following format:
    # {'attributeScores': {'TOXICITY': {'spanScores': [{'end': 6, 'score': {'type': 'PROBABILITY', 'value': 0.3378245}, 'begin': 0}], 'summaryScore': {'type': 'PROBABILITY', 'value': 0.3378245}}}, 'languages': ['en']}
    #print(r)
    if (str(r)=='<Response [200]>'):
        j = r.json()
        if ('attributeScores' in j):
            toxic_score = j['attributeScores']['TOXICITY']['summaryScore']['value']
        else:
            print('attributeScores not in j = r.json()')
            print(j)
            print(sentence)
            toxic_score = 0 # regarded as successfully deceiving Perspective API
    else:
        toxic_score = 0 # regarded as successfully deceiving Perspective API
    return toxic_score

'''
This function returns a list of toxic scores of a list of comments based on www.perspectiveapi.com,
given a list of input comment.
The scores are fetched from www.perspectiveapi.com using request.
input:
    Sentence_List - the input comment
    outfile - (optional) the output file that holds the list of toxic scores of sentences in Sentence_List
output:
    Toxic_Score_List - the list of toxic scores of sentences in Sentence_List
effect:
    outfile holds Toxic_Score_List
'''
def fetch_toxic_score_list_online(Sentence_List, outfile=0):
    Toxic_Score_List = []
    for s in Sentence_List:
        Toxic_Score_List.append(fetch_toxic_score_online(s))
    if (outfile != 0):
        out=open(outfile,'wt')
        out.write('%s' % (''.join(str(toxic_score)+'\n' for toxic_score in Toxic_Score_List)))
        out.close()
    return Toxic_Score_List

'''
input:
    paragraph: a (multi-word) sentence or paragraph
    word_correction_func: a function that corrects a word (default: None)
    paragraph_correction_func: a function that corrects a (multi-word) sentence or paragraph (default: None)
output:
    correction_word_list: a list of (wrong_word, suggested_word)
    corrected_sentence: a corrected version of the input `paragraph`
note:
    The input `paragraph` is pre-processed, such that punctuations are either non-existent, or
        separated from words.
    Exactly one of the inputs word_correction_func and paragraph_correction_func should be specified,
        so that the function knows which spelling correction method to use.
    Require that the input `paragraph_correction_func` must return both `correction_word_list` and
        `corrected_sentence`.
'''
def correct_a_paragraph(paragraph, word_correction_func=None, paragraph_correction_func=None):
    if (word_correction_func != None): # correct words one by one
        correction_word_list = []
        corrected_sentence = ''
        paragraph_sp = paragraph.split()
        for word in paragraph_sp:
            corrected_word = word_correction_func(word)
            if (corrected_word != word):
                correction_word_list.append((word, corrected_word))
            corrected_sentence += (' '+corrected_word)
    elif (paragraph_correction_func != None):
        correction_word_list, corrected_sentence = paragraph_correction_func(paragraph)
    else:
        raise ValueError('Exactly one of the inputs word_correction_func and paragraph_correction_func should be specified')
    return correction_word_list, corrected_sentence

'''
Test a spelling correction algorithm on 'All_Sentences_Scores_Filtered.pickle'
input:
    ASSF_fn: the file name of a pickle that stores All_Sentences_Scores_Filtered: a list [0..4] of list of
        (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, new_word_list)
        where filter means the following:
        check the (sentence, most toxic word) list.
        - If len(most toxic word) <= 2
        - If the most toxic word appears less than 100 times in the dictionary, then discard the sentence.
        - if the most toxic word is auxiliary verb, then discard the sentence.
    CASS_fn: the file name of a pickle that stores the output Correction_All_Sentences_Scores
    word_correction_func: a function that corrects a word (default: None)
    paragraph_correction_func: a function that corrects a (multi-word) sentence or paragraph (default: None)
output:
    Correction_All_Sentences_Scores: a list [0..3] of list of
        (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word,
        new_word_list, correction_word_list, correction_score, corrected_sentence), where
        correction_word_list is a list of (wrong_word, suggested_word).
note:
    The input sentences are pre-processed, such that punctuations are either non-existent, or
        separated from words.
    Exactly one of the inputs word_correction_func and paragraph_correction_func should be specified,
        so that the function knows which spelling correction method to use
'''
def eval_spelling_correction_perspective(ASSF_fn, CASS_fn, word_correction_func=None, paragraph_correction_func=None):
    with open(ASSF_fn, "rb") as handle:
        All_Sentences_Scores_Filtered = pickle.load(handle)
    print('Number of sentences: %d' % (len(All_Sentences_Scores_Filtered[0])+len(All_Sentences_Scores_Filtered[1])
    +len(All_Sentences_Scores_Filtered[2])+len(All_Sentences_Scores_Filtered[3])+len(All_Sentences_Scores_Filtered[4])))

    Correction_All_Sentences_Scores = []
    count = 0

    for i in range(4):
        Correction_All_Sentences_Scores.append([])
        for j in range(len(All_Sentences_Scores_Filtered[i])):
            if (count == 2626):
                print('the %d-th sentence is skipped, because its correction time is too long.' % count)
                count += 1
                continue

            (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, new_word_list) = \
            All_Sentences_Scores_Filtered[i][j]

            original_score = fetch_toxic_score_online(original_sentence)
            revised_toxic_score = fetch_toxic_score_online(revised_sentence)

            correction_word_list, corrected_sentence = correct_a_paragraph(revised_sentence, word_correction_func, paragraph_correction_func)
            correction_score = fetch_toxic_score_online(corrected_sentence)

            Correction_All_Sentences_Scores[i].append((original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, \
                                           new_word_list, correction_word_list, correction_score, corrected_sentence))

            count += 1
            if (count%100==0):
                print('\tprocessed %d sentences' % count)
                partial_CASS_fn = CASS_fn.split('.pickle')[0] + str(count) + '.pickle'
                with open(partial_CASS_fn, "wb") as handle: # save progress
                    pickle.dump(Correction_All_Sentences_Scores, handle, protocol=2)
                print('\t%s dumped' % partial_CASS_fn)

    with open(CASS_fn, "wb") as handle:
        pickle.dump(Correction_All_Sentences_Scores, handle, protocol=2)
    print('%s dumped' % CASS_fn)

    return Correction_All_Sentences_Scores

'''
Plot correction effects
input:
    CASS_fn: the file name of a pickle that stores the output Correction_All_Sentences_Scores
'''
def plot_correction_effects(CASS_fn):
    with open(CASS_fn, "rb") as handle:
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

'''
Do statistics on the spelling correction methods.
input:
    CASS_fn: the file name of a pickle that stores the output Correction_All_Sentences_Scores
print:
1. accuracy
2. score distribution
'''
def spelling_correction_statistics(CASS_fn):

    print('\nExperiment 1: accuracy\n')
    with open(CASS_fn, "rb") as handle:
        CASS = pickle.load(handle)

    accuracy_scores = []

    for i in range(4):
        print('i = %d' % i)
        count = 0
        for j in range(len(CASS[i])):
            (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, \
            new_word_list, correction_word_list, correction_score, corrected_sentence) = CASS[i][j]
            if (len(new_word_list)==0):
                accuracy_scores.append(1)
            else:
                if (len(correction_word_list)==0):
                    accuracy_scores.append(0)
                else:
                    num_correct = 0
                    for k in range(len(correction_word_list)):
                        if ((correction_word_list[k][0] in new_word_list) and (correction_word_list[k][1] == correct_word)):
                            num_correct += 1
                    accuracy_scores.append(1.0*num_correct/len(new_word_list))
            count += 1
            if (count%100==0):
                print('\tprocessed %d sentences' % count)

    avg_accuracy_score = 1.0 * sum(accuracy_scores) / len(accuracy_scores)
    print('avg_accuracy_score: %f' % avg_accuracy_score)

    print('\nExperiment 2: score distribution\n')

    # groups[toxicity]: a list of avg toxic scores after correction for sentences with original toxicity
    #                   in the range [toxicity, toxicity+0.1)
    groups = {}
    for toxicity in [0.5, 0.6, 0.7, 0.8, 0.9]:
        groups[toxicity] = []

    for i in range(4):
        print('i = %d' % i)
        count = 0
        for j in range(len(CASS[i])):
            (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, \
            new_word_list, correction_word_list, correction_score, corrected_sentence) = CASS[i][j]

            if (original_score >= 0.5):
                toxicity_group_index = 1.0 * int(10 * original_score) / 10
                groups[toxicity_group_index].append(correction_score)

            count += 1
            if (count%100==0):
                print('\tprocessed %d sentences' % count)

    avg_group_toxicities = {}
    for toxicity in [0.5, 0.6, 0.7, 0.8, 0.9]:
        avg_group_toxicities[toxicity] = 1.0 * sum(groups[toxicity]) / len(groups[toxicity])
        print('range [%f, %f): avg_toxicity=%f' % (toxicity, toxicity+0.1, avg_group_toxicities[toxicity]))


'''
Test the ekphrasis package on 'All_Sentences_Scores_Filtered.pickle'
input:
   ASSF_fn: the file name of a pickle that stores All_Sentences_Scores_Filtered: a list [0..4] of list of
        (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, new_word_list)
        where filter means the following:
        check the (sentence, most toxic word) list.
        - If len(most toxic word) <= 2
        - If the most toxic word appears less than 100 times in the dictionary, then discard the sentence.
        - if the most toxic word is auxiliary verb, then discard the sentence.
    CASS_fn: the file name of a pickle that stores the output Correction_All_Sentences_Scores
output:
    Correction_All_Sentences_Scores: a list [0..3] of list of
        (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word,
        new_word_list, correction_word_list, correction_score, corrected_sentence), where
        correction_word_list is a list of (wrong_word, suggested_word).
note:
    The input sentences are pre-processed, such that punctuations are either non-existent, or
        separated from words.
'''

ASSF_fn = 'input/All_Sentences_Scores_Filtered.pickle'
CASS_fn = "output/Correction_All_Sentences_Scores.pickle"

sp = SpellCorrector(corpus="english")
ekphrasis_word_correction_func = lambda w: sp.correct(w)

Correction_All_Sentences_Scores = eval_spelling_correction_perspective(ASSF_fn, CASS_fn, word_correction_func=ekphrasis_word_correction_func)


'''
2018.5.20
Plot correction effects
'''

CASS_fn = "output/Correction_All_Sentences_Scores.pickle"
plot_correction_effects(CASS_fn)


'''
Calculate
1. accuracy
2. score distribution
'''

CASS_fn = "output/Correction_All_Sentences_Scores.pickle"
spelling_correction_statistics(CASS_fn)


'''
save original_sentences and corrected_sentences
'''
original_sentences_fn = 'output/original_sentences.txt'
corrected_sentences_fn = 'output/corrected_sentences.txt'
with open(original_sentences_fn, 'wt') as original_sentences_f, open(corrected_sentences_fn, 'wt') as corrected_sentences_f:
    for i in range(4):
        for j in range(len(Correction_All_Sentences_Scores[i])):
            (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, \
            new_word_list, correction_word_list, correction_score, corrected_sentence) = Correction_All_Sentences_Scores[i][j]
            original_sentences_f.write(original_sentence + '\n')
            corrected_sentences_f.write(corrected_sentence + '\n')
