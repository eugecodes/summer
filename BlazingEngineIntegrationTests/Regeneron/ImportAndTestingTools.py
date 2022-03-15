import os, errno



def setNodesInfo(nodesFilePath, nodeIPsIn, nodePortsIn):
    
    if nodesFilePath == "":
        return  # do nothing
    else:
        silentremove(nodesFilePath)
        with open(nodesFilePath, "w+") as f:
            for n in xrange(0,len(nodeIPsIn)):
                f.write(nodeIPsIn[n] + "|" + nodePortsIn[n] + "\n")
            
    


def readNodesFile(nodesFilePath, nodeIPs, nodePorts):
    
    if nodesFilePath == "":
        return  # do nothing
    else:
        with open(nodesFilePath, "r+") as f:
            
            allNodesInfo = f.read()
            
            nodesList = allNodesInfo.split()
            
            for n in xrange(0, len(nodesList)):
                nodeSplit = nodesList[n].split("|")
                if len(nodeSplit) == 2:
                    nodeIPs[n] = nodeSplit[0]
                    nodePorts[n] = nodeSplit[1]


            
            
            
            
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured
