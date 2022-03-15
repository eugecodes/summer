import sys
import json
sys.path.append('../Classes')
from RedshiftHandler import RedshiftHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet
from S3Handler import S3Handler

##############################################
# CONFIGURATION
##############################################
#DB Connection Config
conn_string = "dbname='tpch170' port='5439' user='rodrigo' password='Simply671' host='tpch-benchmark-cluster.cpvw2men8sxv.us-west-2.redshift.amazonaws.com'";
#conn_string = "dbname='tpch1' port='5439' user='rodrigo' password='Terry671' host='tpch1gb.cpvw2men8sxv.us-west-2.redshift.amazonaws.com'"; #Redshift Connection
#AWS Security Config - rodrigo iam
aws_access_key_id = "AKIAIPG7TI6LRZY7P3CA"
aws_secret_access_key = "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"
#Logging Config
s3Bucket = 'tpch170blazing'
version = "redshift ds2.xlarge"
nodeCount = "6 nodes"
logFile = "Log_08242016_11-15-AM.txt"
queryListFile = "queries.json"
#version = "redshift dc1.large"
#logFile = "redshiftLogFile.csv"
#nodeCount = "1 node"
#Run Config
#createTables = False
##############################################
# /CONFIGURATION
##############################################

def replace_date_delta(qstr):
    new_sql = qstr
    if qstr.find("$$") !=-1:
        sql_edit = qstr[qstr.find("$$"):(qstr.find("$$")+30)]
        [empty_block, edit_type, date_edit, low_bound, upper_bound] = sql_edit.split('$$')
        python_date = datetime.datetime.strptime(date_edit, '%Y%m%d').date()
        new_date = python_date - datetime.timedelta(days=(randint(int(low_bound), int(upper_bound))))
        new_sql = qstr.replace(sql_edit, str(new_date))
    return new_sql

dataPerNode = 0

#Initialize key objects for the Benchmark
rh = RedshiftHandler(conn_string, aws_access_key_id, aws_secret_access_key) #Connect to a Redshift Database
s3h = S3Handler(aws_access_key_id, aws_secret_access_key) #Connect to S3
comp = PostgresComparisonTestSet("", rh) #Start up Logging Tool

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
            [filePath, fileSize] = bucketDict[folder][1][uploadCount]
            S3filePath = "'" + 's3://' + s3Bucket + '/' + filePath + "'" #Setup path to S3 files
            dataPerNode += fileSize
            rh.dataLoader(S3filePath, folder[:-1])

    #Run queries
    #########################
    for query in queryList:
        qStr = queryList[query]['sql']
        qstr = replace_date_delta(qStr)
        comp.runAndValidateQuery(qStr, showVerboseQuery=True, fetch=False)


    #Log Results
    #########################
    memo = nodeCount + "|" + str(dataPerNode)
    comp.logResults(logFile, version, memo)

    uploadCount += 1 #This index iterates over the files inside the folders
    if uploadCount >= 1:
        break

rh.close()
