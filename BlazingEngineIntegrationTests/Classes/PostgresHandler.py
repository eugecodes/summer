# coding=utf-8
import psycopg2 as db
import time
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from StringIO import StringIO
import urllib


class PostgresHandler:
    'Connects to a postgres database and allows to run queries'

    def __init__(self, connectStr):
        self.connectStr = connectStr
        self.timeElapsed = 0
        self.results = 0
        self.statusMsg = ""
        self.tableNames = []

    # Main interaction functions

    def runQuery(self, query, **kwargs):
        # has three optional parameters
        verbose = kwargs.get("verbose", False)
        commit = kwargs.get("commit", False)
        showStatus = kwargs.get("status", False)
        fetchResults = kwargs.get("fetch", True)

        startTime = float(time.time())
        remote_connection = db.connect(self.connectStr)
        cursor = remote_connection.cursor()
        cursor.execute(query)
        self.timeElapsed = float(time.time()) - startTime
        self.statusMsg = cursor.statusmessage
        if fetchResults:
            try:
                self.results = cursor.fetchall()
            except:
                print "No results returned"
        else:
            self.results = None
            
        cursor.close()
        if verbose:
            print query
            print self.statusMsg
            try:
                for r in range(0,len(self.results)):
                    print self.results[r]
                print str(self.timeElapsed) + " seconds"
            except:
                print "There is no len when no results were returned"
        if showStatus and not verbose:
            print self.statusMsg
        if commit:
            remote_connection.commit()
        remote_connection.close()

    def getResultsArray(self):
        return self.results

    def describeDatabase(self):
        self.runQuery("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';", verbose = True)

    def getColumnNames(self, tableName):
        self.runQuery("select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = '" + tableName + "';")
        return self.results

    def describeTable(self, tableName):
        self.runQuery("select column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS where table_name = '" + tableName + "';", verbose = True)

    def describeDatabaseVerbose(self):
        self.runQuery("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
        tables = self.results
        strOut = ""
        for t in range(0,len(tables)):
            tableName = tables[t][0]
            numRows = self.__getColumnNumOfRowsStr(tableName)
            strOut = strOut + tableName + ": " + numRows + " rows \n "
            columns = self.getColumnNames(tableName)
            for c in range(0, len(columns)):
                strOut = strOut + columns[c][0] + " | "
            strOut = strOut + "\n \n \n"
        print strOut

    # Initialization functions
    def createDatabase(self, tempConnectStr, dbName):
        remote_connection = db.connect(tempConnectStr)
        remote_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = remote_connection.cursor()
        cursor.execute("create database " + dbName)
        cursor.close()
        remote_connection.close()

    def createTablesOnly(self, tableNameList, path, tableFileList, tableDescriptionList):
        self.tableNames = tableNameList
        for t in range(0,len(tableFileList)):
            if len(tableNameList) == 0:
                splitTableName = tableFileList[t].split(".")
                self.tableNames[t] = splitTableName[0]

            remote_connection = db.connect(self.connectStr)
            cursor = remote_connection.cursor()
            queryString = "create table " + self.tableNames[t] + " ( " + tableDescriptionList[t] + " ) "
            print queryString
            cursor.execute(queryString)
            cursor.close()


    def importDatabaseTables(self, tableNameList, path, tableFileList, tableDescriptionList):
        self.tableNames = tableNameList
        for t in range(0,len(tableFileList)):
            if len(tableNameList) == 0:
                splitTableName = tableFileList[t].split(".")
                self.tableNames[t] = splitTableName[0]

            remote_connection = db.connect(self.connectStr)
            cursor = remote_connection.cursor()
            cursor.execute("create table if not exists " + self.tableNames[t] + " ( " + tableDescriptionList[t] + " ) ")
            cursor.close()
            fileObject = open(path + tableFileList[t])
            self.__processFile(remote_connection, self.tableNames[t], fileObject)
            remote_connection.close()

    # Disposal functions
    def dropTables(self, tableNameList):
        for tableName in tableNameList:
            print "dropping table " + tableName
            self.runQuery("drop table if exists " + tableName + ";", commit = True, fetch=False)
            print self.statusMsg

    def dropDatabase(self, dbName):
        remote_connection = db.connect(self.connectStr)
        remote_connection.set_isolation_level(0)
        cursor = remote_connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS " + dbName)
        print cursor.statusmessage
        cursor.close()
        remote_connection.commit()
        remote_connection.close()

    # Support functions (private methods)
    def __processFile(self, remote_connection, tableName, fileObject):
        SQL_STATEMENT = """
            COPY %s FROM STDIN WITH
                CSV
                QUOTE '"'
                DELIMITER AS '|'
            """

        cursor = remote_connection.cursor()
        cursor.copy_expert(sql=SQL_STATEMENT % tableName, file=fileObject)
        remote_connection.commit()
        cursor.close()
        print "imported " + tableName

    def __getColumnNumOfRowsStr(self,tableName):
        columns = self.getColumnNames(tableName)
        self.runQuery("select count(" + columns[0][0] + ") from " + tableName)
        numStr = str(self.results[0][0])
        formatted = ""
        strLength = len(numStr)
        for x in range(0, strLength):
            if x % 3 == 0 and x != 0:
                formatted = numStr[strLength - x - 1] + "," + formatted
            else:
                formatted = numStr[strLength - x - 1] + formatted

        return formatted
