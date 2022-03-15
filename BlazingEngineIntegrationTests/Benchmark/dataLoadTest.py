import sys
import psycopg2

#Connect to RedShift
connString = "dbname='tpch170' port='5439' user='rodrigo' password='Simply671' host='tpch-benchmark-cluster.cpvw2men8sxv.us-west-2.redshift.amazonaws.com'";
print "Connecting to database\n        ->%s" % (connString)
conn = psycopg2.connect(connString);
cursor = conn.cursor();

#Load File from S3 into Redshift
loadString = """COPY nation
FROM 's3://data-set-builder/bigTPCH/nation.tbl'
credentials 'aws_access_key_id=AKIAIPG7TI6LRZY7P3CA;aws_secret_access_key=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'
DELIMITER '|'
CSV;"""
print "Executing query\n        ->%s" % (loadString)
cursor.execute(loadString)

conn.commit();
conn.close();
