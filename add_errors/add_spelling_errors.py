import random
import string
from corpus_util import loadDict, loadDict_std
import pickle

    
def readTag(fn):
    TARGET_TAG_SET = ["V", "N", "A"]    
    f = open(fn, "r")
    lines = f.readlines()
    selected_inds = []
    selected_words = []
    tok_sent = []
    for line in lines:
        try:
            sent, tag, score, orig_sent = line.strip().split("\t")
        except:
            continue
        tag_seq = tag.split()
        sent_seq = sent.split()
        inds = [ind for ind in range(len(tag_seq)) if tag_seq[ind] in TARGET_TAG_SET]
        selected_inds.append(inds[:])
        words = [sent_seq[ind] for ind in inds]
        selected_words.append(words[:])
        tok_sent.append(sent)
        #if (len(selected_words)>=2):
        #    break
    return selected_inds, selected_words, tok_sent
    
'''
load a list of (toxic_score, sentence, most_toxic_word)
'''
def load_toxic_word(fn):
    with open(fn, "rb") as handle:
        Sentence_And_Toxic_Word = pickle.load(handle)
    return Sentence_And_Toxic_Word
        
    
'''
A method to change a word that maintains edit distance 1
input:
    word - the input word
output:
    modified_word - a word that has edit distance 1 from the input word
'''
def change_a_word_dis1(word):
    Alphabet_List = list(string.ascii_lowercase)
    Alphabet_List.append(' ')
    
    # 0 - add
    # 1 - delete
    # 2 - change    
    method = random.randint(0, 2)
    
    if (method==0):
        pos = random.randint(0, len(word))
        word1 = word[0:pos]
        word2 = word[pos:len(word)]
        add = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
        return word1+add+word2
        
    elif (method==1):
        pos = random.randint(0, len(word)-1)
        word1 = word[0:pos]
        word2 = word[pos+1:len(word)]
        return word1+word2
        
    elif (method==2):
        pos = random.randint(0, len(word)-1)
        word1 = word[0:pos]
        word2 = word[pos+1:len(word)]
        change = word[pos]
        while (change==word[pos]):        
            change = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
        return word1+change+word2

'''
A method to change a word that randomly picks one of {add 1 char, delete 1 char, 
replace 1 char, permute 2 adjacent chars, separate all chars with ' '}.
input:
    word - the input word
output:
    modified_word - a word that has edit distance 1 from the input word
    method - the method used to modify. (0 - add, 1 - delete, 2 - replace, 3 - permute, 4 - separate)
'''
def change_a_word_5_ways(word):
    Alphabet_List = list(string.ascii_lowercase)
    Alphabet_List.append(' ')
    
    # 0 - add
    # 1 - delete
    # 2 - replace  
    # 3 - permute
    # 4 - separate
    method = random.randint(0, 4) # if method>4, then no return value
    
    if (method==0):
        pos = random.randint(0, len(word))
        word1 = word[0:pos]
        word2 = word[pos:len(word)]
        add = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
        return word1+add+word2, 0
        
    elif (method==1):
        pos = random.randint(0, len(word)-1)
        word1 = word[0:pos]
        word2 = word[pos+1:len(word)]
        return word1+word2, 1
        
    elif (method==2):
        pos = random.randint(0, len(word)-1)
        word1 = word[0:pos]
        word2 = word[pos+1:len(word)]
        change = word[pos]
        while (change==word[pos]):        
            change = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
        return word1+change+word2, 2
        
    elif (method==3):
        if (len(word)<=1):
            return word, 3
        else:
            pos = random.randint(0, len(word)-2)
            word1 = word[0:pos]
            word2 = word[pos+2:len(word)]
            return word1+word[pos+1]+word[pos]+word2, 3
        
    elif (method==4):
        modified_word = ''        
        for c in list(word):
            modified_word = modified_word+' '+c
        modified_word = modified_word[1:len(modified_word)]
        return modified_word, 4

