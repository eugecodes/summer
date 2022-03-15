import sys
# sys.path.append('../Classes')
# from PostgresHandler import PostgresHandler
# from LocalBlazingHandler import LocalBlazingHandler
from boto.s3.connection import S3Connection
import psycopg2
import pprint
from datetime import date, timedelta
import time
import csv


def writeToLog(fileName, logList):
    with open(fileName, 'a') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(logList)

def dataLoader(filePath, tableName, cursor):
    loadString = """COPY """ + tableName + """
    FROM '""" + filePath + """'
    credentials 'aws_access_key_id=AKIAIPG7TI6LRZY7P3CA;aws_secret_access_key=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'
    DELIMITER '|'
    CSV;"""
    print "Executing query\n        ->%s" % (loadString)
    startTime = float(time.time())
    cursor.execute(loadString)
    timeElapsed = (float(time.time()) - startTime) * 1000
    print timeElapsed

def runQuery(queryString, cursor, version, nodeCount, dataPerNode):
    print "Executing query\n        ->%s" % (queryString)
    startTime = float(time.time())
    cursor.execute(queryString)
    timeElapsed = (float(time.time()) - startTime) * 1000
    print timeElapsed
    logList = [version, startTime, nodeCount, dataPerNode, queryString, "True", timeElapsed, 0, cursor.rowcount]
    writeToLog(fileName, logList)


def getFileCountList(fileDict):
    lengthList = []
    for table in fileDict:
        lengthList.append(len(table[1]))
    return lengthList

def getS3BucketList(bucketName, aws_access_key_id, aws_secret_access_key ):
    bucketList = []
    conn = S3Connection(aws_access_key_id, aws_secret_access_key)
    bucket = conn.get_bucket(bucketName)
    for key in bucket.list():
        bucketList.append([key.name.encode('utf-8'), key.size])
    return bucketList


aws_access_key_id = 'AKIAIPG7TI6LRZY7P3CA'
aws_secret_access_key = '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'

#Connect to RedShift
#conn_string = "dbname='tpch170' port='5439' user='rodrigo' password='Simply671' host='tpch-benchmark-cluster.cpvw2men8sxv.us-west-2.redshift.amazonaws.com'";
conn_string = "dbname='tpch1' port='5439' user='rodrigo' password='Terry671' host='tpch1gb.cpvw2men8sxv.us-west-2.redshift.amazonaws.com'";



print "Connecting to database\n        ->%s" % (conn_string)
conn = psycopg2.connect(conn_string);
cursor = conn.cursor();

#For Building TPCH170
# path = 's3://tpch170blazing/'
# version = "redshift ds2.xlarge"
# nodeCount = "6 nodes"
# s3Bucket = 'tpch170blazing'
# fileList = getS3BucketList(s3Bucket, aws_access_key_id, aws_secret_access_key)
# dataPerNode = 0
# fileName = "redshiftLogFile.csv"

#For Building TPCH1
path = 's3://tpch1blazing/'
version = "redshift dc1.large"
nodeCount = "1 node"
s3Bucket = 'tpch1blazing'
fileList = getS3BucketList(s3Bucket, aws_access_key_id, aws_secret_access_key)
dataPerNode = 0
fileName = "redshiftLogFile.csv"

for file in fileList:
    dataLoader(path+file[0], file[0][:-4], cursor)

# Need this for large files where each file set has it's own folder
# fileDict = []
# folderCount = -1
# for uploadFile in fileList:
#     if uploadFile[0][-1:] == '/':
#         fileDict.append([uploadFile[0], [], []])
#         folderCount += 1
#
#     else:
#         fileDict[folderCount][1].append(path + uploadFile[0])
#         fileDict[folderCount][2].append(uploadFile[1])

# uploadCount = 0
# lengthList = getFileCountList(fileDict)
# while (uploadCount <= max(lengthList)):
#     for table in fileDict:
#         if uploadCount < len(table[1]):
#             dataLoader(table[1][uploadCount], table[0][:-1], cursor)
#             dataPerNode += table[2][uploadCount]


