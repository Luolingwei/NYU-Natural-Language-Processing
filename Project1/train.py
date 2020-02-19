from collections import defaultdict


def corpus_cal():
    file = open("training_corpus.pos", "r").read()
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

    print("success")


corpus_cal()