def change_a_word_5_ways_invalid(word):
    Alphabet_List = list(string.ascii_lowercase)
    Alphabet_List.append(' ')
    cnt = loadDict()
    
    # 0 - add
    # 1 - delete
    # 2 - replace  
    # 3 - permute
    # 4 - separate
    method = random.randint(0, 4) # if method>4, then no return value
    ret_word_and_method = ('',-1)
    count = 0
    ret_flag = False
    
    while (ret_flag == False and count < 10):
        
        count = count + 1
    
        if (method==0):
            pos = random.randint(0, len(word))
            word1 = word[0:pos]
            word2 = word[pos:len(word)]
            add = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
            ret_word_and_method = (word1+add+word2, 0)
            
        elif (method==1):
            pos = random.randint(0, len(word)-1)
            word1 = word[0:pos]
            word2 = word[pos+1:len(word)]
            ret_word_and_method = (word1+word2, 1)
            
        elif (method==2):
            pos = random.randint(0, len(word)-1)
            word1 = word[0:pos]
            word2 = word[pos+1:len(word)]
            change = word[pos]
            while (change==word[pos]):        
                change = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
            ret_word_and_method =( word1+change+word2, 2)
            
        elif (method==3):
            if (len(word)<=1):
                ret_word_and_method = (word, 3)
            else:
                pos = random.randint(0, len(word)-2)
                word1 = word[0:pos]
                word2 = word[pos+2:len(word)]
                ret_word_and_method = (word1+word[pos+1]+word[pos]+word2, 3)
            
        elif (method==4):
            modified_word = ''        
            for c in list(word):
                modified_word = modified_word+' '+c
            modified_word = modified_word[1:len(modified_word)]
            ret_word_and_method = (modified_word, 4)
            
        if (cnt[ret_word_and_method[0]] == 0):
            ret_flag = True
        else:
            method = random.randint(0, 3)
            
    return ret_word_and_method[0], ret_word_and_method[1]

def change_a_word_5_ways_invalid_v2(word):
    Alphabet_List = list(string.ascii_lowercase)
    cnt = loadDict()
    
    # 0 - add
    # 1 - delete
    # 2 - replace  
    # 3 - permute
    method = random.randint(0, 3) 
    ret_word_and_method = ('',-1)
    count = 0
    ret_flag = False
    
    while (ret_flag == False and count < 10):
        
        count = count + 1
    
        if (method==0):
            pos = random.randint(0, len(word))
            word1 = word[0:pos]
            word2 = word[pos:len(word)]
            add = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
            ret_word_and_method = (word1+add+word2, 0)
            if (ret_word_and_method[0]==''):
                print(word)
                print(ret_word_and_method[0])
                print(method)
                print(pos)
                print(word1)
                print(word2)
                print(add)
                
            
        elif (method==1):
            if (len(word)<8):
                while (method==1):
                    method = random.randint(0, 4)
                continue
            pos = random.randint(0, len(word)-1)
            word1 = word[0:pos]
            word2 = word[pos+1:len(word)]
            ret_word_and_method = (word1+word2, 1)
            if (ret_word_and_method[0]==''):
                print(word)
                print(ret_word_and_method[0])
                print(method)
                print(pos)
                print(word1)
                print(word2)
            
        elif (method==2):
            pos = random.randint(0, len(word)-1)
            word1 = word[0:pos]
            word2 = word[pos+1:len(word)]
            change = word[pos]
            while (change==word[pos]):        
                change = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
            ret_word_and_method =( word1+change+word2, 2)
            if (ret_word_and_method[0]==''):
                print(word)
                print(ret_word_and_method[0])
                print(method)
                print(pos)
                print(word1)
                print(word2)
            
        elif (method==3):
            if (len(word)<=1):
                ret_word_and_method = (word, 3)
            else:
                pos = random.randint(0, len(word)-2)
                word1 = word[0:pos]
                word2 = word[pos+2:len(word)]
                ret_word_and_method = (word1+word[pos+1]+word[pos]+word2, 3)
            if (ret_word_and_method[0]==''):
                print(word)
                print(ret_word_and_method[0])
                print(method)
                print(pos)
                print(word1)
                print(word2)
            
        if (cnt[ret_word_and_method[0]] == 0):
            ret_flag = True
        else:
            method = random.randint(0, 3)
    
    if (ret_flag == False and count >= 10 and ret_word_and_method[1]==0):
        pos = random.randint(0, len(word))
        word1 = word[0:pos]
        word2 = word[pos:len(word)]
        add = '*'
        ret_word_and_method = (word1+add+word2, 0)
    elif (ret_flag == False and count >= 10 and ret_word_and_method[1]==2):
        pos = random.randint(0, len(word)-1)
        word1 = word[0:pos]
        word2 = word[pos+1:len(word)]
        change = '*'
        ret_word_and_method =( word1+change+word2, 2)

    if (ret_word_and_method[1]==-1):
        if (len(word) >= 8):
            pos = random.randint(0, len(word)-1)
            word1 = word[0:pos]
            word2 = word[pos+1:len(word)]
            ret_word_and_method = (word1+word2, 1)
        else:
            pos = random.randint(0, len(word))
            word1 = word[0:pos]
            word2 = word[pos:len(word)]
            add = '*'
            ret_word_and_method = (word1+add+word2, 0)
    
    if (ret_word_and_method[0]==''):
        print(word)
        print(ret_word_and_method[0])
        print(ret_word_and_method[1])
    
    return ret_word_and_method[0], ret_word_and_method[1]


