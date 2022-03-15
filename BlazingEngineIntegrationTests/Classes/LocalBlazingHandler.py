# coding=utf-8
import socket
import shutil
import time

class LocalBlazingHandler:
    'Creates, connects and destroys databases'

    def __init__(self, sockIp, sockPort, schemaName, dbName):
        self.sockIp = sockIp
        self.sockPort = sockPort
        self.schemaName = schemaName
        self.dbName = dbName
        self.tableNames = []
        self.results = ""
        self.timeElapsed = 0
        self.blazingTimeElapsed = 0
        self.rowsReturned = 0
        self.blazingPath = "/disk1/blazing/blazing-uploads/"
        self.delimiterStr = "'|'"
        self.terminationStr = "'\n'"
        self.enclosedByStr = "'\"'"
        self.splitDelim = "┌∩┐(◣_◢)┌∩┐"
        self.limitDataFetch = False


    # Main interaction functions
    def runQuery(self, query, **kwargs):
        # optional parameters
        runRaw = kwargs.get("raw", False)
        verbose = kwargs.get("verbose", False)

        if runRaw:
            rawQueryEngineQuery = query
        else:
            rawQueryEngineQuery = self.schemaName + self.splitDelim + self.dbName + self.splitDelim + query

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.sockIp, self.sockPort))
        messageToEngine = "messageSize:" + str(len(rawQueryEngineQuery)) + ";dataSize:0;" + rawQueryEngineQuery
        startTime = float(time.time())
        sent = s.send(messageToEngine)
        if sent == 0:
            raise RuntimeError("socket connection broken")

        self.results = ""
        data = s.recv(10240)
        while data != "":
            self.results = self.results + data.decode('utf-8')
            if self.limitDataFetch:
                data = ""
            else:
                data = s.recv(10240)

        self.timeElapsed = float(time.time()) - startTime
        if verbose:
            print query
            print self.results
            print str(self.timeElapsed) + " seconds"


    def getResultsArray(self):
        results = self.results
        results = results.replace("\r","")
        resultsArr = results.split("\'")
        for i in range(1,len(resultsArr),2):
            resultsArr[i].replace("\n","$$$linebreak$$$")
            resultsArr[i].replace("|","$$$delim$$$")
        results = "'".join(resultsArr)
        #results
        resultsArr = results.split("\n")

        if(len(resultsArr) >= 1):
            timeAndRowsInfoSplit = resultsArr[0].split("|")
            if (len(timeAndRowsInfoSplit) == 4):
                self.blazingTimeElapsed = float(timeAndRowsInfoSplit[1])
                self.rowsReturned = float(timeAndRowsInfoSplit[3])
            else:
                self.blazingTimeElapsed = 0
                self.rowsReturned = 0

        if(len(resultsArr) >= 3):
            types = resultsArr[2].split("|")
            #print resultsArr
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
                                #dateString = rowSplit[j]
                                #formattedDate = dateString[0:4] + "-" + dateString[4:6] + "-" + dateString[6:8]
                                #row.append( formattedDate)
                            else:
                                row.append(rowSplit[j])
                    resultSet.append(row)
            return resultSet
        else:
            return results

    # Initialization functions
    def initializeDatabase(self, tableNameList, path, tableFileList, tableDescriptionList, **kwargs):

        createCompressed = kwargs.get("compressed", False)
        createSchema = kwargs.get("createSchema", True)
        createDatabase = kwargs.get("createDatabase", True)
        copyUploadFiles = kwargs.get("copyUploadFiles", True)

        if len(tableFileList) != len(tableDescriptionList) or len(tableNameList) != len(tableFileList):
            raise RuntimeError("table list and table description list are not the same size. Error in InitializeDatabase")

        if createSchema:
            self.runQuery("create schema " + self.schemaName, raw = True)
            self.__verifyQueryReturnedProperly("schema created")
        if createDatabase:
            self.runQuery(self.schemaName + self.splitDelim + "create database " + self.dbName, raw = True)
            self.__verifyQueryReturnedProperly("database created")

        self.tableNames = tableNameList
        for t in range(0,len(tableFileList)):
            if len(tableNameList) == 0:
                splitTableName = tableFileList[t].split(".")
                self.tableNames[t] = splitTableName[0]
            if createCompressed:
                self.runQuery(self.schemaName + self.splitDelim + self.dbName + self.splitDelim + "create compressed table " + self.tableNames[t] + " ( " + tableDescriptionList[t] + " ) ", raw = True)
            else:
                self.runQuery(self.schemaName + self.splitDelim + self.dbName + self.splitDelim +"create table " + self.tableNames[t] + " ( " + tableDescriptionList[t] + " ) ", raw = True)

            self.__verifyQueryReturnedProperly("created table " + self.tableNames[t])

            if (copyUploadFiles):
                shutil.copyfile(path + tableFileList[t], self.blazingPath + self.schemaName + "/" + tableFileList[t])
                self.loadDataInfile(tableFileList[t], self.tableNames[t])

    def loadDataInfile(self, fileName, tableName):
        print self.schemaName + self.splitDelim + self.dbName + self.splitDelim +"load data infile " + fileName + " into table " + tableName + " fields terminated by " + self.delimiterStr + " enclosed by " + self.enclosedByStr + " lines terminated by " + self.terminationStr
        self.runQuery(self.schemaName + self.splitDelim + self.dbName + self.splitDelim +"load data infile " + fileName + " into table " + tableName + " fields terminated by " + self.delimiterStr + " enclosed by " + self.enclosedByStr + " lines terminated by " + self.terminationStr, raw = True)
        self.__verifyQueryReturnedProperly("data imported")

    # Disposal functions
    def dropDatabase(self):
        self.runQuery("drop schema " + self.schemaName, raw = True)
        self.__verifyQueryReturnedProperly("schema dropped")

    # Support functions (private methods)

    def __verifyQueryReturnedProperly(self,valStr):
        if(self.results.find(valStr) == -1):
            raise RuntimeError("Did not work error was ==>" + self.results + " for validation string " + valStr)
