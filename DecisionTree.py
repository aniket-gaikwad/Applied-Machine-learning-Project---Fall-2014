#!/usr/bin/env python3

COMMA_SEPARATOR = ','
INSTANCE_COUNT = 0
ATTRIBUTE_COUNT = 0
LEAF = "__leaf"

import random, math, NaiveBayes

def file_read(filename, X, Y):
	
	try:	
		fin = open(filename,"r")
		
		for line in fin:
			newLine = line.strip()
			X.append(newLine.split(COMMA_SEPARATOR))

		for i in range(len(X)):
			Y.append(X[i][len(X[i]) - 1])

	except:
		print("\n Incorrect filename or cannot open filename \"%s\" \n" % filename)
		sys.exit()
		
def CalculateClassEntropy(Y):
	
	classLabel_count = dict((classLabel, Y.count(classLabel)) for classLabel in Y)
	(ratio, entropy) = (0, 0)
	
	for classLabel in classLabel_count:
		ratio = classLabel_count[classLabel] / len(Y)
		entropy += -1 * ratio * math.log2(ratio)

	return entropy

def InfoGain(X, ignoreAttr, classEntropy):
	
	info_gain = {}
	instance_count = len(X)
	attribute_count = len(X[0])
	
	for attribute in range(attribute_count - 1):
		
		if attribute in ignoreAttr:
			continue
		
		attrValue_classLabel_count = {}
		attrValue_count = {}

		for instance in range(instance_count):
			
			classLabel = X[instance][attribute_count - 1]
			attrValue = X[instance][attribute]
			
			if attrValue not in attrValue_classLabel_count:
				attrValue_classLabel_count[attrValue] = {}
			
			if classLabel not in attrValue_classLabel_count[attrValue]:
				attrValue_classLabel_count[attrValue][classLabel] = 1
			else:
				attrValue_classLabel_count[attrValue][classLabel] += 1

			if attrValue not in attrValue_count:
				attrValue_count[attrValue] = 1
			else:
				attrValue_count[attrValue] += 1

		(ratio, entropy, attrEntropy) = (0, 0, 0)

		for attrValue in attrValue_classLabel_count:
			for classLabel in attrValue_classLabel_count[attrValue]:
				
				ratio = attrValue_classLabel_count[attrValue][classLabel] / attrValue_count[attrValue]
				entropy += -1 * ratio * math.log2(ratio)
				
			attrEntropy += entropy * attrValue_count[attrValue] / instance_count
			entropy = 0
		info_gain[attribute] = (classEntropy - attrEntropy) / classEntropy
		
	max_infogain_value = max(info_gain.values())
	attributes = [(attribute, info_gain) for attribute, info_gain in info_gain.items() if info_gain == max_infogain_value]
	
	return random.choice(attributes)

def SplitDataset(attribute, X):
	splitDataset = {}
	
	for instance in range(len(X)):
		
		attrValue = X[instance][attribute]
		
		if attrValue not in splitDataset:
			splitDataset[attrValue] = []
		
		splitDataset[attrValue].append(X[instance])

	return splitDataset

def DominatingClassLabel(X):
	global ATTRIBUTE_COUNT
	classlabel_count = {}
	for instance in X:
		classlabel = instance[ATTRIBUTE_COUNT - 1]
		if classlabel not in classlabel_count:
			classlabel_count[classlabel] = 1
		else:
			classlabel_count[classlabel] += 1
	
	max_classlabel_count = max(classlabel_count.values())
	classlabels = [classlabel for classlabel, count in classlabel_count.items() if count == max_classlabel_count]
	return random.choice(classlabels)

def ConstructTree(tree, X, ignoreAttr, classEntropy, height):
	if(height == 0 or classEntropy == 0):
		tree[LEAF] = DominatingClassLabel(X)
		return

	(attribute, info_gain) = InfoGain(X, ignoreAttr, classEntropy)
	
	ignoreAttrs = ignoreAttr[:]
	ignoreAttrs.append(attribute)
	setX = SplitDataset(attribute, X)
	
	if(info_gain == 1.0):
		if(len(setX) == 1):
			tree[LEAF] = DominatingClassLabel(X)
		else:
			tree[attribute] = {}
			for attrValue in setX:
				tree[attribute][attrValue] = {}
				tree[attribute][attrValue][LEAF] = DominatingClassLabel(setX[attrValue])
		return

	tree[attribute] = {}

	for attrValue in setX:
		tree[attribute][attrValue] = {}
		ConstructTree(tree[attribute][attrValue], setX[attrValue], ignoreAttrs, classEntropy, height - 1)
	
def Predict(predictSet, X, tree, trace):
    for key in tree.keys():
        print(key)
        if(key == LEAF):
            val = tree[LEAF]
            break

        value = str(X[key])

        if(value in tree[key].keys()):
            next = tree[key][value]
        else:
            val = PredictUnseenValue(predictSet, trace)
            break

        if(LEAF not in next.keys()):
            trace.append([key, value])
            val = Predict(predictSet, X, next, trace)
        else:
            val = next[LEAF]
        break
    return val

def PredictUnseenValue(X, trace):
	global ATTRIBUTE_COUNT
	predictSet = X

	for attribute, value in trace:
		splitDataset = SplitDataset(attribute, predictSet)
		predictSet = splitDataset[value]

	attrValue_count = {}
	
	for instance in range(len(predictSet)):
		attrValue = X[instance][ATTRIBUTE_COUNT - 1]
		
		if attrValue not in attrValue_count:
			attrValue_count[attrValue] = 1
		else:
			attrValue_count[attrValue] += 1
	
	max_attrValue_count = max(attrValue_count.values())
	attrValues = [attrValue for attrValue, count in attrValue_count.items() if count == max_attrValue_count]
	return random.choice(attrValues)

def PrintPredictions(tree, X, Y):
	for i in range(len(X)):
		original = Y[i]
		predicted = Predict(X, X[i], tree, [])
		print("Y: ", original, " Y': ", predicted, " Same: ", original == predicted, " Instance: ", i)

def PredictedList(probabilityDistributionChart, tree, X):
    predictedList = []

    for example in probabilityDistributionChart.keys():
        print(probabilityDistributionChart[example])
    print(tree)
    for i in range(len(X)):
        predictedList.append(NaiveBayes.GetClassLabel(probabilityDistributionChart, i, Predict(X, X[i], tree, [])))
    return predictedList

def GenerateTreeFromDatasetGivenByAssorter(X):
    global INSTANCE_COUNT
    global ATTRIBUTE_COUNT
    trainSetX = X
    trainSetY = []
    predictedList = []
    tree = {}

    INSTANCE_COUNT = len(trainSetX)
    ATTRIBUTE_COUNT = len(trainSetX[0])

    for instance in trainSetX:
        trainSetY.append(instance[ATTRIBUTE_COUNT - 1])

    classEntropy = CalculateClassEntropy(trainSetY)
    ConstructTree(tree, trainSetX, [], classEntropy, 3)
	#print(tree)
	#PrintPredictions(tree, trainSetX, trainSetY)
    return tree