def change_a_word_5_ways_invalid_v2_force_method(word, method):
    Alphabet_List = list(string.ascii_lowercase)
    cnt = loadDict()
    
    # 0 - add
    # 1 - delete
    # 2 - replace  
    # 3 - permute 
    ret_word_and_method = ('',-1)
    count = 0
    ret_flag = False
    
    while (ret_flag == False and count < 10):
        
        count = count + 1
    
        if (method==0):
            pos = random.randint(0, len(word))
            word1 = word[0:pos]
            word2 = word[pos:len(word)]
            add = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
            ret_word_and_method = (word1+add+word2, 0)
            if (ret_word_and_method[0]==''):
                print(word)
                print(ret_word_and_method[0])
                print(method)
                print(pos)
                print(word1)
                print(word2)
                print(add)
                
            
        elif (method==1):
            if (len(word)<8):
                print('Bug: used delete method for len(word)')
                return 'Bug: used delete method for len(word)', 1
            pos = random.randint(0, len(word)-1)
            word1 = word[0:pos]
            word2 = word[pos+1:len(word)]
            ret_word_and_method = (word1+word2, 1)
            if (ret_word_and_method[0]==''):
                print(word)
                print(ret_word_and_method[0])
                print(method)
                print(pos)
                print(word1)
                print(word2)
            
        elif (method==2):
            pos = random.randint(0, len(word)-1)
            word1 = word[0:pos]
            word2 = word[pos+1:len(word)]
            change = word[pos]
            while (change==word[pos]):        
                change = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
            ret_word_and_method =( word1+change+word2, 2)
            if (ret_word_and_method[0]==''):
                print(word)
                print(ret_word_and_method[0])
                print(method)
                print(pos)
                print(word1)
                print(word2)
            
        elif (method==3):
            if (len(word)<=1):
                ret_word_and_method = (word, 3)
            else:
                pos = random.randint(0, len(word)-2)
                word1 = word[0:pos]
                word2 = word[pos+2:len(word)]
                ret_word_and_method = (word1+word[pos+1]+word[pos]+word2, 3)
            if (ret_word_and_method[0]==''):
                print(word)
                print(ret_word_and_method[0])
                print(method)
                print(pos)
                print(word1)
                print(word2)
            
        if (cnt[ret_word_and_method[0]] == 0):
            ret_flag = True
    
    if (ret_flag == False and count >= 10 and ret_word_and_method[1]==0):
        pos = random.randint(0, len(word))
        word1 = word[0:pos]
        word2 = word[pos:len(word)]
        add = '*'
        ret_word_and_method = (word1+add+word2, 0)
    elif (ret_flag == False and count >= 10 and ret_word_and_method[1]==2):
        pos = random.randint(0, len(word)-1)
        word1 = word[0:pos]
        word2 = word[pos+1:len(word)]
        change = '*'
        ret_word_and_method =( word1+change+word2, 2)

    if (ret_word_and_method[1]==-1):
        if (len(word) >= 8):
            pos = random.randint(0, len(word)-1)
            word1 = word[0:pos]
            word2 = word[pos+1:len(word)]
            ret_word_and_method = (word1+word2, 1)
        else:
            pos = random.randint(0, len(word))
            word1 = word[0:pos]
            word2 = word[pos:len(word)]
            add = '*'
            ret_word_and_method = (word1+add+word2, 0)
    
    if (ret_word_and_method[0]==''):
        print(word)
        print(ret_word_and_method[0])
        print(ret_word_and_method[1])
    
    return ret_word_and_method[0], ret_word_and_method[1]


