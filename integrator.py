__author__ = 'Aniket'
import Preprocessing
import Boostrap
import KNN
import NaiveBayes
import DecisionTree

def calculateTestError():
    testError=KNN.getTestError(resultKNN,KNN.actualLabel)
    print("****Test Error*****")
    print(testError)
    print("*******Accuracy********")
    accuracy=100-testError
    print(accuracy)

def boostrapVoting():
    global resultKNN
    resultKNN=[]
    for i in range(Boostrap.noOfTestExamples):
        tempDictionary={}
        for j in range(Boostrap.NO_OF_BOOTSTRAPS):
            if prediction[j][i] in tempDictionary:
                tempDictionary[prediction[j][i]] += 1
            else:
                tempDictionary[prediction[j][i]] = 1
        #print("tempDictionary")
        #print(tempDictionary)
        maxVote=max(tempDictionary.items(),key=lambda x:x[1])
        resultKNN.append(maxVote[0])

    print("resultKNN")
    print(resultKNN)



def integrator():
    K=5
    Preprocessing.main()
    Boostrap.main(Preprocessing.inputSet)
    #print(Boostrap.testSet)
    global prediction
    prediction={}
    #bootstrapVoting
    for i in range(Boostrap.NO_OF_BOOTSTRAPS):
        print("*** %d BootStrap ****" %(i))
        #prediction[i]=KNN.main(Boostrap.bootstrap[i],Boostrap.testSet,K)
        (inputToRectifier,probabilityChart, priors, featureAndValues, trainSetLength)=NaiveBayes.NaiveBayes(Boostrap.bootstrap[i])
        print("********DECIION TREE************")
        tree=DecisionTree.GenerateTreeFromDatasetGivenByAssorter(inputToRectifier)
        print("********DECIION TREE ENDS************")
        print("********TEST NAIVE START************")
        probabilityDistributionChart=NaiveBayes.GetProbabilityDistributionTable(probabilityChart, priors, featureAndValues, Boostrap.testSet,trainSetLength)
        print("********TEST NAIVE ENDS************")
        print("********PREDICTION START************")
        prediction[i]=DecisionTree.PredictedList(probabilityDistributionChart,tree,Boostrap.testSet)
    #print("***prediction***",prediction)
    print("*********** BootStrapVoting *************")
    boostrapVoting()
    calculateTestError()


integrator()