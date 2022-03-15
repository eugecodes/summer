import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet

if 'ph' not in locals():
    ph = PostgresHandler("host=169.53.37.156 port=5432 dbname=tpch50mb user=postgres password=terry")
    
if 'bh' not in locals():
    schema="integrationTests"
    db="tpch50Mb"
    bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)

if 'version' not in locals():
    version = 0

if 'memo' not in locals():
    memo = ""
    
if 'logFile' not in locals():
    logFile = ""
    
comp = PostgresComparisonTestSet(bh, ph)

print "**********************************************************************"
print "Starting simple aggregates tests"
print "**********************************************************************"

# count long
qStr = "select count(c_custkey) from customer"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# count double
qStr = "select count(c_acctbal) from customer"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
qStr = "select count(ps_supplycost) from partsupp"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# count string
qStr = "select count(c_name) from customer"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# count date
qStr = "select count(o_orderdate) from orders"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# max long
qStr = "select max(ps_availqty) from partsupp"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# max double
qStr = "select max(ps_supplycost) from partsupp"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# max date
qStr = "select max(o_orderdate) from orders"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# min long
qStr = "select min(ps_availqty) from partsupp"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# min double
qStr = "select min(ps_supplycost) from partsupp"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# min date
qStr = "select min(o_orderdate) from orders"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# sum long
qStr = "select sum(ps_availqty) from partsupp"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# sum double
qStr = "select sum(ps_supplycost) from partsupp"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)

# avg long
qStr = "select avg(ps_availqty) from partsupp"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)
# avg double
qStr = "select avg(ps_supplycost) from partsupp"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)


comp.report()
comp.logResults(logFile, version, memo)
