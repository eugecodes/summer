# coding=utf-8
import psycopg2 as db
import time
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from StringIO import StringIO
import urllib

class RedshiftHandler:
    'Connects to a Redshift database and allows to run queries'

    def __init__(self, connectStr, aws_access_key_id, aws_secret_access_key):
        self.connectStr = connectStr
        print "Connecting to database\n        ->%s" % (connectStr)
        self.remote_connection = db.connect(connectStr)
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.timeElapsed = 0
        self.results = 0
        self.statusMsg = ""
        self.tableNames = []

    def close(self):
        print "Closing connection to database\n        ->%s" % (self.connectStr)
        self.remote_connection.close()

    def runQuery(self, query, **kwargs):
        # has three optional parameters
        verbose = kwargs.get("verbose", False)
        commit = kwargs.get("commit", False)
        showStatus = kwargs.get("status", False)
        fetchResults = kwargs.get("fetch", True)

        #Establish the connection and instantiate the cursor object
        cursor = self.remote_connection.cursor()

        startTime = float(time.time()) #Start recording time after the connection is made
        cursor.execute(query)
        self.timeElapsed = float(time.time()) - startTime #Store the time elapsed
        self.statusMsg = cursor.statusmessage #Store the status message of the cursor object
        if fetchResults:
            self.results = cursor.fetchall()
        else:
            self.results = None
        cursor.close() #Deconstruct the cursor object
        #Print to console if verbose requested.
        if verbose:
            print query
            print self.statusMsg
            if fetchResults:
                for r in range(0,len(self.results)):
                    print self.results[r]
            print str(self.timeElapsed) + " seconds"
        if showStatus and not verbose:
            print self.statusMsg
        if commit:
            self.remote_connection.commit()
        #remote_connection.close() #Deconstruct the remote_connection object

    def getResultsArray(self):
        return self.results

    def describeDatabase(self):
        self.runQuery("SELECT DISTINCT tablename FROM pg_table_def WHERE schemaname = 'public' ORDER BY tablename;", verbose = True)

    def getColumnNames(self, tableName):
        self.runQuery("select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = '" + tableName  + "';")
        return self.results

    def describeTable(self, tableName):
        self.runQuery("select column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS where table_name = '" + tableName + "';", verbose = True)

    def createTablesOnly(self, tableNameList, tableDescriptionList):
        for table in tableNameList: #Iterates through all of the tables to be created
            queryString = "CREATE TABLE IF NOT EXISTS " + table + " ( " + tableDescriptionList[tableNameList.index(table)] + " ); "
            self.runQuery(queryString, verbose = True, fetch = False, commit = True)

    def dataLoader(self, S3filePath, tableName):
        queryString = "COPY " + tableName + " FROM " + S3filePath + " credentials 'aws_access_key_id="+ self.aws_access_key_id + ";aws_secret_access_key=" + self.aws_secret_access_key+ "' DELIMITER '|' CSV;"
        self.runQuery(queryString, verbose = True, fetch = False, commit = True)
