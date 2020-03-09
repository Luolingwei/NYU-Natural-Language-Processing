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
    for i,token in enumerate(tokenList):
        # add prior state
        tokenName,tokenPOS,tokenBIO,tokenLabel,prevWord,prevPOS,prevLabel = token[0],token[1],token[2],token[3],'prev_'+tokenList[max(0,i-1)][0],'prev_'+tokenList[max(0,i-1)][1],'prev_'+tokenList[max(0,i-1)][3]
        featureset = [tokenName,tokenPOS]
        trainToks.append((trans_dic(featureset),tokenLabel))
    return trainToks


def create_testFeatureSet(testokenList):
    # type train_toks: list
    # param train_toks: Training data, represented as a list of
    # pairs, the first member of which is a featureset,
    # and the second of which is a classification label.
    testFratureSet = []
    for i,token in enumerate(testokenList):
        if token!="":
            tokenName,tokenPOS,tokenBIO = token[0],token[1],token[2]
            featureset = [tokenName,tokenPOS]
            testFratureSet.append(featureset)
        else:
            testFratureSet.append("")
    return testFratureSet


def predict(model,testFratureSet):

    labels = []
    for i,feature in enumerate(testFratureSet):
        if feature!="":
            # # add previous label to feature
            # j=i-1
            # while j>=0 and labels[j][0]=="":
            #     j-=1
            #
            # if j==-1: feature+=['prev_'+feature[0],'prev_'+feature[1],'prev_O']
            # else: feature+=['prev_'+testFratureSet[j][0],'prev_'+testFratureSet[j][1],'prev_'+labels[j][1]] # prevPOS
            # # predict based on feature [tokenName,tokenPOS,tokenBIO,prevLabel]
            feature = trans_dic(feature)
            label = model.classify(feature)
            labels.append((list(feature.keys())[0],label))
        else:
            labels.append(("",""))
    return labels


def write_out(out,outname):
    # write to file
    with open(outname, "w+") as f:
        for word,tag in out:
            if word == "":
                f.write("\n")
            else:
                f.write(word)
                f.write("\t")
                f.write(tag)
                f.write("\n")

if __name__ == "__main__":
    # load files
    trainfilePath = "CONLL_NAME_CORPUS_FOR_STUDENTS/CONLL_train.pos-chunk-name"
    testfilePath = "CONLL_NAME_CORPUS_FOR_STUDENTS/CONLL_dev.pos-chunk"
    predictfilePath = "CONLL_NAME_CORPUS_FOR_STUDENTS/CONLL_test.pos-chunk"
    trainTokenList = loadTrainData(trainfilePath)
    testTokenList = loadTestData(testfilePath)
    predictTokenList = loadTestData(predictfilePath)

    # train model
    trainToks = create_trainToks(trainTokenList)
    model = MaxentClassifier.train(trainToks)

    # predict
    testFratureSet = create_testFeatureSet(testTokenList)
    labels = predict(model,testFratureSet)
    write_out(labels,"response.name")

    predictFeatureSet = create_testFeatureSet(predictTokenList)
    labels = predict(model,predictFeatureSet)
    write_out(labels,"CONLL_test.name")