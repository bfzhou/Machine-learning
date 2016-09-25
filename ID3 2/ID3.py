import math
import csv
import types
import random


def classify(classList):
    '''''
    find the most in the set
    '''
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    # print(classCount)
    # return list(classCount.keys());
    return sorted(classCount)[0]


# print(classify(classList))

def classifyRow(row):
    rowDict = {}
    for e in row:
        if not rowDict.__contains__(e):
            rowDict[e] = 0
        rowDict[e] += 1
    # print(rowDict)
    return rowDict


def loadCSV(filename):
    """load CSV files and ouput is a list with all the instance, header and dimention of a instance"""
    testList = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        header = reader.__next__()
        # dim = len(header)
        for row in reader:
            testList.append(row)
    return testList, header


def randomSplit(dataSet, percent):
    if percent > 1 or percent < 0:
        percent = 0.5
    length = len(dataSet)
    partA = [i for i in range(length)]
    partB = []
    while len(partB) / length < percent:
        e = random.randint(0, length - 1)
        if e not in partB:
            partB.append(e)
            partA.remove(e)

    dataSetA = [dataSet[i] for i in partA]
    dataSetB = [dataSet[i] for i in partB]
    return dataSetA, dataSetB
    # return partA, partB


inputData, header = loadCSV('wine.csv')
trainData, testData = randomSplit(inputData, 0.5)
train, valid = randomSplit(trainData, 0.7)

testsize = len(testData)
trainsize = len(train)
validsize = len(valid)

headerLen = len(header)
print('testsize:', testsize, 'trainsize:', trainsize, 'validsize:', validsize)


def transpose(test1):
    global header
    dim1 = len(test1)
    dim2 = len(header)
    test2 = []
    for j in range(dim2):
        column = []
        for i in range(dim1):
            e = test1[i][j]
            column.append(e)
        test2.append(column)
    return test2


train2 = transpose(train)


# decision=list(classifyRow(train2[-1]).keys())




def splitDataSet(dataSet, index, value):
    retDataSet = []
    Vec = dataSet[index]
    for j in range(len(dataSet)):
        if j != index:
            row = dataSet[j]
            reducedVec = []
            for i in range(len(Vec)):
                if Vec[i] == value:
                    reducedVec.append(row[i])
            retDataSet.append(reducedVec)
    return retDataSet


def indexGen(dataSet):
    Num = len(dataSet[-1])
    minEntropy = 0
    index = 0
    for i in range(len(dataSet) - 1):
        row = dataSet[i]
        entropy = 0
        # print('row')
        # print(row)
        rowDict = classifyRow(row)
        # print('rowDict')
        # print(rowDict)
        for dic in rowDict:
            # print (rowDict[dic])
            dicDecision = []
            for j in range(len(row)):
                if row[j] == dic:
                    dicDecision.append(dataSet[-1][j])
            decDict = classifyRow(dicDecision)
            rowNum = rowDict[dic]
            # print('decision Dic')
            # print(decDict)

            for dec in decDict:
                entropy += decDict.get(dec) / Num * math.log2(decDict.get(dec) / rowNum)
        if i == 0:
            minEntropy = entropy
        if entropy > minEntropy:
            minEntropy = entropy
            index = i
    # print('entro:')
    #     print(entropy)
    # print('minimum entropy')
    # print(minEntropy)
    # print(index)

    return index


def treeGen(data, feature):
    # use transposed test2
    result = set(data[-1])
    if len(result) == 1:
        return data[-1][-1]
    if len(data) == 1:
        return classify(data[-1])
    # index=random.randint(0,len(data)-1)
    index = indexGen(data)
    # label=int(feature[index])
    label = feature[index]
    tree = {label: {}}

    valueSet = set(data[index])
    # print(valueSet)
    for value in valueSet:
        subData = splitDataSet(data, index, value)
        # print('label',label,'value',value)
        # print('subData:')
        # print(subData)
        subfeature = list(feature)
        del (subfeature[index])
        tree[label][value] = treeGen(subData, subfeature)
    return tree


gPath = []
gPathDec = []
gDec = []


