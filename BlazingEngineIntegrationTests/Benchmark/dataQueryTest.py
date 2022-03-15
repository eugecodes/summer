import sys
import psycopg2
import time
import csv


def writeToLog(fileName, logList):
    with open(fileName, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(logList)



#Connect to RedShift
connString = "dbname='tpch170' port='5439' user='rodrigo' password='Simply671' host='tpch-benchmark-cluster.cpvw2men8sxv.us-west-2.redshift.amazonaws.com'";
print "Connecting to database\n        ->%s" % (connString)
conn = psycopg2.connect(connString);
cursor = conn.cursor();


version = "redshift ds2.xlarge"
nodeCount = "6 nodes"
fileName = "redshiftLogFile.csv"



#Query Table
queryString = """select * from lineitem limit 100000"""
print "Executing query\n        ->%s" % (queryString)
startTime = float(time.time())
cursor.execute(queryString)
timeElapsed = (float(time.time()) - startTime) * 1000
print timeElapsed


logList = [version, startTime, nodeCount, dataPerNode, queryString, "True", timeElapsed, 0, cursor.rowCount()]
writeToLog(fileName, logList)






conn.commit();
conn.close();
