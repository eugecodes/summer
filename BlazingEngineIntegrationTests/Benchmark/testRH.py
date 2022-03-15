import sys
sys.path.append('../Classes')
from RedshiftHandler import RedshiftHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet

conn_string = "dbname='tpch1' port='5439' user='rodrigo' password='Terry671' host='tpch1gb.cpvw2men8sxv.us-west-2.redshift.amazonaws.com'";
aws_access_key_id = "AKIAIPG7TI6LRZY7P3CA"
aws_secret_access_key = "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"

rh = RedshiftHandler(conn_string, aws_access_key_id, aws_secret_access_key)

#rh.describeDatabase()
#
# rh.describeTable('customer')
# rh.describeTable('lineitem')
#
# rh.runQuery('select * from lineitem limit 10;', verbose=True)
#
# print rh.getResultsArray()
#
# print rh.getColumnNames('nation')

#
# tableNameList = ["test"]
# testDesc = "id INT, name VARCHAR(28), price FLOAT"
# tableDescriptionList = [testDesc]
# rh.createTablesOnly(tableNameList, tableDescriptionList)


# rh.runQuery('select * from lineitem limit 10;', verbose=True)

logFile = "redshiftHandlerTest.txt"
version = "dc1.large-tpch1"
memo = "Testing outto see if this can effectively log results with Redshift only."

comp = PostgresComparisonTestSet("", rh)

queryStr0 = "select * from lineitem limit 10;"
comp.runAndValidateQuery(queryStr0)

queryStr1 = "select * from customer limit 10;"
comp.runAndValidateQuery(queryStr1)

queryStr2 = "select * from orders limit 10;"
comp.runAndValidateQuery(queryStr2)

comp.logResults(logFile, version, memo)

rh.close() #Since we're only starting one connection, then you must close out your connection to Redshift.
