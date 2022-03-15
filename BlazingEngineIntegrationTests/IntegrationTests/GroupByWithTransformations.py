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
print "Starting Group By With Aggretations and Transformations tests"
print "**********************************************************************"

# group by with count
qStr = "select count(o_orderkey) + o_custkey from orders group by o_custkey order by o_custkey limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=False)
# group by with count itself
qStr = "select o_custkey*o_custkey*count(o_custkey) from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where count is of double
qStr = "select count(o_orderkey)/o_custkey from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where count is of double
qStr = "select count(o_orderkey)*o_custkey from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# group by with sum
qStr = "select sum(o_orderkey) + o_custkey from orders group by o_custkey order by o_custkey limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=False)
# group by with sum itself
qStr = "select o_custkey*o_custkey*sum(o_custkey) from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where sum is of double
qStr = "select sum(o_totalprice)/o_custkey from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where sum is of double
qStr = "select sum(o_totalprice)*o_custkey from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# group by with max
qStr = "select max(o_orderkey) + o_custkey from orders group by o_custkey order by o_custkey limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=False)
# group by with max itself
qStr = "select o_custkey*o_custkey*max(o_custkey) from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where max is of double
qStr = "select max(o_totalprice)/o_custkey from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where max is of double
qStr = "select max(o_totalprice)*o_custkey from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# group by with min
qStr = "select min(o_orderkey) + o_custkey from orders group by o_custkey order by o_custkey limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=False)
# group by with min itself
qStr = "select o_custkey*o_custkey*min(o_custkey) from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where min is of double
qStr = "select min(o_totalprice)/o_custkey from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where min is of double
qStr = "select min(o_totalprice)*o_custkey from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# group by with avg
qStr = "select avg(o_orderkey) + o_custkey from orders group by o_custkey order by o_custkey limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=False, precision=0.01)
# group by with avg itself
qStr = "select o_custkey*o_custkey*avg(o_custkey) from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where avg is of double
qStr = "select avg(o_totalprice)/o_custkey from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where avg is of double
qStr = "select avg(o_totalprice)*o_custkey from orders where o_custkey < 100 group by o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# ************ same as above but also grouping by String
# group by with count
qStr = "select count(o_orderkey) + o_custkey from orders group by o_custkey, o_orderstatus order by o_custkey, o_orderstatus limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=False)
# group by with count itself
qStr = "select o_custkey*o_custkey*count(o_custkey) from orders where o_custkey < 100 group by o_custkey, o_clerk"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where count is of double
qStr = "select count(o_orderkey)/o_custkey from orders where o_custkey < 100 group by o_custkey, o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where count is of double
qStr = "select count(o_orderkey)*o_custkey from orders where o_custkey < 100 group by o_custkey, o_clerk"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# group by with sum
qStr = "select sum(o_orderkey) + o_custkey from orders group by o_custkey, o_clerk order by o_custkey, o_clerk limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# group by with sum itself
qStr = "select o_custkey*o_custkey*sum(o_custkey) from orders where o_custkey < 100 group by o_custkey, o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where sum is of double
qStr = "select sum(o_totalprice)/o_custkey from orders where o_custkey < 100 group by o_custkey, o_clerk"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where sum is of double
qStr = "select sum(o_totalprice)*o_custkey from orders where o_custkey < 100 group by o_custkey, o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# group by with max
qStr = "select max(o_orderkey) + o_custkey from orders group by o_clerk, o_custkey, o_orderstatus order by o_custkey, o_clerk, o_orderstatus  limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# group by with max itself
qStr = "select o_custkey*o_custkey*max(o_custkey) from orders where o_custkey < 100 group by o_custkey, o_clerk, o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where max is of double
qStr = "select max(o_totalprice)/o_custkey from orders where o_custkey < 100 group by o_orderstatus, o_clerk, o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where max is of double
qStr = "select max(o_totalprice)*o_custkey from orders where o_custkey < 100 group by o_custkey, o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# group by with min
qStr = "select min(o_orderkey) + o_custkey from orders group by o_custkey, o_clerk order by o_clerk, o_custkey limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# group by with min itself
qStr = "select o_custkey*o_custkey*min(o_custkey) from orders where o_custkey < 100 group by o_custkey, o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where min is of double
qStr = "select min(o_totalprice)/o_custkey from orders where o_custkey < 100 group by o_custkey, o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where min is of double
qStr = "select min(o_totalprice)*o_custkey from orders where o_custkey < 100 group by o_custkey, o_clerk"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# group by with avg
qStr = "select avg(o_orderkey) + o_custkey from orders group by o_clerk, o_custkey, o_orderstatus order by o_orderstatus, o_custkey, o_clerk limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# group by with avg itself
qStr = "select o_custkey*o_custkey*avg(o_custkey) from orders where o_custkey < 100 group by o_custkey, o_clerk, o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where avg is of double
qStr = "select avg(o_totalprice)/o_custkey from orders where o_custkey < 100 group by o_custkey, o_clerk"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)
# where avg is of double
qStr = "select avg(o_totalprice)*o_custkey from orders where o_custkey < 100 group by o_clerk, o_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)


# group by without aggregations
qStr = """select ps_partkey*ps_suppkey, ps_partkey/ps_suppkey, ps_suppkey + ps_partkey,  ps_suppkey - ps_partkey, ps_suppkey * ps_suppkey, ps_partkey * ps_partkey
 from partsupp where ps_partkey < 100 group by ps_partkey, ps_suppkey """
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select o_totalprice*o_custkey, o_totalprice/o_custkey, o_custkey + o_totalprice,  o_custkey - o_totalprice, o_custkey * o_custkey, o_totalprice * o_totalprice
 from orders where o_custkey < 100 group by o_totalprice, o_custkey """
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)


# lets make sure that all aggs have correct output when all agged values are null
qStr = "select  o_orderstatus, count(o_custkey), count(nullif(o_custkey, 5)), min(nullif(o_custkey, 5)), max(nullif(o_custkey, 5)), sum(nullif(o_custkey, 5)), avg(nullif(o_custkey, 5)) from orders where o_custkey = 5 group by o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select orders.o_orderstatus, count(customer.c_nationkey), count(nullif(customer.c_nationkey, 3)), min(nullif(customer.c_nationkey, 3)), max(nullif(customer.c_nationkey, 3)), sum(nullif(customer.c_nationkey, 3)), avg(nullif(customer.c_nationkey, 3))
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
 where  customer.c_nationkey = 3
 group by orders.o_orderstatus"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)


comp.report()
comp.logResults(logFile, version, memo)
