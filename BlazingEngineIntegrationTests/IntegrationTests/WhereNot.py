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
print "Starting Where Not tests"
print "**********************************************************************"

# where > long and > double
qStr = "select ps_partkey, ps_availqty from partsupp where not(ps_availqty > 7000 and ps_supplycost > 700) order by ps_partkey, ps_availqty limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where > long or > double
qStr = "select ps_partkey, ps_availqty from partsupp where not(ps_availqty > 7000 or ps_supplycost > 700) order by ps_partkey, ps_availqty limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where < long and >= date
qStr = "select o_orderkey from orders where not(o_custkey < 300 and o_orderdate >= '19980801') order by o_orderkey limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where < long or >= date
qStr = "select o_orderkey from orders where not(o_custkey < 100 or o_orderdate >= '19980801') order by o_orderkey limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where < double or < date
qStr = "select o_orderkey, o_orderstatus from orders where not(o_totalprice < 50000 or o_orderdate < '19920103') order by o_orderkey, o_orderstatus limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where < double and < date
qStr = "select o_orderkey, o_orderstatus from orders where not(o_totalprice < 50000 and o_orderdate < '19920103') order by o_orderkey, o_orderstatus limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where < date or >= date
qStr = "select o_orderkey, o_orderdate from orders where not(o_orderdate < '19920103' or o_orderdate >= '19980801') order by o_orderkey, o_orderdate limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where < long and >= long
qStr = "select ps_partkey, ps_availqty from partsupp where not(ps_availqty < 3 and ps_availqty >= 1) order by ps_partkey, ps_availqty limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where < long or = string
qStr = "select o_orderkey, o_orderstatus from orders where o_custkey < 10 or not(o_orderstatus = 'O') order by o_orderkey, o_orderstatus limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where < long and = string
qStr = "select o_orderkey, o_orderstatus from orders where not(o_custkey < 10) and o_orderstatus = 'O' order by o_orderkey, o_orderstatus limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where < long or != string
qStr = "select o_orderkey, o_orderstatus from orders where o_custkey < 10 or not(o_orderstatus != 'O') order by o_orderkey, o_orderstatus limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where < long and <> string
qStr = "select o_orderkey, o_orderstatus from orders where o_custkey < 10 and not(o_orderstatus <> 'O') order by o_orderkey, o_orderstatus limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)


# where < long and = string orderless limitless
qStr = "select o_orderkey, o_orderstatus from orders where not(o_custkey >= 100) and not(o_orderdate = '19920103')"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

# triple or
qStr = "select o_orderkey, o_orderstatus from orders where not(o_custkey < 10 or o_orderstatus = 'O') or o_orderstatus = 'F' order by o_orderkey, o_orderstatus limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# triple and
qStr = "select o_orderkey, o_orderstatus from orders where o_totalprice < 50000 and not(o_orderdate < '19980303' and o_orderdate > '19920103') order by o_orderkey, o_orderstatus limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# multiple combinations using parenthesis
qStr = "select o_orderkey, o_orderstatus from orders where not(o_custkey > 50 or (o_orderdate = '19920103' or o_orderdate = '19920105'))"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = "select o_orderkey, o_orderstatus from orders where not((o_custkey <= 500 and o_orderdate = '19920103') or o_orderdate <> '19920105')"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
    
qStr = "select o_orderkey, o_orderstatus from orders where not(o_custkey >= 100 and (o_orderstatus = 'O'  or (o_orderstatus = 'F' and o_custkey > 100)) and o_orderdate >= '19920105') order by o_orderkey limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)




comp.report()
comp.logResults(logFile, version,memo)
