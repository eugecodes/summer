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
    bh = LocalBlazingHandler("127.0.0.1", 8890, schema, "tpch50Mb_xpart")

if 'version' not in locals():
    version = 0

if 'memo' not in locals():
    memo = ""
    
if 'logFile' not in locals():
    logFile = ""
    
comp = PostgresComparisonTestSet(bh, ph)


print "**********************************************************************"
print "Starting simple predicates tests"
print "**********************************************************************"

# where equals long
qStr = "select * from customer where c_custkey = 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where equals double
qStr = "select * from orders where o_totalprice = 82404.60"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where equals string
qStr = "select * from customer where c_name = 'Customer#000000009'"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where equals date
qStr = "select * from orders where o_orderdate = '19961201' order by o_orderkey limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where not equals long
qStr = "select o_orderkey from orders where o_shippriority != 0 order by o_orderkey limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where not equals double
qStr = "select o_orderkey from orders where o_totalprice != 82404.60 order by o_orderkey limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where not equals string
qStr = "select o_orderkey from orders where o_orderstatus != 'O' order by o_orderkey limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where not equals date
qStr = "select o_orderkey from orders where o_orderdate != '19961201' order by o_orderkey limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where > long
qStr = "select ps_partkey, ps_availqty from partsupp where ps_availqty > 9980 order by ps_partkey  limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where > double
qStr = "select ps_availqty, ps_supplycost from partsupp where ps_supplycost > 998 order by ps_partkey  limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where > date
qStr = "select o_orderkey, o_orderdate from orders where o_orderdate > '19980801' order by o_orderkey  limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where >= long
qStr = "select ps_partkey, ps_availqty from partsupp where ps_availqty >= 9980 order by ps_partkey  limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where >= double
qStr = "select ps_availqty, ps_supplycost from partsupp where ps_supplycost >= 998 order by ps_partkey  limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where >= date
qStr = "select o_orderkey, o_orderdate from orders where o_orderdate >= '19980801' order by o_orderkey  limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where < long
qStr = "select ps_partkey, ps_availqty from partsupp where ps_availqty < 2 order by ps_partkey  limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where < double
qStr = "select ps_availqty, ps_supplycost from partsupp where ps_supplycost < 2 order by ps_partkey  limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
# where < date
qStr = "select o_orderkey, o_orderdate from orders where o_orderdate < '19920103' order by o_orderkey  limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# where <= long
qStr = "select ps_partkey, ps_availqty from partsupp where ps_availqty <= 2 order by ps_partkey  limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# where <= double
qStr = "select ps_availqty, ps_supplycost from partsupp where ps_supplycost <= 2 order by ps_partkey  limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
# where <= date
qStr = "select o_orderkey, o_orderdate from orders where o_orderdate <= '19920103' order by o_orderkey  limit 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# should return empty
qStr = """select p_name from part
where  p_name = 'almond aquamarine mint misty red' and p_name = 'almond aquamarine frosted tomato green' and p_name = 'almond azure drab ghost mint'
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

# tests strings with spaces
qStr = """select p_name from part
where  p_name = 'almond aquamarine mint misty red' or p_name = 'almond aquamarine frosted tomato green' or p_name = 'almond azure drab ghost mint'
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)



comp.report()
comp.logResults(logFile, version, memo)
