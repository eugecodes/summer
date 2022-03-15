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
print "*****************Starting predicates with aggregates tests*********************"
print "**********************************************************************"


# where = long
qStr = "select count(ps_partkey), avg(ps_availqty) from partsupp where ps_availqty = 9980"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where = double
qStr = "select sum(ps_availqty), avg(ps_supplycost) from partsupp where ps_supplycost = 998"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.1)
# where = date
qStr = "select max(o_totalprice), min(o_orderdate) from orders where o_orderdate = '19980801'"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where = string
qStr = "select count(o_orderkey) from orders where o_orderstatus = 'O'"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where <> long
qStr = "select count(ps_partkey), avg(ps_availqty) from partsupp where ps_availqty <> 9980"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.1)
# where <> double
qStr = "select sum(ps_availqty), avg(ps_supplycost) from partsupp where ps_supplycost <> 998"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.1)
# where <> date
qStr = "select max(o_totalprice), min(o_orderdate) from orders where o_orderdate <> '19980801'"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where <> string
qStr = "select count(o_orderkey) from orders where o_orderstatus <> 'O'"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where > long
qStr = "select count(ps_partkey), avg(ps_availqty) from partsupp where ps_availqty > 9980"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.1)
# where > double
qStr = "select sum(ps_availqty), avg(ps_supplycost) from partsupp where ps_supplycost > 998"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.1)
# where > date
qStr = "select max(o_totalprice), min(o_orderdate) from orders where o_orderdate > '19980801'"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where >= long
qStr = "select count(ps_partkey), avg(ps_availqty) from partsupp where ps_availqty >= 9980"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.1)
# where >= double
qStr = "select sum(ps_availqty), avg(ps_supplycost) from partsupp where ps_supplycost >= 998"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.1)
# where >= date
qStr = "select max(o_totalprice), min(o_orderdate) from orders where o_orderdate >= '19980801'"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where < long
qStr = "select count(ps_partkey), avg(ps_availqty) from partsupp where ps_availqty < 2"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.1)
# where < double
qStr = "select sum(ps_availqty), avg(ps_supplycost) from partsupp where ps_supplycost < 2"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.1)
# where < date
qStr = "select max(o_totalprice), min(o_orderdate) from orders where o_orderdate < '19920103'"
comp.runAndValidateQuery(qStr, showVerboseFails=True)



comp.report()
comp.logResults(logFile, version, memo)
