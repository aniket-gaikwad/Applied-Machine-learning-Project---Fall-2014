__author__ = 'Aniket'
import sys
import random
import  KNN

inputData=[]
SIGMA=0.66
NO_OF_BOOTSTRAPS=int(sys.argv[2])


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



def generateTrainTestSample(inputFile):
    fin=open(inputFile,"r")
    global trainSet
    trainSet = []
    global testSet
    testSet = []

    for line in fin:
        newLine=line.strip()
        if random.random() < SIGMA:
            trainSet.append(newLine.split(','))
        else:
            testSet.append(newLine.split(','))


def main():
    inputFile=sys.argv[1]
    global trainSet
    global testSet
    global bootstrap

    generateTrainTestSample(inputFile)
    bootstrapping(trainSet)
    KNN.main(bootstrap[1],testSet,3)

main()
