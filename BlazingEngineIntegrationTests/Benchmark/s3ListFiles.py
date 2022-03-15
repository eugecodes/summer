from boto.s3.connection import S3Connection


def getS3BucketList(bucketName, aws_access_key_id, aws_secret_access_key ):
    #Returns a list of files and their respective size in bytes
    bucketList = []
    conn = S3Connection(aws_access_key_id, aws_secret_access_key)
    bucket = conn.get_bucket(bucketName)
    for key in bucket.list():
        bucketList.append([key.name.encode('utf-8'), key.size])
    return bucketList

def getFileCountList(fileDict):
    #Returns list of lengths of an inner array
    lengthList = []
    for table in fileDict:
        lengthList.append(len(table[1]))
    return lengthList




aws_access_key_id = 'AKIAIPG7TI6LRZY7P3CA'
aws_secret_access_key = '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'
s3Bucket ='tpch170blazing'
fileList = getS3BucketList(s3Bucket, aws_access_key_id, aws_secret_access_key)



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
            #print table[1][uploadCount]
            tempList = table[1][uploadCount].split('/')
            print tempList[0]
            # print tempList[1]
            # print table[1][uploadCount]
            # print table[0]
            # print len(table[0])
    uploadCount += 1
