import gensim
import numpy as np
from scipy.stats import pearsonr


def load353(filePath):
    pairs = []
    real_scores = []
    file = open(filePath, "r")
    for line in file.readlines():
        if line[0]=='#': continue
        line = line.rstrip("\n")
        tokens = line.split("\t")
        pairs.append([tokens[1].lower(),tokens[2].lower()])
        real_scores.append(float(tokens[3]))
    return pairs, real_scores

def score_embeddings(pairs):
    machine_score = []
    for word1,word2 in pairs:
        vector1 = model.wv[word1]
        vector2 = model.wv[word2]
        machine_score.append(round(cosine_similarity(vector1,vector2),3))
    return machine_score

def cosine_similarity(vector1,vector2):
    vec1 = np.array(vector1)
    vec2 = np.array(vector2)
    return np.dot(vec1,vec2)/(np.linalg.norm(vec1)*(np.linalg.norm(vec2)))

def analogy(word1,pre_word1,word2):
    vector1 = np.array(model.wv[word1])
    vector2 = np.array(model.wv[word2])
    pre_vector1 = np.array(model.wv[pre_word1])
    pre_vector2 = list(pre_vector1 + (vector2 - vector1))

    most_similar = ""
    maxSimilarity = -1
    for word in model.index2word:
        if word!=pre_word1:
            curvector = model.wv[word]
            curSimilarity = cosine_similarity(curvector,pre_vector2)
            if curSimilarity > maxSimilarity:
                most_similar, maxSimilarity = word, curSimilarity
    return most_similar


if __name__ == "__main__":


    model = gensim.models.KeyedVectors.load_word2vec_format("glove.model")
    pairs, human_scores = load353("wordsim-353.txt")
    machine_scores = score_embeddings(pairs)
    r, p_value = pearsonr(human_scores, machine_scores)

    with open("output.txt", "w+") as f:
        f.write("########################## Calculate wordsim-353 ###########################\n")
        f.write("{: <15} {: <15} {: <15} {: <15}".format("word1","word2","human score","machine score"))
        f.write("\n")
        for i,pair in enumerate(pairs):
            f.write("{: <15} {: <15} {: <15} {: <15}".format(pair[0],pair[1],str(human_scores[i]),str(machine_scores[i])))
            f.write("\n")

        f.write("\n")
        f.write("overall correlation is: %.3f\n" % (r))
        f.write("\n")

        f.write("############################# Analogy #####################################\n")

        f.write("analogy for [king,man,queen] is: ")
        f.write(analogy("king","man","queen") + "\n")

        f.write("analogy for [king,father,queen] is: ")
        f.write(analogy("king","father","queen") + "\n")

        f.write("analogy for [boy,man,girl] is: ")
        f.write(analogy("boy","man","girl") + "\n")

        f.write("analogy for [brother,boy,sister] is: ")
        f.write(analogy("brother","boy","sister") + "\n")

        f.write("analogy for [china,beijing,america] is: ")
        f.write(analogy("china","beijing","america") + "\n")

        f.write("analogy for [tokyo,japan,beijing] is: ")
        f.write(analogy("tokyo","japan","beijing") + "\n")

        f.write("analogy for [summer,hot,winter] is: ")
        f.write(analogy("summer", "hot", "winter") + "\n")

        f.write("analogy for [bad,worse,good] is: ")
        f.write(analogy("bad", "worse", "good") + "\n")

        f.write("analogy for [sunny,sun,rainy] is: ")
        f.write(analogy("sunny", "sun", "rainy") + "\n")

        f.write("analogy for [big,heavy,small] is: ")
        f.write(analogy("big", "heavy", "small") + "\n")

        f.write("analogy for [happy,happiness,sad] is: ")
        f.write(analogy("happy", "happiness", "sad") + "\n")

        f.write("analogy for [plant,oxygen,animal] is: ")
        f.write(analogy("plant", "oxygen", "animal") + "\n")
