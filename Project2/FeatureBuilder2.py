from nltk import MaxentClassifier
from gensim.models import word2vec
import gensim

def trans_dic(words):
    return {word:True for word in words}


def loadTrainData(filePath):
    trainTokenList = []
    words = []
    file = open(filePath, "r")
    for line in file.readlines():
        line = line.rstrip("\n")
        if line!="":
            token=line.split("\t")
            trainTokenList.append(token)
            words.append(token[0])
    return words,trainTokenList


def loadTestData(filePath):
    testokenList = []
    words = []
    file = open(filePath, "r")
    for line in file.readlines():
        line = line.rstrip("\n")
        if line != "":
            token = line.split("\t")
            testokenList.append(token)
            words.append(token[0])
        else:
            testokenList.append("")
    return words,testokenList

def generateWord2Vec(words):

    # glove cover
    model = gensim.models.KeyedVectors.load_word2vec_format("glove.model")
    memo = set(model.index2word)
    # sentences = [words]
    # model = word2vec.Word2Vec(sentences,window=10,min_count=1,size=20)

    # collect vectors
    vectors = []
    for word in words:
        if word in memo:
            vectors.append(model.wv[word])
        else:
            vectors.append([])

    # fill empty vectors by neighbors
    for i, v in enumerate(vectors):
        if len(v) == 0:
            neighbors = []
            j = i - 1
            while j >= 0 and len(vectors[j]) == 0:
                j -= 1
            if j >= 0: neighbors.append(vectors[j])
            k = i + 1
            while k < len(vectors) and len(vectors[k]) == 0:
                k += 1
            if k < len(vectors): neighbors.append(vectors[k])
            vectors[i] = sum(neighbors) / len(neighbors)

    vectors_memo = {}
    # create avg vectors for each unique word (only 2w unique words, 1.1w covered by glove but 20w+ words in train corpus)
    for i,word in enumerate(words):
        curvector = vectors[i]
        if word not in vectors_memo:
            vectors_memo[word] = [curvector]
        else:
            vectors_memo[word].append(curvector)

    # average all vectors for a certain word
    for uniqueWord, vector in vectors_memo.items():
        curvectorList = vectors_memo[uniqueWord]
        vectors_memo[uniqueWord] = sum(curvectorList)/len(curvectorList)

    # calculate mean values based on unique words vector set
    avgValues = []
    for feature in zip(*list((vectors_memo.values()))):
        avg = sum(feature)/len(feature)
        avgValues.append(avg)

    # create features for each unique word
    word2vecFeatureDic = {}
    for uniqueWord, vector in vectors_memo.items():
        curfeature = []
        for j,n in enumerate(vector):
            # larger than average value, label it as 'U', else 'B'
            if n>avgValues[j]:
                curfeature.append(str(j)+'U')
            else:
                curfeature.append(str(j)+'B')
        word2vecFeatureDic[uniqueWord] = curfeature
    return word2vecFeatureDic


def create_trainToks(tokenList,trainWord2VecFeature):
    # type train_toks: list
    # param train_toks: Training data, represented as a list of
    # pairs, the first member of which is a featureset,
    # and the second of which is a classification label.
    trainToks = []
    for i,token in enumerate(tokenList):
        # add prior state
        tokenName,tokenPOS,tokenBIO,tokenLabel,prevWord,prevPOS,prevLabel = token[0],token[1],token[2],token[3],'prev_'+tokenList[max(0,i-1)][0],'prev_'+tokenList[max(0,i-1)][1],'prev_'+tokenList[max(0,i-1)][3]
        featureset = [tokenName,tokenPOS]
        featureset+=trainWord2VecFeature[tokenName]
        trainToks.append((trans_dic(featureset),tokenLabel))
    return trainToks


def create_testFeatureSet(testokenList,testWord2VecFeature):
    # type train_toks: list
    # param train_toks: Training data, represented as a list of
    # pairs, the first member of which is a featureset,
    # and the second of which is a classification label.
    testFratureSet = []
    for i,token in enumerate(testokenList):
        if token!="":
            tokenName,tokenPOS,tokenBIO = token[0],token[1],token[2]
            featureset = [tokenName,tokenPOS]
            featureset+=testWord2VecFeature[tokenName]
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

    trainwords, trainTokenList = loadTrainData(trainfilePath)
    trainWord2VecFeature = generateWord2Vec(trainwords)

    testwords, testTokenList = loadTestData(testfilePath)
    testWord2VecFeature = generateWord2Vec(testwords)

    predictwords, predictTokenList = loadTestData(predictfilePath)
    predictWord2VecFeature = generateWord2Vec(predictwords)

    # train model
    trainToks = create_trainToks(trainTokenList,trainWord2VecFeature)
    model = MaxentClassifier.train(trainToks)

    # predict
    testFratureSet = create_testFeatureSet(testTokenList,testWord2VecFeature)
    labels = predict(model,testFratureSet)
    write_out(labels,"response.name")

    predictFeatureSet = create_testFeatureSet(predictTokenList, predictWord2VecFeature)
    labels = predict(model,predictFeatureSet)
    write_out(labels,"CONLL_test.name")