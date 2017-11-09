import time
import pickle
current_time = time.strftime("%Y-%m-%d", time.localtime())
file1 = open('data/unk_words.txt')
file2 = open('data/unk.txt', 'w')
item = file1.readlines()[0].split(' ')
j = []
for index, i in enumerate(item):
    if index == 0:
        j.append(i)
    else:
        if index % 2 == 1:
            j.append(i + ' ' + (item[index+1]))
        else:
            continue
'''
def load_model(f_name):
    ifp = open(f_name, 'rb')
    return pickle.load(ifp)
prob_start = load_model("model/prob_start")
prob_trans = load_model("model/prob_trans")
prob_emit = load_model("model/prob_emit")
prob_tags = load_model("model/prob_tags")
print(prob_start['z'])
print(max(prob_start.values()))
'''
import re
from Preprocessor import preprocessor
a = '\'/w 你好啊 \'/w asda'
print(re.sub('[\s+\.\!\/_,$%^*(\"\'—！，。“”’‘？?、~@#￥…&（）]{1}/w', '', a))
p = preprocessor("testdata/ori_data.txt", "testdata/tags.txt", "testdata/train.txt", "testdata/test.txt")
p.generateData(10, 1)