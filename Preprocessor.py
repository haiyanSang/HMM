import Util
import re


class preprocessor():
    def __init__(self, fp, tag_fp, train_fp, test_fp):
        self.tagDic = {}
        self.filePath = fp
        self.tagFilePath = tag_fp
        self.trainFilePath = train_fp
        self.testFilePath = test_fp

    def segSentences(self, line, sentenceTags):
        lines = []
        startIndex = 0
        endIndex = 0
        for endIndex in range(len(line)):
            if sentenceTags.__contains__(line[endIndex]):
                endIndex += 2
                if len(line) - endIndex < 7:
                    ll = line[startIndex:]
                    lines.append(ll)
                    endIndex = len(line) + 1
                    startIndex = endIndex
                else:
                    ll = line[startIndex:endIndex + 1]
                    lines.append(ll)
                    startIndex = endIndex + 1
        # if there's no sentence split tag, add the line.
        if endIndex > startIndex + 1:
            ll = line[startIndex:]
            lines.append(ll)

        return lines

    # Get rid of the punctuations and its tag /w
    # def stem(self, line):
        # l = re.sub('[●\s+-\.\!\/_,$%^*(\"\'—！，。“”’‘？?、~@#￥…&（）》《；：\)【】]{0,1}/w', '', line)
        # return l
    # n means n-fold, split data in n parts. i means different method of splitting. i locate in [0, n)
    def generateData(self, n=10, i=0):
        trainFile = open(self.trainFilePath,"w")
        testFile = open(self.testFilePath,"w")
        sentenceTags=['。','?','？','！','!']
        file=open(self.filePath)
        num=0
        while 1:
            line = file.readline().strip("\n")
            # Take the punctuation or not
            # line = self.stem(line)
            if not line:
                break
            lines=self.segSentences(line,sentenceTags)
            for ll in lines:
                words,tags=Util.seprateWordsAndTags(ll)
                if tags.__contains__(''):
                    continue
                for tag in tags:
                    if self.tagDic.__contains__(tag):
                        continue
                    else:
                        self.tagDic[tag]=1
                num = num +1
                # n-fold
                if num % n == i:
                    testFile.write(ll+"\n")
                else:
                    #testFile.write(ll + "\n")
                    trainFile.write(ll+"\n")
        file.close()
        print(self.tagDic.keys())

        trainFile.close()
        testFile.close()

        resultFile=open(self.tagFilePath, "w")
        result=""
        for key in self.tagDic.keys():
            result+="\'"+key + "\'"+ ","
        resultFile.write(result)
        resultFile.close()
        print("The game is over!")
