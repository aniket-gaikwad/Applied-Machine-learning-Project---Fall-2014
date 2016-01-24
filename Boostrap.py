__author__ = 'Aniket'
import sys
import random
#import  KNN

inputData=[]
SIGMA=0.66
NO_OF_BOOTSTRAPS=int(sys.argv[3])


def bootstrapping(trainSet):
    #fin=open(inputFile,"r")
    #cnt=0
    #global bootstrap
    #bootstrap=[]
    #for line in fin:
        #cnt += 1
        #newLine=line.strip()
        #inputData.append(newLine.split(','))

    global bootstrap
    bootstrap=[]
    print("numberOfInstance : %d" %(len(trainSet)))
    sizeOfBootstrap=int(len(trainSet)/NO_OF_BOOTSTRAPS)

    #sizeOfBootstrap=int(cnt/NO_OF_BOOTSTRAPS)
    print("One Bootstrap size : %d " %(sizeOfBootstrap))

    for i in range(NO_OF_BOOTSTRAPS):
        bootstrap_lst = []
        for j in range(sizeOfBootstrap):
            bootstrap_lst.append(random.choice(trainSet))
        bootstrap.append(bootstrap_lst)

    for i in range(NO_OF_BOOTSTRAPS):
        print("**********")
        #print(bootstrap[i])
        print("length : %d" %(len(bootstrap[i])))



def generateTrainTestSample(inputData):
    #fin=open(inputFile,"r")
    global trainSet
    trainSet = []
    global testSet
    testSet = []

    for line in range(len(inputData)):
        if random.random() < SIGMA:
            trainSet.append(inputData[line])
        else:
            testSet.append(inputData[line])
    print("TRain : ")
    print(trainSet)
    print("Test :")
    print(testSet)
    global noOfTestExamples
    noOfTestExamples=len(testSet)

def main(inputSet):
    #inputFile=sys.argv[1]
    global trainSet
    global testSet
    global bootstrap

    #generateTrainTestSample(inputFile)
    generateTrainTestSample(inputSet)
    bootstrapping(trainSet)


#main()
