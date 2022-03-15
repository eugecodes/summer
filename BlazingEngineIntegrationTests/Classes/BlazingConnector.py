# coding=utf-8
import requests
import json

class BlazingResult(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
    
    def results_clean(self,j):
        self.__dict__ = json.loads(j)
           
class BlazingPyConnector:

    def __init__(self, host, username, password, database, **kwargs):
        self.host = host
        self.port = kwargs.get('port', '8443')
        self.username = username
        self.password = password
        self.database = database
        
    def connect(self):
        r = requests.post('https://'+self.host+':'+self.port+'/blazing-jdbc/register', data={'username':self.username, 'password':self.password, 'database':self.database}, verify=False)
        connection = r.content
        r = requests.post('https://'+self.host+':'+self.port+'/blazing-jdbc/query', data={'username':self.username, 'token':connection, 'query':'use database '+self.database}, verify=False)
        return connection
        
    def run(self, query, connection):
        r = requests.post('https://'+self.host+':'+self.port+'/blazing-jdbc/query', data={'username':self.username, 'token':connection, 'query':query}, verify=False)
        result_key = r.content
        r = requests.post('https://'+self.host+':'+self.port+'/blazing-jdbc/get-results', data={'username':self.username, 'token':connection, 'resultSetToken':result_key}, verify=False)
        result = BlazingResult(r.content)
        return result
        
bl = BlazingPyConnector('52.41.136.244','felipe@blazingdb.com','tester','emilse')
con = bl.connect()
result = bl.run("list tables",con)
print result.status