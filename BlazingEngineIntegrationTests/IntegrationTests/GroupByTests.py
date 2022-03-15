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
print "Starting Group By tests"
print "**********************************************************************"

# group by string
# group by with count
qStr = "select count(o_orderkey) from orders group by o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
# group by with count itself
qStr = "select count(o_orderstatus) from orders group by o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
# group by with sum
qStr = "select sum(o_shippriority) from orders group by o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
# group by with avg(long)
qStr = "select avg(o_custkey) from orders group by o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# group by with avg(double)
qStr = "select avg(o_totalprice) from orders group by o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# group by with max
qStr = "select max(o_totalprice) from orders group by o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
# group by with min
qStr = "select min(o_custkey) from orders group by o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

# group by long
# group by with count
qStr = "select count(o_shippriority) from orders group by o_shippriority"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
# group by with sum
qStr = "select sum(o_shippriority) from orders group by o_shippriority"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
# group by with avg
qStr = "select avg(o_totalprice) from orders group by o_shippriority"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# group by with avg(long)
qStr = "select avg(o_custkey) from orders group by o_shippriority"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# group by with max
qStr = "select max(o_totalprice) from orders group by o_shippriority"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
# group by with min
qStr = "select min(o_custkey) from orders group by o_shippriority"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

# multiple aggregates
if db=="tpch50Mb":
# getting rounding errors on this one
    qStr = "select count(o_shippriority), sum(o_totalprice) from orders group by o_shippriority"
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
    
qStr = "select max(o_totalprice), min(o_totalprice), avg(o_totalprice) from orders group by o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# with predicates
qStr = "select avg(o_totalprice) from orders where o_orderstatus = 'O' group by o_orderpriority"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
qStr = "select sum(o_totalprice) from orders where o_orderdate >= '19980701' and o_orderdate < '19980706' group by o_orderdate"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
qStr = "select count(o_custkey) from orders where o_orderdate >= '19980701' and o_orderdate < '19980706' group by o_orderdate"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
qStr = "select count(distinct o_custkey) from orders where o_orderdate >= '19980701' and o_orderdate < '19980706' group by o_orderdate"
# group by with distinct not working right now comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, alternateQuery="select count_distinct(o_custkey) from orders where o_orderdate >= '19980701' and o_orderdate < '19980706' group by o_orderdate")

qStr = "select o_orderpriority, count(o_custkey) from orders where o_orderstatus = 'P' group by o_orderpriority"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
qStr = "select o_orderpriority, count(distinct o_custkey) from orders where o_orderstatus = 'P' group by o_orderpriority"
# group by with distinct not working right now comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01, alternateQuery="select o_orderpriority, count_distinct(o_custkey) from orders where o_orderstatus = 'P' group by o_orderpriority")
qStr = "select o_orderpriority, count(o_totalprice) from orders where o_orderstatus = 'P' group by o_orderpriority"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
qStr = "select o_shippriority, count(distinct o_totalprice) from orders where o_orderstatus = 'O' group by o_shippriority"
# group by with distinct not working right now comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01, alternateQuery="select o_shippriority, count_distinct(o_totalprice) from orders where o_orderstatus = 'O' group by o_shippriority")

# multiple aggregates, including count distinct
qStr = "select count(distinct o_custkey), sum(o_totalprice) from orders where o_orderdate >= '19980701' and o_orderdate < '19980706' group by o_orderdate"
# group by with distinct not working right now comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, alternateQuery="select count_distinct(o_custkey), sum(o_totalprice) from orders where o_orderdate >= '19980701' and o_orderdate < '19980706' group by o_orderdate")

# with order by's
qStr = "select o_orderstatus, max(o_totalprice), min(o_totalprice), avg(o_totalprice) from orders group by o_orderstatus order by o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)
qStr = "select o_orderdate, sum(o_totalprice) from orders where o_orderdate >= '19980701' and o_orderdate < '19980706' group by o_orderdate order by o_orderdate"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)
qStr = "select o_orderdate, avg(o_totalprice), count(o_totalprice) from orders where o_orderstatus = 'P' or o_orderdate < '19910406' group by o_orderdate order by o_orderdate limit 200"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)

# multiple combinations using parenthesis
qStr = "select count(distinct o_custkey), sum(o_totalprice) from orders where o_custkey <= 500 and (o_orderdate = '19920103' or o_orderdate = '19920105') group by o_orderdate"
# group by with distinct not working right now comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, alternateQuery="select count_distinct(o_custkey), sum(o_totalprice) from orders where o_custkey <= 500 and (o_orderdate = '19920103' or o_orderdate = '19920105') group by o_orderdate")
qStr = "select o_orderstatus, max(o_totalprice), min(o_totalprice) from orders where (o_custkey <= 500 and o_orderdate = '19920103') or o_orderdate = '19920105' group by o_orderstatus order by o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
qStr = "select o_orderdate, avg(o_totalprice), count(o_totalprice) from orders where o_custkey <= 500 and (o_orderstatus = 'O'  or (o_orderstatus = 'F' and o_custkey > 100)) and o_orderdate >= '19920105'  group by o_orderdate order by o_orderdate limit 200"
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)


comp.report()
comp.logResults(logFile, version, memo)
