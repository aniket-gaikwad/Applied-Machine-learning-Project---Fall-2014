__author__ = 'Aniket'
import math
import sys
import operator

NO_OF_NEIGBHORS=int(sys.argv[3])

def file_read_trainSet(inputFile):
    fin=open(inputFile,"r")
    global trainSet
    trainSet = []
    global trainClassLabelSet
    trainClassLabelSet = []
    for line in fin:
        newLine=line.strip()
        trainSet.append(newLine.split(','))

    #for i in range(len(trainSet)):
        #trainClassLabelSet.append(trainSet[i][len(trainSet[i])-1:])
        #trainSet[i]=trainSet[i][0:len(trainSet[i])-1]
    #print(trainSet)



def file_read_testSet(inputFile):
    fin=open(inputFile,"r")
    global testSet
    testSet = []
    global testClassLabelSet
    testClassLabelSet = []
    for line in fin:
        newLine=line.strip()
        testSet.append(newLine.split(','))

    #for i in range(len(testSet)):
        #testClassLabelSet.append(testSet[i][len(testSet[i])-1:])
        #testSet[i]=testSet[i][0:len(testSet[i])-1]
    #print(testSet)

def ecludianDistance(instance1,instance2,length):
    distance=0
    #print(instance1)
    for x in range(length):
        distance += pow((int(instance1[x])-int(instance2[x])),2)
    #print("distance: %d" %distance)
    return math.sqrt(distance)

def getNeighbors(testInstance,trainSet,k):
    length=len(testInstance)-1
    distOfTestInstance=[]
    #global neighbors
    neighbors=[]
    sortedDistforTestInstance=[]
    global trainClassLabelSet

    for x in range(len(trainSet)):
        distance=ecludianDistance(testInstance,trainSet[x],length)
        distOfTestInstance.append((trainSet[x],distance))

    sortedDistforTestInstance = sorted(distOfTestInstance,key=operator.itemgetter(1),reverse=False)
    #sortedDistforTestInstance = sorted(distOfTestInstance,key=lambda i:distOfTestInstance[1],reverse=False)
    #print(sortedDistforTestInstance)

    for i in range(k):
        neighbors.append(sortedDistforTestInstance[i][0] )
    return neighbors

def getVotingByNeighbors(neighbors):
    length=len(neighbors)
    neighborsVote={}

    for x in range(len(neighbors)):
        #print(neighbors[x][1][0])
        if neighbors[x][-1] in neighborsVote:                ## its list of 2 list and x will point to each (list1,list2)
            neighborsVote[neighbors[x][-1]] += 1
        else:
            neighborsVote[neighbors[x][-1]] = 1
    #print(neighborsVote)
    #for x in range(len(neighbors)):
        #print()

    sortedNeighborsVote=sorted(neighborsVote.items(),key=operator.itemgetter(1),reverse=True)
    #print(sortedNeighborsVote)
    #print(sortedNeighborsVote[0][0])
    return(sortedNeighborsVote[0][0])

def getTestError(prediction,actualLabel):
    length=len(prediction)
    cnt=0
    print(prediction)
    print(actualLabel)
    print(length)
    for i in range(length):
        if prediction[i]!=actualLabel[i]:
            cnt += 1
    print(cnt)

    return ((cnt*100)/length)


def main():
    trainFile=sys.argv[1]
    testFile=sys.argv[2]

    file_read_trainSet(trainFile)
    #print(trainSet)
    file_read_testSet(testFile)
    #print(testSet)
    #print(testSet[1])
    prediction=[]
    actualLabel=[]
    for i in range(len(testSet)):
        neighbors=getNeighbors(testSet[i],trainSet,NO_OF_NEIGBHORS)
        #print("neighbors : %s" %(neighbors))
        neighborsVote=getVotingByNeighbors(neighbors)
        #print(neighborsVote)
        print("For testSet : %s Prediction : %s Actual Class Label : %s" %(testSet[i],neighborsVote,testSet[i][-1]))
        prediction.append(neighborsVote)
        actualLabel.append(testSet[i][-1])
    testError=getTestError(prediction,actualLabel)
    print("****Test Error*****")
    print(testError)
main()