#!/usr/bin/python
#-*-coding:utf-8
import sys
import Util
import pickle
import time
from Preprocessor import preprocessor
state_M = 4
word_N = 0
current_time = time.strftime("%Y-%m-%d", time.localtime())
A_dic = {} # Transfer dict
B_dic = {} # Emission dict
Count_dic = {}
Pi_dic = {} # Initial dict
word_set = set()
state_list = ['n','nhd','ns','nr2','p','nzit','al','nz','ngis','uyy','ng','nisb',
              'nzmc','ntu','tg','j','vf','nmc','ngo','gb','nnt','q','vn','nt','uzhi','vd',
              'dl','t','f','usuo','rzv','an','vg','c','gg','uzhe','nsff','nto','r','aghm',
              'rzs','vyou','bl','ntc','k','ntcb','pbei','ule','vis','Mg','qt','nis','nzhm',
              'nito','nisis','udh','a','nff','nu','qo','ude2','ulian','vi','nisu','gm','qv',
              'nba','z','uls','ag','niso','ngf','ude1','qf','dg','nmcmc','m','ry','e','nh','y',
              'uguo','na','vit','no','pba','ad','rz','nnd','nso','w','u','gi','nrf','nr1','gc','gp',
              'nf','bo','vl','o','i','nsf','nish','nhmhm','d','nitu','usuois','rzt','gcmc','niss',
              'cc','b','nr','vshi','nrff','v','nnto','mq','x','rr','rys','nisit','nisf','s','ude3',
              'Rg','ryt','nrj','nmchm','nit','agf','gbmc','udeng','nzf','nitit','vx','ryv','qhm','nhm','l']
line_num = 0

PROB_START = "model/prob_start"
PROB_EMIT = "model/prob_emit"
PROB_TRANS = "model/prob_trans"
PROB_TAGS = "model/prob_tags"

def init():
    global state_M
    global word_N
    state_M=len(state_list) # Number of tags
    word_N=len(word_set) # Number of vocab

    # Initialize all the dict into prob 0
    for state in state_list:
        A_dic[state] = {}
        for state1 in state_list:
            A_dic[state][state1] = 0.0
    for state in state_list:
        Pi_dic[state] = 0.0
        B_dic[state] = {}
        # Smoothing
        Count_dic[state] = 0

def SaveModel():
    start_fp = open(PROB_START,'wb')
    emit_fp = open(PROB_EMIT,'wb')
    trans_fp = open(PROB_TRANS,'wb')
    tags_fp = open(PROB_TAGS,'wb')

    print ("len(word_set) = %s " % (len(word_set)))
    for key in Pi_dic:
        '''
        if Pi_dic[key] != 0:
            Pi_dic[key] = -1*math.log(Pi_dic[key] * 1.0 / line_num)
        else:
            Pi_dic[key] = 0
        '''
        Pi_dic[key] = Pi_dic[key] * 1.0 / line_num
    # Save the initial matrix
    pickle.dump(Pi_dic,start_fp)

    for key in A_dic:
        for key1 in A_dic[key]:
            '''
            if A_dic[key][key1] != 0:
                A_dic[key][key1] = -1*math.log(A_dic[key][key1] / Count_dic[key])
            else:
                A_dic[key][key1] = 0
            '''
            if A_dic[key][key1] != 0 and Count_dic[key] > 0:
                A_dic[key][key1] = float(A_dic[key][key1]) / Count_dic[key]
            else:
                A_dic[key][key1] = 0
            # A_dic[key][key1] = A_dic[key][key1] / Count_dic[key]
    # Save the transfer matrix
    pickle.dump(A_dic,trans_fp)
    for key in B_dic:
        for word in word_set:
            '''
            if B_dic[key][word] != 0:
                B_dic[key][word] = -1*math.log(B_dic[key][word] / Count_dic[key])
            else:
                B_dic[key][word] = 0
            '''
            if B_dic[key].get(word) and Count_dic[key] > 0:
                    B_dic[key][word] = float(B_dic[key][word])/ Count_dic[key]
            else:
                B_dic[key][word] = 0
            # B_dic[key][word] = B_dic[key][word] / Count_dic[key]
    # Save the emit matrix
    pickle.dump(B_dic,emit_fp)
    # Save the tag frequency dic
    total_count_tags = sum(Count_dic.values())
    prob_tag = {}
    for key in Count_dic:
        prob_tag[key] = float(Count_dic[key])/total_count_tags
    print(prob_tag)
    pickle.dump(prob_tag, tags_fp)
    start_fp.close()
    emit_fp.close()
    trans_fp.close()


def main_1(trainFilePath):
    # if len(sys.argv) != 2:
    #     print ("Usage [%s] [input_data] " % (sys.argv[0]))
    #     sys.exit(0)
    inputFile = open(trainFilePath)
    init()
    global word_set
    global line_num # initialized as 0
    while 1:
        line = inputFile.readline()
        if not line:
            break
        line_num += 1
        if line_num % 1000 == 0:
            print (line_num)
        # if line_num >2:
        #     break
        line = line.strip()

        if not line:
            continue
        # words and tags for the current line
        word_list,tag_list=Util.seprateWordsAndTags(line)
        # Build the word set
        word_set = word_set | set(word_list)
        for i in range(len(tag_list)):
            if i == 0:
                # Update initial matrix
                Pi_dic[tag_list[0]] += 1
                # Update the state count
                Count_dic[tag_list[0]] += 1
            else:
                # Update transfer matrix
                A_dic[tag_list[i - 1]][tag_list[i]] += 1
                # Update the state count
                Count_dic[tag_list[i]] += 1
                if not B_dic[tag_list[i]].get(word_list[i]):
                    # initial the emit matrix
                    B_dic[tag_list[i]][word_list[i]] = 1
                else:
                    B_dic[tag_list[i]][word_list[i]] += 1

    SaveModel()
    inputFile.close()

if __name__ == "__main__":
    p = preprocessor("data/ori_data.txt", "data/tags.txt", "data/train.txt", "data/test.txt")
    p.generateData(10, 5)
    main_1("data/train.txt")
