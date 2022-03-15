import sys
sys.path.append('../Classes')
from S3Handler import S3Handler

aws_access_key_id = "AKIAIPG7TI6LRZY7P3CA"
aws_secret_access_key = "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"

s3h = S3Handler(aws_access_key_id, aws_secret_access_key)

# s3h.setBucket("tpch1blazing")
s3h.setBucket("tpch170blazing")


tempList = []
tempList = s3h.getBucketList()
# print tempList

folderList = s3h.getBucketDict()


# print folderList.keys()
#
#
# print folderList


#
# print s3h.getFileCount('lineitem/')
#
# print s3h.getFileList('lineitem/')

bucketDict = s3h.getBucketDict()
uploadCount = 0

for folder in bucketDict:
    print bucketDict[folder][1][uploadCount]
uploadCount += 1
