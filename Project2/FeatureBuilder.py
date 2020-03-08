from nltk.classify import MaxentClassifier

def trans_dic(words):
    return {word:True for word in words}

def loadTrainData(filePath):
    trainTokenList = []
    file = open(filePath, "r")
    for line in file.readlines():
        line = line.rstrip("\n")
        if line!="":
            token=line.split("\t")
            trainTokenList.append(token)
    return trainTokenList

def loadTestData(filePath):
    testokenList = []
    file = open(filePath, "r")
    for line in file.readlines():
        line = line.rstrip("\n")
        if line != "":
            token = line.split("\t")
            testokenList.append(token)
        else:
            testokenList.append("")
    return testokenList

def create_trainToks(tokenList):
    # type train_toks: list
    # param train_toks: Training data, represented as a list of
    # pairs, the first member of which is a featureset,
    # and the second of which is a classification label.
    trainToks = []
    for token in tokenList:
        tokenName,tokenPOS,tokenBIO,tokenLabel = token[0],token[1],token[2],token[3]
        featureset = [tokenName,tokenPOS,tokenBIO]
        trainToks.append((trans_dic(featureset),tokenLabel))
    return trainToks


def create_testFeatureSet(testokenList):
    # type train_toks: list
    # param train_toks: Training data, represented as a list of
    # pairs, the first member of which is a featureset,
    # and the second of which is a classification label.
    testFratureSet = []
    for token in testokenList:
        if token!="":
            tokenName,tokenPOS,tokenBIO = token[0],token[1],token[2]
            featureset = [tokenName,tokenPOS,tokenBIO]
            testFratureSet.append(trans_dic(featureset))
        else:
            testFratureSet.append("")
    return testFratureSet



if __name__ == "__main__":
    trainfilePath = "Test/CONLL_train.pos-chunk-name"
    testfilePath = "Test/CONLL_dev.pos-chunk"
    trainTokenList = loadTrainData(trainfilePath)
    testokenList = loadTestData(testfilePath)
    trainToks = create_trainToks(trainTokenList)
    testFratureSet = create_testFeatureSet(testokenList)
    model = MaxentClassifier.train(trainToks)

    labels = []
    for feature in testFratureSet:
        if feature!="":
            label = model.classify(feature)
            labels.append((list(feature.keys())[0],label))
        else:
            labels.append("")
    print("success")