def modify_one_word_dis1(sentence, Words_List):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p,'')
    Words_In_Sentence = s_wo_punctuation.split()
    #print(Words_In_Sentence)
    Modified_Sentences = []
    #print(Words_List)    
    for word in Words_List:
        New_Words_In_Sentence = Words_In_Sentence[:] # Note that Python by default passes by reference
        #print(New_Words_In_Sentence)
        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
        #print(Indices)
        for i in Indices:
            #print(New_Words_In_Sentence[i])
            New_Words_In_Sentence[i] = change_a_word_dis1(New_Words_In_Sentence[i])
            #print(New_Words_In_Sentence[i])
        new_sentence = ''
        for w in New_Words_In_Sentence:
            new_sentence = new_sentence + w + ' '
        Modified_Sentences.append(new_sentence)
    return Modified_Sentences


def modify_one_word_5_ways(sentence, Words_List):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p,'')
    Words_In_Sentence = s_wo_punctuation.split()
    #print(Words_In_Sentence)
    Modified_Sentences = []
    #print(Words_List)    
    for word in Words_List:
        New_Words_In_Sentence = Words_In_Sentence[:] # Note that Python by default passes by reference
        #print(New_Words_In_Sentence)
        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
        #print(Indices)
        method = -1        
        for i in Indices:
            #print(New_Words_In_Sentence[i])
            #print(type(New_Words_In_Sentence))
            #s = New_Words_In_Sentence            
            #print('s=',s)            
            New_Words_In_Sentence[i], method = change_a_word_5_ways(New_Words_In_Sentence[i])            
            #print(New_Words_In_Sentence[i])
        new_sentence = ''
        for w in New_Words_In_Sentence:
            new_sentence = new_sentence + w + ' '
        Modified_Sentences.append([new_sentence, method])
    return Modified_Sentences
    
def modify_one_word_5_ways_invalid(sentence, Words_List):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p,'')
    Words_In_Sentence = s_wo_punctuation.split()

    Modified_Sentences = []
  
    for word in Words_List:
        for p in list(string.punctuation):
            word = word.replace(p,'')
        New_Words_In_Sentence = Words_In_Sentence[:] # Note that Python by default passes by reference
        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
        if (len(Indices)>0):  
            method = -1        
            for i in Indices:
                New_Words_In_Sentence[i], method = change_a_word_5_ways_invalid(New_Words_In_Sentence[i])            
            new_sentence = ''
            for w in New_Words_In_Sentence:
                new_sentence = new_sentence + w + ' '
            Modified_Sentences.append([new_sentence, method, word, New_Words_In_Sentence[Indices[0]]])
    return Modified_Sentences
    

def modify_one_word_5_ways_invalid_v2(sentence, Words_List):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p,'')
    Words_In_Sentence = s_wo_punctuation.split()

    Modified_Sentences = []
  
    for word in Words_List:
        for p in list(string.punctuation):
            word = word.replace(p,'')
        New_Words_In_Sentence = Words_In_Sentence[:] # Note that Python by default passes by reference
        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
        if (len(Indices)>0):  
            method = -1        
            for i in Indices:
                New_Words_In_Sentence[i], method = change_a_word_5_ways_invalid_v2(New_Words_In_Sentence[i])            
            new_sentence = ''
            for w in New_Words_In_Sentence:
                new_sentence = new_sentence + w + ' '
            Modified_Sentences.append([new_sentence, method, word, [New_Words_In_Sentence[i] for i in Indices]])
    return Modified_Sentences


