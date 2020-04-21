NLP HW6 write-up

Submitted files:

	1 Source code: "FeatureBuilder.py"

	2 CONLL_test.name: it's the program output on test data


Best score on development corpus:

	FeatureSet3: [tokenName,tokenPOS]
	  49372 out of 51578 tags correct
	  accuracy: 95.72
	  5917 groups in key
	  6269 groups in response
	  4351 correct groups
  	  precision: 69.41
  	  recall:    73.53
  	  F1:        71.41


All featureSets I tried:

	FeatureSet1: [tokenName]
	  48805 out of 51578 tags correct
  	  accuracy: 94.62
	  5917 groups in key
	  5416 groups in response
	  3872 correct groups
  	  precision: 71.49
  	  recall:    65.44
  	  F1:        68.33

	FeatureSet2: [tokenName,tokenBIO]
	  46874 out of 51578 tags correct
  	  accuracy: 90.88
	  5917 groups in key
	  3477 groups in response
	  2257 correct groups
  	  precision: 64.91
  	  recall:    38.14
  	  F1:        48.05

	FeatureSet3: [tokenName,tokenPOS]
	  49372 out of 51578 tags correct
	  accuracy: 95.72
	  5917 groups in key
	  6269 groups in response
	  4351 correct groups
  	  precision: 69.41
  	  recall:    73.53
  	  F1:        71.41

	FeatureSet4: [tokenName,tokenPOS,tokenBIO]
	  47966 out of 51578 tags correct
  	  accuracy: 93.00
	  5917 groups in key
	  4599 groups in response
	  3107 correct groups
  	  precision: 67.56
  	  recall:    52.51
  	  F1:        59.09

	FeatureSet5: [tokenName,tokenPOS,prevWord]
	  48788 out of 51578 tags correct
  	  accuracy: 94.59
	  5917 groups in key
	  5246 groups in response
	  3694 correct groups
  	  precision: 70.42
  	  recall:    62.43
  	  F1:        66.18

	FeatureSet6: [tokenName,tokenPOS,prevPOS]
	  48142 out of 51578 tags correct
  	  accuracy: 93.34
	  5917 groups in key
	  5137 groups in response
	  3284 correct groups
  	  precision: 63.93
  	  recall:    55.50
  	  F1:        59.42

	FeatureSet7: [tokenName,tokenPOS,prevLabel]
	  47877 out of 51578 tags correct
	  accuracy: 92.82
	  5917 groups in key
	  4071 groups in response
	  3231 correct groups
  	  precision: 79.37
  	  recall:    54.61
  	  F1:        64.70

	FeatureSet8: [tokenName,tokenPOS,prevWord,prevPOS,prevLabel]
	  46442 out of 51578 tags correct
  	  accuracy: 90.04
	  5917 groups in key
	  2854 groups in response
	  1922 correct groups
  	  precision: 67.34
  	  recall:    32.48
  	  F1:        43.83

