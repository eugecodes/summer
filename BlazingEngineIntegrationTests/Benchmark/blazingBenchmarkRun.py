import sys
import json
sys.path.append('../Classes')
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet
from S3Handler import S3Handler

##############################################
# CONFIGURATION
##############################################
#DB Connection Config
schema="2"
db="tpch170"
host = "127.0.0.1"
port = 8890
#AWS Security Config - rodrigo iam
aws_access_key_id = "AKIAIPG7TI6LRZY7P3CA"
aws_secret_access_key = "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"
#Logging Config
s3Bucket = 'tpch170blazing'
version = "blazing g2.2xlarge"
nodeCount = "16 nodes"
logFile = "bigBHLogFile.txt"
queryListFile = "queryList.json"
#Run Config
#createTables = False
##############################################
# /CONFIGURATION
##############################################

dataPerNode = 0

#Initialize key objects for the Benchmark
bh = LocalBlazingHandler(host, port, schema, db)
s3h = S3Handler(aws_access_key_id, aws_secret_access_key) #Connect to S3
comp = PostgresComparisonTestSet(bh, "") #Start up Logging Tool

#Set the S3 Bucket (create list and dictionary)
s3h.setBucket(s3Bucket)
bucketDict = s3h.getBucketDict()

#Get the list of queries from a JSON file
json_data=open(queryListFile).read()
queryList = json.loads(json_data)

#Get the # of files in each folder
lengthList = []
for folder in bucketDict:
    lengthList.append(s3h.getFileCount(folder))

uploadCount = 0
while (uploadCount <= max(lengthList)): #Iterate over all of the files, in all of the folders

    #Upload a series of files
    #########################
    for folder in bucketDict: #Iterate over all of the folders
        if uploadCount < s3h.getFileCount(folder):
            filePath = bucketDict[folder][1][uploadCount][0] #File Path
            fileSize = bucketDict[folder][1][uploadCount][1] #File size
            S3filePath = "'" + 's3://' + s3Bucket + '/' + filePath + "'" #Setup path to S3 files
            dataPerNode += fileSize
            tempFileInfo = filePath.split('/') #Break up filePath to make it easier to reference for BlazingDB
            # download file into uploads
            downloadS3intoBHUploads(tempFileInfo[1], schema)
            # load data infile
            bh.loadDataInfile(tempFileInfo[1], tempFileInfo[0])
            # delete data from uploads
            removeS3File(tempFileInfo[1])

    Run queries
    ########################
    for query in queryList:
        qStr = queryList[query]['sql']
        comp.runAndValidateQuery(qStr, showVerboseQuery=True)

    #Log Results
    #########################
    memo = nodeCount + "|" + str(dataPerNode)
    comp.logResults(logFile, version, memo)

    uploadCount += 1 #This index iterates over the files inside the folders
    if uploadCount >= 1:
        break