def ConvTree(tree, path, pathDec, level):
    global gpath, gPathDec, gDec
    if len(tree) == 1:

        node = tree[list(tree.keys())[0]]

        for branch in node:
            # print('branch:',branch)
            # print(node[branch])
            # print('node:',list(tree.keys()))
            xrule = []
            xpathDec = []
            xpath = path.copy()
            xpathDec = pathDec.copy()
            # xrule[list(tree.keys())[0]]=branch
            xpath.append(list(tree.keys())[0])
            xpathDec.append(branch)

            if not type(node[branch]) == type(str()):
                line = '|\t' * level
                line += str(list(tree.keys())[0])
                line += ':--'
                line += str(branch)
                # line+='-->'
                print(line)
                ConvTree(node[branch], xpath, xpathDec, level + 1)
            else:
                # print(xpath)
                # print(xpathDec)
                # print('|\t' * level, '(',list(tree.keys())[0], '):--', branch, '-->','decision', node[branch])
                line = '|\t' * level
                line += str(list(tree.keys())[0])
                line += ':--'
                line += str(branch)
                line += '-->'
                line += 'decision:'
                line += str(node[branch])
                print(line)
                gPath.append(xpath)
                gPathDec.append(xpathDec)
                gDec.append(node[branch])

    return 0


def treeError(path, pathDec, dec, data):
    # use unchanged input data
    global header
    results = [0 for i in range(len(data))]
    for i in range(len(data)):
        row = data[i]
        for j in range(len(path)):
            rule = path[j]
            ruleResult = True

            for k in range(len(rule)):
                ruleNode = rule[k]
                if ruleNode in header:
                    index = header.index(ruleNode)
                    # print(pathDec[j][k],row[index])
                    ruleResult = ruleResult and (pathDec[j][k] == row[index])

            if (ruleResult):
                results[i] = dec[j]
    dataDec = [ex[-1] for ex in data]
    mode = classify(dataDec)
    # print('mode:',mode)
    error = 0
    for k in range(len(results)):
        e = results[k]
        if e == 0:
            e = mode
        if e != dataDec[k]:
            error += 1
    return error / len(data)


print('header:')
print(header)
tree = treeGen(train2, header)

print('\n' * 3)
print('tree list:')
print(tree)
print('\n' * 3)
print('tree:')
# path=[]
# pathDec=[]
ConvTree(tree, [], [], 0)
print('\n' * 3)
print(gPath)
print(gPathDec)
print(gDec)


# indexGen(test2)

def rulePrint(xpath, xpathDec, xdec):
    for i in range(len(xpath)):
        row = xpath[i]
        rule = 'if '
        for j in range(len(row) - 1):
            rule += '(' + xpath[i][j] + '=' + xpathDec[i][j] + ')&'
        if len(row) - 1 >= 0:
            rule += '(' + xpath[i][-1] + '=' + xpathDec[i][-1] + ')'
        rule += '\tthen ' + xdec[i]
        print(rule)
    return 0


print('\nerror before rule pruning:')
xerror = treeError(gPath, gPathDec, gDec, testData)
print('error:', xerror)
print('\n' * 3)
print('rules before rule pruning')
rulePrint(gPath, gPathDec, gDec)

error = treeError(gPath, gPathDec, gDec, valid)


def treeCut(gPath, gPathDec, gDec, testData):
    global error
    for i in range(len(gPath)):
        row = gPath[i]
        for j in range(len(row)):
            temp = gPath[i][j]
            gPath[i][j] = 'mark'
            xerror = treeError(gPath, gPathDec, gDec, testData)
            if xerror < error:
                error = xerror
            else:
                gPath[i][j] = temp

    xpath = []
    xpathDec = []
    xdec = []
    for i in range(len(gPath)):
        row = gPath[i]
        xrow = []
        xdecrow = []
        for j in range(len(row)):
            temp = gPath[i][j]
            if temp != 'mark':
                xrow.append(temp)
                xdecrow.append(gPathDec[i][j])
        if xrow != []:
            xpath.append(xrow)
            xpathDec.append(xdecrow)
            xdec.append(gDec[i])
    return xpath, xpathDec, xdec


xpath, xpathDec, xdec = treeCut(gPath, gPathDec, gDec, valid)
print('\n' * 3)
print(xpath)
print(xpathDec)
print(xdec)
print('\nerror after rule pruning')
xerror = treeError(xpath, xpathDec, xdec, testData)
print('error:', xerror)

print('\n' * 3)
print('rules after rule pruning')
rulePrint(xpath, xpathDec, xdec)
