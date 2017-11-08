#!/usr/bin/python
#-*-coding:utf-8
import pickle
import Util
import math

def load_model(f_name):
    ifp = open(f_name, 'rb')
    return pickle.load(ifp)

prob_start = load_model("model/prob_start")
prob_trans = load_model("model/prob_trans")
prob_emit = load_model("model/prob_emit")

def viterbi(obs, states, start_p, trans_p, emit_p) :
    offset = 0.8
    V = [{}] #tabular
    path = {}
    obs=obs.split(" ")
    for y in states:
        if emit_p[y].get(obs[0]):
            V[0][y] = start_p[y] * (emit_p[y].get(obs[0]))
        else:
            V[0][y] = start_p[y] * (emit_p[y].get(obs[0], 0.0000001))
        # V[0][y] = math.log(start_p[y]) + math.log(emit_p[y].get(obs[0],0.00000001))
        # print(y)
        # print(V[0][y])
        path[y] = [y]
    for t in range(1,len(obs)):
        V.append({})
        newpath = {}
        for y in states:
            try:
                (prob, state) = max([(V[t-1][y0] * trans_p[y0].get(y,0.0000001) * emit_p[y].get(obs[t],0.000001) ,y0) for y0 in states])
                # (prob, state) = min([-math.log(V[t - 1][y0] - math.log(trans_p[y0].get(y, 0.00000001)) -math.log(emit_p[y].get(obs[t], 0.00000001)), -math.log(y0)) for y0 in states if V[t - 1][y0] > 0])
            except:
                print("XXXXXXXXXXXXXXXXXXXXXXX:",V)
                print("y:",y,"obs:",obs[t])
                print("V[t-1]:",V[t-1])
                raise Exception("max arg is empty",)
            V[t][y] =prob
            newpath[y] = path[state] + [y]
        path = newpath
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def prediction(sentence):
    try:
        prob, pos_list =  viterbi(sentence,('n','nhd','ns','nr','p','nzit','al','nz','ngis','uyy','ng','nisb','nzmc','ntu','tg','j','vf','nmc','ngo','gb','nnt','q','vn','nt','uzhi','vd','dl','t','f','usuo','rzv','an','vg','c','gg','uzhe','nsff','nto','r','aghm','rzs','vyou','bl','ntc','k','ntcb','pbei','ule','vis','Mg','qt','nis','nzhm','nito','nisis','udh','a','nff','nu','qo','ude2','ulian','vi','nisu','gm','qv','nba','z','uls','ag','niso','ngf','ude1','qf','dg','nmcmc','m','ry','e','nh','y','uguo','na','vit','no','pba','ad','rz','nnd','nso','w','u','gi','nrf','nr1','gc','gp','nf','bo','vl','o','i','nsf','nish','nhmhm','d','nitu','usuois','rzt','gcmc','niss','cc','b','nr','vshi','nrff','v','nnto','mq','x','rr','rys','nisit','nisf','s','ude3','Rg','ryt','nrj','nmchm','nit','agf','gbmc','udeng','nzf','nitit','vx','ryv','qhm','nhm','l'), prob_start, prob_trans, prob_emit)
    except:
        raise Exception("get an error when prediction.")
    return (prob,pos_list)



def validate():
    testRecordFilePath="data/testRecord.txt"
    testRecordFile=open(testRecordFilePath,"w")
    testFilePath="data/test.txt"
    testFile=open(testFilePath)
    line_sum=0
    words_count=0
    right=0
    while 1:
        line = testFile.readline()
        line_sum+=1
        if not line:
            break
        if line_sum>100:
            break
        line=line.strip()

        words,tags=Util.seprateWordsAndTags(line)
        inputstr=" ".join(words)
        try:
            prob,predicteTags=prediction(inputstr)
        except:
            print("ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,")
            # print("PredicTags:", predicteTags)
            # print("tags:", tags)
            print(line)
        if len(predicteTags) !=len(tags):
            words_count+=len(tags)
            print("-----------------------------------------------------------------")
            print("PredicTags:",predicteTags)
            print("tags:",tags)
            print(line)
        else:
            testRecordFile.write("--------------------------------------------------------\n")
            testRecordFile.write(line+"\n")
            testRecordFile.write("tags:"+str(tags)+"\n")
            testRecordFile.write("PredicTags:"+str(predicteTags)+"\n")

            for i in range(len(predicteTags)-1):
                words_count+=1
                if predicteTags[i]==tags[i]:
                    right+=1

    correct_rate=right*1.0/words_count

    print("测试语料:%d行，总词数:%d,正确标注总数:%d,正确率:%.4f"%(line_sum,words_count,right,correct_rate))

'''def test():
    test_str = u"长春 市长 春节 讲话。"
    prob, pos_list = prediction(test_str)
    print(test_str)
    print(pos_list)
    test_str = u"他 说 的 确实 在理."
    prob, pos_list = prediction(test_str)
    print(test_str)
    print(pos_list)

    test_str = u"毛主席 万岁。"
    prob, pos_list = prediction(test_str)
    print(test_str)
    print(pos_list)

    test_str = u"我 有 一台 电脑。"
    prob, pos_list = prediction(test_str)
    print(test_str)
    print(pos_list)'''


if __name__ == "__main__":
    # test()
    validate()