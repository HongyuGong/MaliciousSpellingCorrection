# -*- coding: utf-8 -*-
import pickle
from add_spelling_errors import change_a_word_5_ways_invalid_v2
from spam_util import preprocess
from corpus_util import loadDict

def load_pickle(fn):
    with open(fn, "rb") as handle:
        Content = pickle.load(handle)
    return Content

def modify_toxic_words_in_file(Toxic_Words, fn, out_fn):
    
    with open(fn) as f:
        sentence = f.read()
    Words_In_Sentence = sentence.split()
    New_Words_In_Sentence = []
    Correct_and_Wrong_Words = []
    for i in range(len(Words_In_Sentence)):
        if (Words_In_Sentence[i] in Toxic_Words):
            wrong_word = change_a_word_5_ways_invalid_v2(Words_In_Sentence[i])[0]
            New_Words_In_Sentence.append(wrong_word)
            Correct_and_Wrong_Words.append((Words_In_Sentence[i], wrong_word))
        else:
            New_Words_In_Sentence.append(Words_In_Sentence[i])
            
    modified_content = ''
    for i in range(len(New_Words_In_Sentence)):
        try:
            modified_content = modified_content + New_Words_In_Sentence[i] + ' '
        except:
            print(New_Words_In_Sentence[i])
            print(Words_In_Sentence[i])
            print(sentence)
    original_and_modified_content = (sentence, modified_content)

    with open(out_fn, "w") as f:
        try:
            f.write(sentence+'\n')
            f.write(modified_content+'\n')
            for j in range(len(Correct_and_Wrong_Words)):
                f.write(Correct_and_Wrong_Words[j][0]+', '+Correct_and_Wrong_Words[j][1]+'; ')
        except:
            print('modify_toxic_words_in_file: around line 77: write to file bug for sentence:')
            print('sentence:',sentence)
            print('modified_content:',modified_content)
            print('Correct_and_Wrong_Words:',Correct_and_Wrong_Words)

    return original_and_modified_content, Correct_and_Wrong_Words
    

def modify_toxic_words_in_file_v2(Toxic_Words, fn, out_fn):
    
    with open(fn) as f:
        content = f.read()    
    
    Words_In_Sentence, lemma_list = preprocess(content)
    if (len(Words_In_Sentence) != len(lemma_list)):
        print('bug: len(word_list) != len(lemma_list)')
        print(content)
        print(len(Words_In_Sentence), Words_In_Sentence)        
        print(len(lemma_list), lemma_list)
    
    New_Words_In_Sentence = []
    Correct_and_Wrong_Words = []
    for i in range(len(Words_In_Sentence)):
        if (lemma_list[i] in Toxic_Words):
            wrong_word = change_a_word_5_ways_invalid_v2(Words_In_Sentence[i])[0]
            New_Words_In_Sentence.append(wrong_word)
            Correct_and_Wrong_Words.append((Words_In_Sentence[i], wrong_word))
        else:
            New_Words_In_Sentence.append(Words_In_Sentence[i])
    
    sentence = ''
    for i in range(len(Words_In_Sentence)):
        try:
            sentence = sentence + Words_In_Sentence[i] + ' '
        except:
            print(Words_In_Sentence[i])
            print(Words_In_Sentence)
        
    modified_content = ''
    for i in range(len(New_Words_In_Sentence)):
        try:
            modified_content = modified_content + New_Words_In_Sentence[i] + ' '
        except:
            print(New_Words_In_Sentence[i])
            print(Words_In_Sentence[i])
            print(Words_In_Sentence)
            
    original_and_modified_content = (sentence, modified_content)

    with open(out_fn, "w") as f:
        try:
            f.write(sentence+'\n')
            f.write(modified_content+'\n')
            for j in range(len(Correct_and_Wrong_Words)):
                f.write(Correct_and_Wrong_Words[j][0]+', '+Correct_and_Wrong_Words[j][1]+'; ')
        except:
            print('modify_toxic_words_in_file: around line 600: write to file bug for sentence:')
            print('sentence:',sentence)
            print('modified_content:',modified_content)
            print('Correct_and_Wrong_Words:',Correct_and_Wrong_Words)

    return original_and_modified_content, Correct_and_Wrong_Words


def modify_toxic_words_in_file_v3(Toxic_Words, fn, out_fn):
    
    with open(fn) as f:
        content = f.read()    
    
    Words_In_Sentence, lemma_list = preprocess(content)
    if (len(Words_In_Sentence) != len(lemma_list)):
        print('bug: len(word_list) != len(lemma_list)')
        print(content)
        print(len(Words_In_Sentence), Words_In_Sentence)        
        print(len(lemma_list), lemma_list)
    
    New_Words_In_Sentence = []
    Correct_and_Wrong_Words = []
    for i in range(len(Words_In_Sentence)):
        if (len(Words_In_Sentence[i])>3 and (lemma_list[i] in Toxic_Words)):
            wrong_word = change_a_word_5_ways_invalid_v2(Words_In_Sentence[i])[0]
            New_Words_In_Sentence.append(wrong_word)
            Correct_and_Wrong_Words.append((Words_In_Sentence[i], wrong_word))
        else:
            New_Words_In_Sentence.append(Words_In_Sentence[i])
    
    sentence = ''
    for i in range(len(Words_In_Sentence)):
        try:
            sentence = sentence + Words_In_Sentence[i] + ' '
        except:
            print(Words_In_Sentence[i])
            print(Words_In_Sentence)
        
    modified_content = ''
    for i in range(len(New_Words_In_Sentence)):
        try:
            modified_content = modified_content + New_Words_In_Sentence[i] + ' '
        except:
            print(New_Words_In_Sentence[i])
            print(Words_In_Sentence[i])
            print(Words_In_Sentence)
            
    original_and_modified_content = (sentence, modified_content)

    with open(out_fn, "w") as f:
        try:
            f.write(sentence+'\n')
            f.write(modified_content+'\n')
            for j in range(len(Correct_and_Wrong_Words)):
                f.write(Correct_and_Wrong_Words[j][0]+', '+Correct_and_Wrong_Words[j][1]+'; ')
        except:
            print('modify_toxic_words_in_file: around line 600: write to file bug for sentence:')
            print('sentence:',sentence)
            print('modified_content:',modified_content)
            print('Correct_and_Wrong_Words:',Correct_and_Wrong_Words)

    return original_and_modified_content, Correct_and_Wrong_Words


def process_spam_file(fn, out_fn, Toxic_Words):

    try:
        f = open(fn)
        f.close()
        file_missing = False
    except:
        file_missing = True
        
    try:
        original_and_modified_content, Correct_and_Wrong_Words = modify_toxic_words_in_file_v3(Toxic_Words, fn, out_fn)
        op_successful = True
    except:
        original_and_modified_content = None
        Correct_and_Wrong_Words = None
        op_successful = False
    
    return file_missing, original_and_modified_content, Correct_and_Wrong_Words, op_successful
    
    
