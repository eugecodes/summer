# coding=utf-8
import socket
import shutil
import time

class connect:
    'Creates, connects and destroys databases'

    def __init__(self, host, database, username, password, **kwargs): #port, schema,
        self.host = host
        self.port = kwargs.get("port", 8890)
        self.schema = kwargs.get("schema", 6)
        self.database = database
        self.splitDelim = "┌∩┐(◣_◢)┌∩┐"


    # Main interaction functions
    def execute(self, query, **kwargs):
        results = ""
        timeElapsed = 0
        verbose = True

        if query.find("create") or query.find("drop"):
            rawQueryEngineQuery = query
        else:
            rawQueryEngineQuery = self.schema + self.splitDelim + self.database + self.splitDelim + query

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        messageToEngine = "messageSize:" + str(len(rawQueryEngineQuery)) + ";dataSize:0;" + rawQueryEngineQuery
        startTime = float(time.time())
        sent = s.send(messageToEngine)
        if sent == 0:
            raise RuntimeError("socket connection broken")

        results = ""
        data = s.recv(10240)
        while data != "":
            results = results + data.decode('utf-8')
            data = s.recv(10240)

        timeElapsed = float(time.time()) - startTime
        if verbose:
            print query
            print results
            print str(timeElapsed) + " seconds"

    
    
    def fetchall(self):
        results = results
        results = results.replace("\r","")
        resultsArr = results.split("\'")
        for i in range(1,len(resultsArr),2):
            resultsArr[i].replace("\n","$$$linebreak$$$")
            resultsArr[i].replace("|","$$$delim$$$")
        results = "'".join(resultsArr)
        resultsArr = results.split("\n")

        if(len(resultsArr) >= 3):
            types = resultsArr[2].split("|")
            resultSet = []
            for i in resultsArr[3:]:
                if i != "":
                    rowSplit = i.split("|")
                    row = []
                    for j in range(0,len(rowSplit)):
                        if (rowSplit[j] == "null"):
                            row.append("null")
                        else:
                            if(types[j] == "string"):
                                row.append( rowSplit[j].replace("'","").replace("$$$linebreak$$$","\n").replace("$$$delim$$$","|"))
                            elif(types[j] == "long"):
                                row.append( long(rowSplit[j]))
                            elif(types[j] == "double"):
                                row.append( float(rowSplit[j]))
                            elif(types[j] == "date"):
                                row.append(rowSplit[j])
                            else:
                                row.append(rowSplit[j])
                    resultSet.append(row)
            return resultSet
        else:
            return results
    
    