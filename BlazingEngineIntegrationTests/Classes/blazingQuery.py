import psycopg2 as db
import math

import requests

import datetime
import psycopg2 as db
import os
remote_connection = db.connect('host=169.53.37.156 port=5432 dbname=sec2 user=postgres password=terry')

cursor = remote_connection.cursor()


#get a list of all the tables

def importPostgreTableDataToBlazing(postgresTable,blazingTable,postgresIdColumn):
    f = open(blazingTable + '.csv', 'w')
    start = 0
    length = 10000
    lastSize = 1
    totalRows = 0
    while lastSize > 0:
#        query = "select * from " + postgresTable + " order by " + postgresIdColumn + " limit " + str(length) + " offset " + str(start)
        query = "select * from " + postgresTable + " limit " + str(length) + " offset " + str(start)
 
        print query
        cursor.execute(query)
        tables = cursor.fetchall()
        if(len(tables) > 0):
            writeBatchToFile(f,convertBatchToCsvString(tables))
        start += length
        lastSize = len(tables)
        totalRows = totalRows + lastSize
    print totalRows
    f.close()
    query = "load data infile " + os.path.basename(os.getcwd()) + "/" + blazingTable + ".csv into table " + blazingTable + " fields terminated by '|' enclosed by '\"' lines terminated by '\n'"
    blazingQuery(query)

"""
importPostgreTableDataToBlazing("document","document","document_id")


blazingTable = "document"
query = "load data infile " + os.path.basename(os.getcwd()) + "/" + blazingTable + ".csv into table " + blazingTable + " fields terminated by '|' enclosed by '\"' lines terminated by '\n'"
print query
blazingQuery(query)


cursor.execute("select avg(document_id),min(document_id),max(document_id), document_type from document group by document_type")
cursor.fetchall();

cursor.execute("select * from document where document_id = 4")
cursor.fetchall();

cursor.execute("select * from document limit 10")
cursor.fetchall();


convertBatchToCsvString(tables)
"""

def writeBatchToFile(file,batchString):
    file.write(batchString)


def convertBatchToCsvString(resultSet):
    resultString = ""
    for row in resultSet:
        resultString = resultString + convertPostgresRowToCsvString(row) + "\n"
    return resultString

def convertPostgresRowToCsvString(row):
    rowString = ""
    for column in row:
        rowString = rowString + postgresConvertValues(column) + "|"
    return rowString[:-1]

def postgresConvertValues(value):
    if(isinstance(value,datetime.datetime)):
        return str(value.year) + "-" + str(value.month) + "-" + str(value.day)
    elif(isinstance(value,datetime.date)):
        return str(value.year) + "-" + str(value.month) + "-" + str(value.day)
      
    elif(isinstance(value,bool)):
        if value == True:
            return "1"
        else:
            return "0"
    else:
        if(isinstance(value,basestring)):
            return '"' + value.replace("\r","") + '"'
        else:
            return str(value)



def blazingQuery(url,token,query,fileName):
    if ":8443" not in url:
        url = url.replace("/database/query",":8443/database/query")
    print url
    r = requests.post(url, data={'token': token, 'query': query, 'fileName': fileName})
    print r.text
    if r.text.startswith('<html>'):
        return [['error running query',r.text]]
    else:
        results = r.text
        results = results.replace("\r","")
        resultsArr = results.split("\'")
        for i in range(1,len(resultsArr),2):
            resultsArr[i].replace("\\n","$$$linebreak$$$")
            resultsArr[i].replace("|","$$$delim$$$")
        results = "'".join(resultsArr)
        start = results.index('"entity":',0,400) + 10
        end = len(results) -2;
        results = results[start:end]
        #results
        resultsArr = results.split("\\n")
        resultsArr
        if(len(resultsArr) >= 3):
            types = resultsArr[2].split("|")
            types
            #print resultsArr
            resultSet = []
            for i in resultsArr[3:]:
                if i != "":
                    rowSplit = i.split("|")
                    row = []
                    for j in range(0,len(rowSplit)):
                        if(types[j] == "string"):
                            row.append( rowSplit[j].replace("'","").replace("$$$linebreak$$$","\n").replace("$$$delim$$$","|"))
                        elif(types[j] == "long"):
                            row.append( long(rowSplit[j]))
                        elif(types[j] == "double"):
                            row.append( float(rowSplit[j]))
                        elif(types[j] == "date"):
                            dateString = rowSplit[j]
                            formattedDate = dateString[0:4] + "-" + dateString[4:6] + "-" + dateString[6:8]
                            row.append( formattedDate)
                        else:
                            print "could not find type: " + types[j]
                            row.append(rowSplit[j])
                    resultSet.append(row)
        else:
            return results
    return resultSet
