

PROB_START = "model/prob_start"
PROB_EMIT = "model/prob_emit"
PROB_TRANS = "model/prob_trans"

def seprateWordsAndTags(line):
    word_list=[]
    tag_list=[]
    line = line.strip()
    if line.__contains__(" "):
        word_tags=line.split(" ")
        for word_tag in word_tags:
            if word_tag.__contains__("/"):
                wt=word_tag.split("/")
                tag=wt[len(wt)-1]
                word="/".join(wt[0:len(wt)-1])
                word_list.append(word)
                tag_list.append(tag)
    else:
        word_tag = line
        if word_tag.__contains__("/"):
            wt = word_tag.split("/")
            tag = wt[len(wt) - 1]
            word = "/".join(wt[0:len(wt) - 1])
            word_list.append(word)
            tag_list.append(tag)

    return word_list,tag_list

# testFilePath="data/test.txt"
#
# testFile=open(testFilePath)
# testNum=1000
# while 1:
#     line = testFile.readline()
#     if not line:
#         break
#     testNum-=1
#     if testNum<0:
#         break
#     words,tags=seprateWordsAndTags(line)
#     if len(words) != len(tags):
#         print(words)
#         print(tags)