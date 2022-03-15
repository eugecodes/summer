# coding=utf-8
import socket
import shutil
import time

class blazing_connect:

    def __init__(self, host, port, schema, database):
        self.host = host
        self.port = port
        self.schema = schema
        self.database = database
        self.splitDelim = "┌∩┐(◣_◢)┌∩┐"

    def execute(self, query, **kwargs):

        if(query.find("create")):
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

        self.results = ""
        data = s.recv(10240)
        while data != "":
            self.results = self.results + data.decode('utf-8')

            #if self.limitDataFetch:
            #    data = ""
            #else:

            data = s.recv(10240)

        self.timeElapsed = float(time.time()) - startTime

        #if verbose:

        print query
        print self.results
        print str(self.timeElapsed) + " seconds"
