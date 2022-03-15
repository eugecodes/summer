# coding=utf-8
from boto.s3.connection import S3Connection
import os
import shutil
import time

class S3Handler:
    'Connects to an S3 account and enables a multitude of functions on S3'

    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.conn = S3Connection(aws_access_key_id,aws_secret_access_key)
        self.bucket = None
        self.bucketList = []
        self.bucketDict = {}

    def setBucket(self, bucketName):
        self.bucket = self.conn.get_bucket(bucketName)
        for key in self.bucket.list():
            self.bucketList.append([key.name.encode('utf-8'), key.size]) #building general bucket list
        tempBucketDict = {}
        for item in self.bucketList:
            if item[0][-1:] == '/':
                tempFileCount = 0
                tempFileList = []
                tempBucketDict[item[0]] = None
                tempFolderName = item[0]
            else:
                tempFileCount +=1
                tempFileList.append([item[0], item[1]])
                tempBucketDict[tempFolderName] = [tempFileCount, tempFileList]
        self.bucketDict = tempBucketDict

    def getBucketList(self):
        return self.bucketList

    def getBucketDict(self):
        return self.bucketDict

    def getFileCount(self, folderName):
        return self.bucketDict[folderName][0]

    def getFileList(self, folderName):
        return self.bucketDict[folderName][1]

    def getFolderList(self):
        folderList = []
        testDict = {}
        fileCount = 0
        tempFileList = []
        for item in self.bucketList:
            if item[0][-1:] == '/':
                folderList.append(item[0])
                fileCount = 0
                tempFileList = []
                testDict[item[0]] = None
                folderName = item[0]
            else:
                fileCount +=1
                tempFileList.append(item[0])
                testDict[folderName] = [fileCount, tempFileList]
        return testDict

    def downloadS3intoBHUploads(self, keyName, schema):
        key = self.bucket.get_key(keyName)
        print "Copying file: " + keyName
        loadStartTime = float(time.time())
        key.get_contents_to_filename('/home/ubuntu/' + keyName)
        shutil.move('/home/ubuntu/' + keyName, '/disk1/blazing/blazing-uploads/' + schema + '/' + keyName)
        print "S3 file download took: " + str(float(time.time()) - loadStartTime)

    def removeS3File(self, filePath):
        print "Removing file: " + filePath
        os.remove('/disk1/blazing/blazing-uploads/' + filePath)
