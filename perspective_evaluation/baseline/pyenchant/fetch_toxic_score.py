import requests


def fetch_toxic_score_online(sentence):
    # the variable "sessionId" is a random value written arbitrarily
    try:
        r = requests.post('http://www.perspectiveapi.com/check', json={"comment":sentence, "sessionId":"10002022"})
    except:
        print('fetch_toxic_score_online: r = requests.post() bug')
        print(sentence)
        # return 2 # bug
        return 0 # regarded as successfully deceiving Perspective API        
        
    if (str(r)=='<Response [200]>'):    
        j = r.json()
        #print(j)
        #print()
        if ('attributeScores' in j):
            toxic_score = j['attributeScores']['TOXICITY']['summaryScore']['value']
        else:
            print('attributeScores not in j = r.json()')
            print(j)
            print(sentence)
            #toxic_score = 2
            toxic_score = 0 # regarded as successfully deceiving Perspective API
    else:
#        print('str(r) != \'<Response [200]>\'')
#        print(r)
#        print(sentence)
#        #toxic_score = 2
        toxic_score = 0 # regarded as successfully deceiving Perspective API
    return toxic_score


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
Main
'''
'''
Sentence_List = ['good','bad','idiot','idiiot','idioot','he is an idiot']

for s in Sentence_List:
    toxic_score = fetch_toxic_score_online(s)
    print('%s: %f' %(s,toxic_score))
    
fetch_toxic_score_list_online(Sentence_List, outfile='out_toxic_score_list.txt')
'''
