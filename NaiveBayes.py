#!/usr/bin/env python3

import sys, random, DecisionTree

PROBABILITY = 0
RANK = 1

def file_read(filename, X, Y):
    
	try:	
		fin = open(filename,"r")
	
		for line in fin:
			newLine = line.strip()
			X.append(newLine.split(','))

		for i in range(len(X)):
			Y.append(X[i][len(X[i]) - 1])
			X[i] = X[i][0 : len(X[i]) - 1]
		
	except:
		print ("\n Incorrect filename or cannot open filename \"%s\" \n" % filename)
		sys.exit()
        
def CalculatePrior(priors, trainSetY):

	for classLabel in trainSetY:
		if (classLabel in priors.keys()):
			priors[classLabel] += 1
		else:
			priors[classLabel] = float(1)

def CreateProbabilityTable(probabilityTable, featureAndValues, setX, setY):

	for example in range(len(setX)):
		classLabel = setY[example]
		
		if (classLabel not in probabilityTable.keys()):
			probabilityTable[classLabel] = {}
		
		for featureIndex in range(len(setX[example])):
			featureValue = setX[example][featureIndex]
			
			if (featureIndex not in featureAndValues.keys()):
				featureAndValues[featureIndex] = []
			
			if (featureValue not in featureAndValues[featureIndex]):
				featureAndValues[featureIndex].append(featureValue)
			
			if (featureIndex not in probabilityTable[classLabel].keys()):
				probabilityTable[classLabel][featureIndex] = {}
			
			if (featureValue in probabilityTable[classLabel][featureIndex].keys()):
				probabilityTable[classLabel][featureIndex][featureValue] += 1
			else:
				probabilityTable[classLabel][featureIndex][featureValue] = float(1)
	
	for classLabel in probabilityTable.keys():
		for feature in featureAndValues.keys():
			for value in featureAndValues[feature]:
				if (value not in probabilityTable[classLabel][feature].keys()):
					probabilityTable[classLabel][feature][value] = float(0)

def AddToFeaturesAndProbabilityTable(probabilityTable, featureAndValues, setX):
	
	for example in range(len(setX)):
		for featureIndex in range(len(setX[example])):
			featureValue = setX[example][featureIndex]
			if (featureValue not in featureAndValues[featureIndex]):
				featureAndValues[featureIndex].append(featureValue)
				for classLabel in probabilityTable.keys():
					probabilityTable[classLabel][featureIndex][featureValue] = float(0)
	
def PerformLaplaceCorrection(probabilityTable, priors, setLength):

	for classLabel in probabilityTable.keys():
		priorCount = priors[classLabel]
		priors[classLabel] = (priors[classLabel] + 1) / (setLength + len(priors))
		for featureIndex in probabilityTable[classLabel].keys():
			featureValuesCount = len(probabilityTable[classLabel][featureIndex])
			for featureValue in probabilityTable[classLabel][featureIndex].keys():
				probabilityTable[classLabel][featureIndex][featureValue] = (probabilityTable[classLabel][featureIndex][featureValue] + 1) / (priorCount + featureValuesCount)
				probabilityTable[classLabel][featureIndex][featureValue] = round(probabilityTable[classLabel][featureIndex][featureValue], 2)
		
def CalculateProbability(probabilityTable, priors, testSetX):
    predictedProbability = {}
    #Iterate through all examples in the test set
    for testExample in range(len(testSetX)):

        # To calculate the probability for (class label
        probability = {}
        # List of probabilities of class labels for (the current example for (ranking
        probabilityRankingList = []
        # To calculate the sum of probabilities of all class labels for (each example
        totalProbability = 0.0
        # Stores the output as - Example index -> Class Label -> [Probability of the class label, Rank of the label for (the example]
        predictedProbability[testExample] = {}

        for classLabel in probabilityTable.keys():
            probability[classLabel] = priors[classLabel]
            predictedProbability[testExample][classLabel] = [0 for i in range(2)]

            for featureIndex in range(len(testSetX[testExample])):
                featureValue = testSetX[testExample][featureIndex]
                probability[classLabel] *= probabilityTable[classLabel][featureIndex][featureValue]

            predictedProbability[testExample][classLabel][PROBABILITY] = probability[classLabel]
            totalProbability += probability[classLabel]
            # Add only distict probabilities
            if(probability[classLabel] not in probabilityRankingList):
                probabilityRankingList.append(probability[classLabel])

        # Sort probabilities in desecnding order
        probabilityRankingList.sort(reverse=True)

        # Normalize the probability and rank each class label for the example
        for classlabel in predictedProbability[testExample].keys():
            predictedProbability[testExample][classlabel][RANK] = probabilityRankingList.index(predictedProbability[testExample][classlabel][PROBABILITY]) + 1
            predictedProbability[testExample][classlabel][PROBABILITY] /= totalProbability

    return predictedProbability

def GenerateTrainSetForRectifier(X, Y, predictedProbability):
    inputToRectifier = []
    for exampleIndex in range(len(X)):
        inputToRectifier.append(X[exampleIndex])
        inputToRectifier[exampleIndex].append(str(GetRank(predictedProbability, exampleIndex, Y[exampleIndex])))
    return inputToRectifier
	
def GetRank(predictedProbability, exampleIndex, classlabel):
	return predictedProbability[exampleIndex][classlabel][RANK]
	
def GetClassLabel(predictedProbability, exampleIndex, rank):
    print(exampleIndex, rank)
    claslabel = [classlabel for classlabel in predictedProbability[exampleIndex].keys() if predictedProbability[exampleIndex][classlabel][RANK] == rank]
    return random.choice(claslabel)

def GetProbabilityDistributionTable(probabilityTable, priors, featureAndValues, dataset, trainSetLength):
    testSetX = []
    for i in range(len(dataset)):
        testSetX.append(dataset[i][0 : len(dataset[i]) - 2])

    AddToFeaturesAndProbabilityTable(probabilityTable, featureAndValues, testSetX)
    PerformLaplaceCorrection(probabilityTable, priors, trainSetLength)
    return CalculateProbability(probabilityTable, priors, testSetX)

def NaiveBayes(trainSet):

    priors = {}
    probabilityTable = {}
    featureAndValues = {}
    tree = {}
    trainSetX = []
    trainSetY = []

    predictedProbability = {}
    inputToRectifier = []

    for i in range(len(trainSet)):
        trainSetY.append(trainSet[i][len(trainSet[i]) - 1])
        trainSetX.append(trainSet[i][0 : len(trainSet[i]) - 2])

    CalculatePrior(priors, trainSetY)
    CreateProbabilityTable(probabilityTable, featureAndValues, trainSetX, trainSetY)
    AddToFeaturesAndProbabilityTable(probabilityTable, featureAndValues, trainSetX)
    PerformLaplaceCorrection(probabilityTable, priors, len(trainSetX))
    predictedProbability = CalculateProbability(probabilityTable, priors, trainSetX)
    #PrintClassLabels(testSetY, predictedProbability)
    inputToRectifier = GenerateTrainSetForRectifier(trainSetX, trainSetY, predictedProbability)

    return (inputToRectifier, probabilityTable, priors, featureAndValues, len(trainSetX))
    #DecisionTree.GenerateTreeFromDatasetGivenByAssorter(inputToRectifier, tree)

