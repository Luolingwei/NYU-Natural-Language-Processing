NLP HW4 write-up

The score on the development corpus (WSJ_24.pos): 
	31420 out of 32853 tags correct
  	accuracy: 95.638146

Submitted files:

	1 Source code: "train.py". It takes "training_corpus.pos" as the training corpus. After the training, it also takes WSJ_23.words and WSJ_24.words as predict source files, and it will output the corresponding tagged files "WSJ_23.pos" and "out24.pos".
	Note: "out24.pos" is used for model scoring. And "WSJ_23.pos" is the required prediction.

	2 "WSJ_23.pos". It is the tagged file my program output.


The tagging logic in my program:

	Training: Based on the training corpus, I will calculate and get 3 dictionary.
		  (1) tagTrans_poss: {tagA:{(tag1,tagA):poss1,(tag2,tagA):poss2}}, it stores the tag transition possibility of each (preTag, curTag).
		  (2) tag_poss: {tagA: possibility}, it stores the occurrence possibility of all tags.
		  (3) word2tag_poss: {wordA:{tag1:poss1,tag2:poss2}}, it stores the tag possibility for a certain word.

	Tagging: I calculated tag using different strategies for different cases.
		  (1) for line0, it has no previous line. If it appeared in corpus, we use word2tag_poss to extract tag with largest poss. If it's not in corpus (unknown word), we use tag_poss to extract tag with largest poss.
		  (2) for words appeared in corpus, we use word2tag_poss to extract tag poss, and also extract tagTransition poss using tagTrans_poss. If tagTransition poss exists, we use tag poss*tagTransition poss as poss of current tag. Otherwise, we use tag poss * average poss of (tagTrans_poss[tag]). We set tag of largest poss as final tag for current word.
		  (3) for words not in the corpus (unknown words). We use tag_poss to extract tag poss, and also extract tagTransition poss using tagTrans_poss. If tagTransition poss exists, we use tag poss*tagTransition poss as poss of current tag. Otherwise, we use tag poss * average poss of (tagTrans_poss[tag]). We set tag of largest poss as final tag for current word.
