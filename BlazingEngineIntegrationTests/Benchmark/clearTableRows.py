import sys
import psycopg2

#Connect to RedShift
connString = "dbname='tpch170' port='5439' user='rodrigo' password='Simply671' host='tpch-benchmark-cluster.cpvw2men8sxv.us-west-2.redshift.amazonaws.com'";
print "Connecting to database\n        ->%s" % (connString)
conn = psycopg2.connect(connString);
cursor = conn.cursor();


tableNameList = ["customer", "lineitem", "nation", "orders", "part", "partsupp", "region", "supplier"]

for table in tableNameList:
    queryString = "DELETE FROM " + table + ";"
    print "Executing query\n        ->%s" % (queryString)
    cursor.execute(queryString)

conn.commit();
conn.close();
