import gensim
import shutil
from sys import platform
from gensim.models import word2vec

# 计算行数，就是单词数
def getFileLineNums(filename):
    f = open(filename, 'r')
    count = 0
    for line in f:
        count += 1
    return count


# Linux或者Windows下打开词向量文件，在开始增加一行
def prepend_line(infile, outfile, line):
    with open(infile, 'r') as old:
        with open(outfile, 'w') as new:
            new.write(str(line) + "\n")
            shutil.copyfileobj(old, new)


def prepend_slow(infile, outfile, line):
    with open(infile, 'r') as fin:
        with open(outfile, 'w') as fout:
            fout.write(line + "\n")
            for line in fin:
                fout.write(line)


def load(filename):
    num_lines = getFileLineNums(filename)
    print("there are %d lines in total"%(num_lines))
    gensim_file = 'glove_model.txt'
    gensim_first_line = "{} {}".format(num_lines, 50)
    # Prepends the line.
    if platform == "linux" or platform == "linux2":
        prepend_line(filename, gensim_file, gensim_first_line)
        print("append success")
    else:
        prepend_slow(filename, gensim_file, gensim_first_line)
        print("append success")

    model = gensim.models.KeyedVectors.load_word2vec_format(gensim_file)
    model.save_word2vec_format("glove.model")
    print("model save success")



if __name__ == "__main__":

    glove_path = "/Users/luolingwei/Desktop/Classes/NLP/Homeworks/HW7/glove.6B.50d.txt"
    load(glove_path)
    print("Generate glove model success")