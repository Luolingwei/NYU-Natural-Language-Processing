from collections import defaultdict


def corpus_cal(corpus):
    file = open(corpus, "r").read()
    lines = file.splitlines()

    tag_count=defaultdict(int)
    word2tag_count=defaultdict(lambda: defaultdict(int))
    tagTrans_count=defaultdict(int)

    for i in range(len(lines)):
        curline=lines[i].split("\t")
        if i!=len(lines)-1: nextline=lines[i+1].split("\t")
        else: nextline=""

        # count tag and word2tag
        if len(curline)==2:
            # count tags
            word,tag=curline[0],curline[1]
            tag_count[tag]+=1
            word2tag_count[word][tag]+=1

        # count tagTransfer
        if len(curline)==2 and len(nextline)==2:
            curtag,nexttag=curline[1],nextline[1]
            tagTrans_count[(curtag,nexttag)]+=1

    tag_poss=defaultdict(int)
    word2tag_poss=defaultdict(lambda: defaultdict(int))
    tagTrans_poss=defaultdict(lambda: defaultdict(int))

    # tag poss calculation
    tag_sum=sum(tag_count.values())
    for tag in tag_count.keys():
        tag_poss[tag]=tag_count[tag]/tag_sum

    # word2Tag poss calculation
    for word in word2tag_count.keys():
        inner_total=sum(word2tag_count[word].values())
        for tag in word2tag_count[word]:
            word2tag_poss[word][tag]=word2tag_count[word][tag]/inner_total

    # tagTransfer poss calculation
    trans_sum=sum(tagTrans_count.values())
    for trans in tagTrans_count.keys():
        poss=tagTrans_count[trans]/trans_sum
        tagTrans_poss[trans[1]][trans]=poss

    return tag_poss,word2tag_poss,tagTrans_poss

def sample_predict(tag_poss,word2tag_poss,tagTrans_poss,sample):
    file = open(sample, "r")
    line_number=0
    out=[]
    for line in file.readlines():

        word=line.rstrip()
        if word=="":
            out.append(("",""))
            continue

        if line_number==0:
            if word in word2tag_poss:
                ans_tag=max(word2tag_poss[word].keys(),key=lambda x:word2tag_poss[word][x])
            else:
                ans_tag=max(tag_poss.keys(),key=lambda x:tag_poss[x])
        else:
            pre_tag=out[-1][1]
            if word in word2tag_poss:
                max_poss = 0
                for curtag,poss in word2tag_poss[word].items():
                    if poss*tagTrans_poss[curtag][(pre_tag,curtag)]!=0:
                        # (pre_tag,curtag) transfer can be found
                        curposs=poss*tagTrans_poss[curtag][(pre_tag,curtag)]
                    else:
                        curposs=poss*(sum(tagTrans_poss[curtag].values())/len(tagTrans_poss[curtag]))

                    if curposs>max_poss:
                        max_poss=curposs
                        ans_tag=curtag
            else:
                max_poss = 0
                for curtag,poss in tag_poss.items():
                    if poss*tagTrans_poss[curtag][(pre_tag,curtag)]!=0:
                        # (pre_tag,curtag) transfer can be found
                        curposs=poss*tagTrans_poss[curtag][(pre_tag,curtag)]
                    else:
                        curposs=poss*(sum(tagTrans_poss[curtag].values())/len(tagTrans_poss[curtag]))

                    if curposs > max_poss:
                        max_poss = curposs
                        ans_tag = curtag

        out.append((word,ans_tag))
        line_number+=1
    return out

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
    corpus="training_corpus.pos"
    tag_poss,word2tag_poss,tagTrans_poss=corpus_cal(corpus)

    # wirte out 24 test file
    sample="WSJ_24.words"
    outname="out24.pos"
    out=sample_predict(tag_poss,word2tag_poss,tagTrans_poss,sample)
    write_out(out,outname)

    # write out 23 predict file
    sample="WSJ_23.words"
    outname="WSJ_23.pos"
    out=sample_predict(tag_poss,word2tag_poss,tagTrans_poss,sample)
    write_out(out,outname)