def modify_one_word_5_ways_invalid_v2_force_method(sentence, Words_List, method):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p,'')
    Words_In_Sentence = s_wo_punctuation.split()

    Modified_Sentences = []
  
    for word in Words_List:
        for p in list(string.punctuation):
            word = word.replace(p,'')
        New_Words_In_Sentence = Words_In_Sentence[:] # Note that Python by default passes by reference
        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
        if (len(Indices)>0):        
            for i in Indices:
                New_Words_In_Sentence[i], method = change_a_word_5_ways_invalid_v2_force_method(New_Words_In_Sentence[i], method)            
            new_sentence = ''
            for w in New_Words_In_Sentence:
                new_sentence = new_sentence + w + ' '
            Modified_Sentences.append([new_sentence, method, word, [New_Words_In_Sentence[i] for i in Indices]])
    return Modified_Sentences
    


def modify_key_words_5_ways_readTag(indices,sentence):
    Words_In_Sentence = sentence.split()
    selected_word_list = [Words_In_Sentence[i] for i in indices]
    selected_word_list = list(set(selected_word_list)) # unique
    Modified_Sentences = modify_one_word_5_ways(sentence, selected_word_list)
    #print(Modified_Sentences)
    Modified_Sentences_And_Words = [[Modified_Sentences[i][0], Modified_Sentences[i][1], selected_word_list[i]] for i in range(len(selected_word_list))]
    #print(Modified_Sentences_And_Words)    
    return Modified_Sentences_And_Words 
    


def modify_key_words_5_ways_readTag_invalid(indices,sentence):
    Words_In_Sentence = sentence.split()
    selected_word_list = [Words_In_Sentence[i] for i in indices]
    selected_word_list = list(set(selected_word_list)) # unique
    Modified_Sentences = modify_one_word_5_ways_invalid(sentence, selected_word_list)
    #print(Modified_Sentences)
    Modified_Sentences_And_Words = []
    for i in range(len(selected_word_list)):
        try:
            Modified_Sentences_And_Words.append([[Modified_Sentences[i][0], Modified_Sentences[i][1], selected_word_list[i], Modified_Sentences[i][3]]])
        except:
            print('len(Modified_Sentences) < 4:',i)
    #print(Modified_Sentences_And_Words)    
    return Modified_Sentences_And_Words


def modify_key_words_5_ways_readTag_invalid_v2(indices,sentence):
    Words_In_Sentence = sentence.split()
    selected_word_list = [Words_In_Sentence[i] for i in indices]
    selected_word_list = list(set(selected_word_list)) # unique
    Modified_Sentences = modify_one_word_5_ways_invalid_v2(sentence, selected_word_list)
    #print(Modified_Sentences)
    Modified_Sentences_And_Words = []
    for i in range(len(selected_word_list)):
        try:
            Modified_Sentences_And_Words.append([Modified_Sentences[i][0], Modified_Sentences[i][1], selected_word_list[i], Modified_Sentences[i][3]])
        except:
            print('len(Modified_Sentences) < 4:',i)
    #print(Modified_Sentences_And_Words)    
    return Modified_Sentences_And_Words


def modify_key_words_5_ways_readTag_invalid_v2_force_method(indices,sentence, method):
    Words_In_Sentence = sentence.split()
    selected_word_list = [Words_In_Sentence[i] for i in indices]
    selected_word_list = list(set(selected_word_list)) # unique
    Modified_Sentences = modify_one_word_5_ways_invalid_v2_force_method(sentence, selected_word_list, method)
    #print(Modified_Sentences)
    Modified_Sentences_And_Words = []
    for i in range(len(selected_word_list)):
        try:
            Modified_Sentences_And_Words.append([Modified_Sentences[i][0], Modified_Sentences[i][1], selected_word_list[i], Modified_Sentences[i][3]])
        except:
            print('len(Modified_Sentences) < 4:',i)
    #print(Modified_Sentences_And_Words)    
    return Modified_Sentences_And_Words
    
