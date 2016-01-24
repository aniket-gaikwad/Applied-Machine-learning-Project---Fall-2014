__author__ = 'Aniket'
import sys
import operator

def file_read(inputFile):
    fin=open(inputFile,"r")
    global inputSet
    inputSet = []
    global trainClassLabelSet
    trainClassLabelSet = []
    for line in fin:
        newLine=line.strip()
        inputSet.append(newLine.split(','))

def readMetaFile(metaFile):
    fin=open(metaFile,"r")
    global metadata
    metadata = []
    for line in fin:
        newLine=line.strip()
        metadata.append(newLine.split(','))
    print("*****METADATA*****")
    print(metadata)

def metadataPopulation(metadata):

    ########## creation of sub-metadata ###################
    global subMetadata
    subMetadata={}

    for i in range(lengthOfInstance):
        subMetadata[metadata[i][0]]=metadata[i][1]
    print("Sub-metedata")
    print(subMetadata)

    ################### Meta Continous Values ##########################################
    metaContinousValues={'0-.100':'0.50','.101-.200':'0.150','.201-.300':'0.250','.301-.400':'0.350','.401-.500':'0.450','.501-.600':'0.550','.601-.700':'0.650','.701-.800':'0.750','.801-.900':'0.850','.901-1':'0.950'}
    print("metaContinousValues")
    print(metaContinousValues)
    ################# Meta character values ################################
    global metaCharValues
    metaCharValues={}
    tempList=[]
    for i in range(lengthOfInstance):
        tempList.append(metadata[i][2:])
    #print("TEMPLIST")
    #print(tempList)
    count=0
    for j in range(len(tempList)):
        if metadata[j][1] == 'CH':
            for k in range(len(tempList[j])):
                if tempList[j][k] in metaCharValues:
                    continue
                else:
                    count += 1
                    metaCharValues[tempList[j][k]] = count
    print("metaCharValues")
    print(metaCharValues)

    ############### Meta other Values #############################

    global metaOtherValues
    metaOtherValues={}
    tempList=[]
    for i in range(lengthOfInstance):
        tempList.append(metadata[i][2:])
    #print("TEMPLIST")
    #print(tempList)
    count=0
    for j in range(len(tempList)):
        if metadata[j][1] == 'O':
            for k in range(len(tempList[j])):
                if tempList[j][k] in metaOtherValues:
                    continue
                else:
                    count += 1
                    metaOtherValues[tempList[j][k]] = count
    print("metaOtherValues")
    print(metaOtherValues)
        #for j in range(len(tempList)):
            #print(metadata[i][j])

def dataNormalization(sample):
    intSample=map(float,sample)
    #print("sample",sample)
    #print("**Max***")
    #print(max(intSample))
    minS=min(intSample)
    #print("mins",minS)
    intSample=map(float,sample)
    maxS=max(intSample)
    #print("maxS",maxS)


    z={}
    for i in range(len(sample)):
        z[sample[i]]=abs((float(sample[i])-minS)/(maxS-minS))
    #print("Z:" , z)

    #print("Min Z" ,min(z.items(),key=lambda x:x[1]))
    #print("Max Z" ,max(z.items(),key=lambda x:x[1]))

    return z

def normalization():
    global normalizedData
    normalizedData={}
    for i in range(lengthOfInstance):
        #if  str(i) in subMetadata:
        type=subMetadata[str(i)]
        #print("TYPE : ",type)
        temp_list=[]
        if type=='C':
            for j in range(len(inputSet)):
                temp_list.append(inputSet[j][i])
            normalizedData[i]=dataNormalization(temp_list)
        #print("normalizedData[%d]" %(i))
        #print(normalizedData[i])

def inputDataModification(inputSet):
    #print("*************Original Training Set************")
    #print(inputSet)
    global inputSetNew
    inputSetNew=inputSet
    type =''
    #print(subMetadata)
    for j in range(lengthOfInstance):
        #print(str(j))
        if  str(j) in subMetadata:

            type=subMetadata[str(j)]
            #print("Type : ",type)
        for i in range(len(inputSet)):
            if type=='C':
                if inputSet[i][j] in normalizedData[j]:
                    inputSet[i][j]=str(normalizedData[j][inputSet[i][j]])
            elif type=='CH':
                if inputSet[i][j] in metaCharValues:
                    inputSet[i][j]=str(metaCharValues[inputSet[i][j]])
            elif type=='O':
                if inputSet[i][j] in metaOtherValues:
                    inputSet[i][j]=str(metaOtherValues[inputSet[i][j]])



def dataCleaning():
    '''global inputSet
    tobeDeleted=[]
    for i in reversed(range(len(inputSet))):
        for j in range(lengthOfInstance):
            if inputSet[i][j]=='?':
                del inputSet[i]
                #print(i,inputSet[i])
                #tobeDeleted.append(i)
                break

    print("***tobeDeleted****")
    print(tobeDeleted)
    print("Length : ",len(tobeDeleted))
    for i in range(NoOfInstance):
        if i in tobeDeleted:
            print("GONNA DELETE : %d" %(i))
            print(inputSet[i])
            del inputSet[i]
    print("AFTER DELETION OF INPUT SET :")
    print(inputSet[71])

    for example in inputSet:
        for attribute in example:
            if attribute=='?':
                print("EXAMPLE :" ,example)
                inputSet.remove(example)
                break'''

    for i in range(NoOfInstance-1,0,-1):
        for j in range(lengthOfInstance):
            if inputSet[i][j]=='?':
                inputSet.remove(inputSet[i])
                break

    print("After Cleansing :")
    print(inputSet)



def main():
    inputFile=sys.argv[1]
    metaFile=sys.argv[2]
    file_read(inputFile)
    global inputSet
    #print("****inputSet***** : ")
    #print(inputSet)
    global lengthOfInstance
    lengthOfInstance=len(inputSet[1])
    global NoOfInstance
    NoOfInstance=len(inputSet)
    #print("Length of one instance : %d" %(lengthOfInstance))
    #temp_list=[]
    #tSet=['2','3','2','2']
    attributeValues=[]
    for i in range(lengthOfInstance):
        temp_list=[]
        for j in range(len(inputSet)):
            temp_list.append(inputSet[j][i])
        attributeValues.append(temp_list)
        #print("************************")
        #print(len(attributeValues[i]))
        #print(len(set(attributeValues[i])))
    #print(set(attributeValues[4]))

    readMetaFile(metaFile)
    dataCleaning()
    metadataPopulation(metadata)
    #inputDataModification(inputSet)
    #print("METADATA :")
    #print(metadata)
    normalization()
    inputDataModification(inputSet)
    print("********Modified*********")
    print(inputSet)
    #dataCleaning()

#main()


