import sys
import subprocess
import time
import os

sys.path.append('../Classes')
sys.path.append('./')
from ImportAndTestingTools import setNodesInfo
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet


if 'bh' not in locals():
    schema="8"    'need to find out what this is for our schema. will probably be something like 1
    db="tpch200GB"
    # schema="testCompSharedAll"
    # db="tpch1Gb"
    bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)

if 'version' not in locals():
    version = 0

if 'memo' not in locals():
    memo = ""

if 'logFile' not in locals():
    logFile = ""



logFile = "./regeneronTestLog.txt"
version = "master 6/14/2016"

comp = PostgresComparisonTestSet(bh, "")

nodesFile = "/disk1/blazing/blazing/nodes.config"
# nodesFile = "/home/wmalpica/repos/nodes.config"


#Load Configuration
loadNodeIPs = ["52.40.211.73", "52.40.215.172", "52.27.199.62", "52.38.213.118", "52.27.38.240"]
loadNodePorts = ["8890", "8890", "8890", "8890", "8890"]

#Query 8 Node Configuration
node8IPs = ["52.40.211.73", "52.40.215.172", "52.27.199.62", "52.38.213.118", "52.27.38.240"]
node8Ports = ["8890", "8890", "8890", "8890", "8890"]

#Query 16 Node Configuration
node16IPs = ["52.40.211.73", "52.40.215.172", "52.27.199.62", "52.38.213.118", "52.27.38.240"]
node16Ports = ["8890", "8890", "8890", "8890", "8890"]





'setup load data config here!****************************************'

loadDataQuery = """load data infile reg.csv into table regeneronFlatTable fields terminated by ',' enclosed by '\"' lines terminated by '\n'"""




'****************************************'
'os.devnull is a location in the OS that writes to and does not take up any space
'****************************************'
FNULL = open(os.devnull, 'w')

startingIteration = 7
endingIteration = 13

for iteration in xrange(startingIteration, endingIteration):

    for numNodes in xrange(0, 5): 'do not need this for loop

        nodeIPsIn = [nodeIPs[0]]
        nodePortsIn = [nodePorts[0]]
    #    nodeIPsIn = [nodeIPs[numNodes]]
    #    nodePortsIn = [nodePorts[numNodes]]

        if numNodes + 1 > 1:
            for nodeInd in xrange(1, numNodes + 1):
                nodeIPsIn += [nodeIPs[nodeInd]]
                nodePortsIn += [nodePorts[nodeInd]]

        setNodesInfo(nodesFile, nodeIPsIn, nodePortsIn)
        print "$$$$$$$$$$$ testing on node: " + str(numNodes)


        p = subprocess.Popen(["Simplicity", "8890", "/disk1/blazing/blazing.conf"], stdout=FNULL, stderr=subprocess.STDOUT)
        print "Starting Blazing Service with subprocess %s" % p.pid
        time.sleep(2)

        memo = str(numNodes + 1) + " nodes|" + str(1.2*(iteration+1)) + " rows per node (millions)"
        print memo

        bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)
        bh.limitDataFetch = True
        comp = PostgresComparisonTestSet(bh, "")
    #    comp.runAndValidateQuery(queryStr0, showVerboseQuery=True)
    #    comp.runAndValidateQuery(queryStr1, showVerboseQuery=True)
    #    comp.runAndValidateQuery(queryStr2, showVerboseQuery=True)
    #    comp.runAndValidateQuery(queryStr3, showVerboseQuery=True)
    #    comp.runAndValidateQuery(queryStr4, showVerboseQuery=True)
        comp.runAndValidateQuery(queryStr0)
     #   time.sleep(2)
        comp.runAndValidateQuery(queryStr1)
     #   time.sleep(2)
        comp.runAndValidateQuery(queryStr2)
     #   time.sleep(2)
        comp.runAndValidateQuery(queryStr3)
     #   time.sleep(2)
        comp.runAndValidateQuery(queryStr4)


        comp.logResults(logFile, version, memo)

        p.terminate()
        returncode = p.wait()
        print "Returncode of subprocess: %s" % returncode
        time.sleep(1)


    p = subprocess.Popen(["Simplicity", "8890", "/disk1/blazing/blazing.conf"], stdout=FNULL, stderr=subprocess.STDOUT)
    print "About to loadDataInfile.    Starting Blazing Service with subprocess %s" % p.pid
    time.sleep(2)
    bh.delimiterStr = "','"
    loadStartTime = float(time.time())
    bh.loadDataInfile("reg.csv", "regeneronFlatTable")
    print "load took: " + str(float(time.time()) - loadStartTime)
#    time.sleep(900)
    p.terminate()
    returncode = p.wait()
    print "Finished loadDataInfile.     Returncode of subprocess: %s" % returncode
    time.sleep(1)