for file in fileList:
    dataLoader(path+file[0], file[0][:-4], cursor)


    # for table in fileDict:
    #     if uploadCount < len(table[1]):
    #         dataLoader(table[1][uploadCount], table[0][:-1], cursor)
    #         dataPerNode += table[2][uploadCount]
    #
    #
    #
    #
    #
    #
    #
    #
    # print "The data inside each node is : " + str(dataPerNode)
    # queryString = """
    #     SELECT l_returnflag,
    #     l_linestatus,
    #        SUM(l_quantity) AS sum_qty,
    #        SUM(l_extendedprice) AS sum_base_price,
    #        SUM(l_extendedprice*(1 - l_discount)) AS sum_disc_price,
    #        SUM(l_extendedprice*(1 - l_discount)*(1 + l_tax)) AS sum_charge,
    #        AVG(l_quantity) AS avg_qty,
    #        AVG(l_extendedprice) AS avg_price,
    #        AVG(l_discount) AS avg_disc,
    #        COUNT(*) AS count_order
    #     FROM lineitem
    #     WHERE l_shipdate <= DATE '1998-12-01'
    #     GROUP BY l_returnflag,
    #              l_linestatus
    #     ORDER BY l_returnflag,
    #              l_linestatus;"""
    # # runQuery(queryString, cursor, version, nodeCount, dataPerNode)
    #
    # queryString = """
    #     SELECT l_returnflag,
    #     l_linestatus,
    #        SUM(l_quantity) AS sum_qty,
    #        SUM(l_extendedprice) AS sum_base_price,
    #        AVG(l_quantity) AS avg_qty,
    #        AVG(l_extendedprice) AS avg_price,
    #        AVG(l_discount) AS avg_disc,
    #        COUNT(*) AS count_order
    #     FROM lineitem
    #     WHERE l_shipdate <= DATE '1998-12-01'
    #     GROUP BY l_returnflag,
    #              l_linestatus
    #     ORDER BY l_returnflag,
    #              l_linestatus;"""
    # # runQuery(queryString, cursor, version, nodeCount, dataPerNode)
    #
    # queryString = """
    #     SELECT s_acctbal,
    #        s_name,
    #        n_name,
    #        p_partkey,
    #        p_mfgr,
    #        s_address,
    #        s_phone,
    #        s_comment
    #     FROM part,
    #          supplier,
    #          partsupp,
    #          nation,
    #          region
    #     WHERE p_partkey = ps_partkey
    #     AND   s_suppkey = ps_suppkey
    #     AND   s_nationkey = n_nationkey
    #     AND   n_regionkey = r_regionkey
    #     AND   r_name = 'AMERICA'
    #     AND   ps_supplycost = (SELECT MIN(ps_supplycost)
    #                            FROM partsupp,
    #                                 supplier,
    #                                 nation,
    #                                 region
    #                            WHERE p_partkey = ps_partkey
    #                            AND   s_suppkey = ps_suppkey
    #                            AND   s_nationkey = n_nationkey
    #                            AND   n_regionkey = r_regionkey
    #                            AND   r_name = 'AMERICA')
    #     ORDER BY s_acctbal DESC,
    #              n_name,
    #              s_name,
    #              p_partkey;"""
    # # runQuery(queryString, cursor, version, nodeCount, dataPerNode)
    #
    # queryString = """
    #     SELECT l_orderkey,
    #     SUM(l_extendedprice) AS revenue,
    #         o_orderdate,
    #         o_shippriority
    #     FROM customer,
    #         orders,
    #         lineitem
    #     WHERE c_mktsegment = 'BUILDING'
    #     AND   c_custkey = o_custkey
    #     AND   l_orderkey = o_orderkey
    #     AND   o_orderdate < DATE '1998-12-01'
    #     AND   l_shipdate > DATE '1994-01-01'
    #     GROUP BY l_orderkey,
    #         o_orderdate,
    #         o_shippriority
    #     ORDER BY revenue DESC,
    #         o_orderdate;"""
    # # runQuery(queryString, cursor, version, nodeCount, dataPerNode)
    #
    # uploadCount +=1

conn.commit();
conn.close();
