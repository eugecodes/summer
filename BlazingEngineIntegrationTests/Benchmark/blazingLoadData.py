import sys
import subprocess
import time
import os
import shutil

sys.path.append('../Classes')
sys.path.append('./')
# from ImportAndTestingTools import setNodesInfo
from LocalBlazingHandler import LocalBlazingHandler
from boto.s3.connection import S3Connection

def getS3BucketList(bucket, aws_access_key_id, aws_secret_access_key ):
    #Returns a list of files and their respective size in bytes
    bucketList = []
    for key in bucket.list():
        bucketList.append([key.name.encode('utf-8'), key.size])
    return bucketList

def getFileCountList(fileDict):
    #Returns list of lengths of an inner array
    lengthList = []
    for table in fileDict:
        lengthList.append(len(table[1]))
    return lengthList



if 'bh' not in locals():
    schema="2"
    db="tpchtest"
    bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)

#Set values for S3 Connector
aws_access_key_id = 'AKIAIPG7TI6LRZY7P3CA'
aws_secret_access_key = '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'
s3Bucket = 'tpch170blazing'

conn = S3Connection(aws_access_key_id, aws_secret_access_key)
tpchBucket = conn.get_bucket(s3Bucket)

fileList = getS3BucketList(tpchBucket, aws_access_key_id, aws_secret_access_key)

#Build an array that holds directory, files, and file sizes
fileDict = []
folderCount = -1
for uploadFile in fileList:
    if uploadFile[0][-1:] == '/':
        fileDict.append([uploadFile[0], [], []])
        folderCount += 1

    else:
        fileDict[folderCount][1].append(uploadFile[0])
        fileDict[folderCount][2].append(uploadFile[1])


uploadCount = 0
lengthList = getFileCountList(fileDict)
while (uploadCount <= max(lengthList)):
    for table in fileDict:
        if uploadCount < len(table[1]):
            #Copy the data from S3
            key = tpchBucket.get_key(table[1][uploadCount])
            #key = tpchBucket.lookup(table[1][uploadCount])
            #Need to remove the front of the file path so I break up the string into a list and grab the second piece
            tempList = table[1][uploadCount].split('/')
            print "Copying file: " + str(tempList[1])
            loadStartTime = float(time.time())
            # key.get_contents_to_filename('/disk1/blazing/blazing-uploads/2/' +tempList[1])
            key.get_contents_to_filename('/home/ubuntu/' +tempList[1])
            shutil.move('/home/ubuntu/' + tempList[1], '/disk1/blazing/blazing-uploads/2/' + tempList[1])
            print "S3 file download took: " + str(float(time.time()) - loadStartTime)
            print "About to loadDataInfile: " + tempList[1]
            bh.delimiterStr = "'|'"
            loadStartTime = float(time.time())
            bh.loadDataInfile(tempList[1], tempList[0])
            print "load took: " + str(float(time.time()) - loadStartTime)
            print "Finished loadDataInfile."
            os.remove('/disk1/blazing/blazing-uploads/2/' + tempList[1])
    uploadCount +=1
    if uploadCount > 1:
        break
