import Util

#
def segSentences(line,sentenceTags):
    lines=[]
    startIndex=0
    endIndex=0

    for endIndex in range(len(line)):
        if sentenceTags.__contains__(line[endIndex]):
            endIndex+=2
            if len(line)-endIndex<7:
                ll=line[startIndex:]
                lines.append(ll)
                endIndex=len(line)+1
                startIndex=endIndex
            else:
                ll=line[startIndex:endIndex+1]
                lines.append(ll)
                startIndex=endIndex+1
    # if there's no sentence split tag, add the line.
    if endIndex>startIndex+1:
        ll=line[startIndex:]
        lines.append(ll)

    return lines



tagDic={}

filePath= "data/ori_data.txt"
tagFilePath = "data/tags.txt"

trainFilePath = "data/train.txt"
testFilePath = "data/test.txt"
trainFile = open(trainFilePath,"w")
testFile = open(testFilePath,"w")
sentenceTags=['。','?','？','！','!']
file=open(filePath)
num=0
while 1:
    line = file.readline().strip("\n")
    if not line:
        break
    lines=segSentences(line,sentenceTags)

    for ll in lines:
        words,tags=Util.seprateWordsAndTags(ll)
        if tags.__contains__(''):
            continue

        for tag in tags:
            if tagDic.__contains__(tag):
                continue
            else:
                tagDic[tag]=1

        num = num +1
        if num % 10 == 0:
            testFile.write(ll+"\n")
        else:
            trainFile.write(ll+"\n")

        # if ll.__contains__(" "):
        #     word_tags=ll.split(" ")
        #     for word_tag in word_tags:
        #
        #         if word_tag.__contains__("/"):
        #             wt=word_tag.split("/")
        #             if len(wt)>2:
        #                 tag=wt[len(wt)-1]
        #             else:
        #                 tag=wt[1]
        #             if tag == '':
        #                 print(ll)
        #             if tag.__contains__("\\"):
        #                 print(word_tag)
        #             if tagDic.__contains__(tag):
        #                 continue
        #             else:
        #                 tagDic[tag]=1
file.close()
print(tagDic.keys())

trainFile.close()
testFile.close()

resultFile=open(tagFilePath, "w")
result=""
for key in tagDic.keys():
    result+="\'"+key + "\'"+ ","
resultFile.write(result)
resultFile.close()
print("The game is over!")