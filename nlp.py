import random
from collections import Counter

class biKey:
    def __init__(self, firstString, secondString):
        self.first = firstString
        self.second = secondString

    def __eq__(self, other):
        return self.first == other.first and self.second == other.second

    def __hash__(self):
        res = hash(self.first)*1000000
        res += hash(self.second)
        return res

    def __str__(self):
        return '['+ self.first+ ' '+ self.second + ']'

def uniTrain(line):
    global uniSet
    if '<s>' in uniSet:
        uniSet['<s>'] += 1
    else:

        uniSet['<s>'] = 1
    for string in line:
        if string in uniSet:
            uniSet[string] += 1
        else:
            uniSet[unk] += 1
            uniSet[string] = 1
    if '</s>' in uniSet:
        biSet['</s>'] += 1
    else:
        biSet['</s>'] = 1

def biTrain(line):
    global biSet
    afterUnk = False
    if '<s>' in biSet:
        biSet['<s>'].append(line[0])
    else:
        biSet['<s>'] = [line[0]]
    for i in range(len(line) - 1):
        if line[i] in biSet:
            biSet[line[i]].append(line[i + 1])
            #afterUnk = False
        else:
            biSet[unk].append(line[i + 1])
            biSet[line[i]] = [line[i + 1]]
            #afterUnk = True

    if line[-1] in biSet:
        biSet[line[-1]].append('</s>')
    else:
        biSet[unk].append('</s>')
        biSet[line[-1]] = ['</s>']

def triTrain(line):
    if line[0] in tbiset:
        first = biKey('<s>',line[0])
    else:
        first = biKey('<s>',unk)
        tbiset[unk] = []
    if first in triSet:
        triSet[first].append(line[1])
    else:
        triSet[first] = [line[1]]
    for i in range(len(line) - 2):
        if line[i] in tbiset:
            fl = line[i]
        else:
            tbiset[line[i]] = []
            fl = unk
        if line[i+1] in tbiset:
            sl = line[i+1]
        else:
            tbiset[line[i+1]] = []
            sl = unk

        tmpKey = biKey(fl, sl)
        if tmpKey in triSet:
            triSet[tmpKey].append(line[i+2])
        else:
            triSet[tmpKey] = [line[i+2]]
    if line[-2] in tbiset:
        tmpKey = biKey(line[-2], line[-1])
    if tmpKey in triSet:
        triSet[tmpKey].append('</s>')
    else:
        triSet[tmpKey] = ['</s>']

def random_line(fname):
    rndList = []
    for i in range(test_file_lines):
        rndList.append(i)
    random.shuffle(rndList)
    rndLines = []
    with open(fname, encoding='utf8') as fp:
        for i, line in enumerate(fp):
            if i in rndList[0:100]:
                rndLines.append(line)
    fp.close()
    return rndLines

def calculateUnigram():
    maxi = 0.0
    item = 'a'
    count = 0.0
    for l in uniSet:
        count += uniSet[l]
        if uniSet[l] > maxi:
            maxi = uniSet[l]
            item = l
    return [item, maxi/count]

def calculateBigram(line):
    for i in range(len(line)):
        if line[i] == '$':
            ind = i
            break
    if line[ind - 1] not in biSet:
        first = biSet[unk]
        Cfirst = uniSet[unk]
    else:
        first = biSet[line[ind - 1]]
        Cfirst = uniSet[line[ind - 1]]
    count = 0
    data = Counter(first)
    get_mode = dict(data)
    mode = [k for k, v in get_mode.items() if v == max(list(data.values()))]
    counter = 0
    for f in first:
        if f == mode[0]:
            counter += 1

    return [mode[0],counter/Cfirst]

def calculateTrigram(line):
    for i in range(len(line)):
        if line[i] == '$':
            ind = i
            break
    if i < 1:
        return [unk, 0]
    elif i == 1:
        fl = unk
        if line[0] in tbiset:
            sl = line[0]
        else:
            sl = unk
    else:
        if line[ind - 2] in tbiset:
            fl = line[ind - 2]
        else:
            fl = unk
        if line[ind - 1] in tbiset:
            sl = line[ind-1]
        else:
            sl = unk

    testBikey = biKey(fl, sl)
    # options = triSet[testBikey]
    maxi = 0
    item = ''
    if testBikey not in triSet:
        return [unk, 0]

    for tb in triSet[testBikey]:
        res = l3*findPTri(testBikey,tb) + l2*findPBi(fl,sl) + l1*findPUni(sl)
        if maxi < res:
            maxi = res
            item = tb
    return [item, maxi]

def findPUni(string):
    total = 0.0
    for u in uniSet:
        total += uniSet[u]
    return uniSet[string]/total

def findPBi(first, second):
    fCount = uniSet[first]
    count = 0.0
    for item in biSet[first]:
        if item == second:
            count += 1
    return count/fCount

def findPTri(inBikey, after):
    cFirst = 0.0
    for item in biSet[inBikey.first]:
        if item == inBikey.second:
            cFirst += 1
    cSecond = 0.0
    if inBikey not in triSet:
        return 0
    for item in triSet[inBikey]:
        if item == after:
            cSecond += 1
    if cFirst == 0:
        return 0
    return cSecond/cFirst



def makeKnown(line):
    for word in range(int(len(line)/(1.5))):
        uniSet[word] = 0
        biSet[word] = []
        tbiset[word] = []
    uniSet[unk] = 0
    biSet[unk] = []
    tbiset[unk] = []

l3 = 0.0
l2 = 1
l1 = 0.0
unk = '<UNK>'
uniSet = {}
biSet = {}
tbiset = {}
triSet = {}
test_file_lines = 306681
number_of_tests = 100

f = open('train_v2.txt', 'r')
training = []
for i in range(500):
    newLine = f.readline()
    #print(newLine)
    newLine = newLine.replace('\n','')
    training.append(newLine.split(' '))

    makeKnown(newLine.split(' '))
    biTrain(newLine.split(' '))
    uniTrain(newLine.split(' '))
    triTrain(newLine.split(' '))

print('Train data read successfully')
f.close()

f = open('labels.txt', 'r')
ans = []
for i in range(80):
    line = f.readline()
    line = line.replace('\n','')
    sLine = line.split(' ')
    ans.append(sLine[1])
f.close()


#read from file
f = open('test_v2.txt', 'r', encoding='utf8')
f.readline()
correct = 0
unkNumbers = 0

for i in range(80):
    testLine = f.readline()
    splitTestLine = testLine.split(' ')
    uniAnswer = calculateUnigram()
    biAnswer = calculateBigram(splitTestLine)
    triAnswer = calculateTrigram(splitTestLine)
    bestAnswer = max(uniAnswer[1], biAnswer[1], triAnswer[1])
    if bestAnswer == uniAnswer[1]:
        tempAnswer = uniAnswer
    elif bestAnswer == biAnswer[1]:
        tempAnswer = biAnswer
    else:
        tempAnswer = triAnswer

    if tempAnswer[0] == ans[i]:
        correct += 1

    print("predicted:[", tempAnswer[0], "], answer[", ans[i],"]")
f.close()
print("accuracy is "+str(correct/80*100) + "%")
#print(unkNumbers)
#print(random_line('test_v2.txt'))
