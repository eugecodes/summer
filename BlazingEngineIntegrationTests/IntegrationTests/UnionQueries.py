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
print "Starting Union Queries tests"
print "**********************************************************************"

qStr = "select r_regionkey as key, r_name as name from region union all select n_nationkey as key, n_name as name from nation order by name"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = "select ps_partkey, ps_availqty from partsupp where ps_availqty >= 9980 union all select ps_partkey, ps_availqty from partsupp where ps_partkey < 10 limit 2000"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select p_partkey as key, p_name as name from part where p_partkey in (2, 4, 6)
union all select p_partkey as key, p_name as name from part where p_partkey in (12, 14, 16)
union all select p_partkey as key, p_name as name from part where p_partkey in (102, 104, 106)"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select p_partkey as key, p_name as name from part where p_partkey in (2, 4, 6)
union all select ps_partkey as key, ps_comment as name from partsupp where ps_partkey in (12, 14, 16)
union all select partsupp.ps_partkey as key, part.p_name as name from part
inner join partsupp on partsupp.ps_partkey = part.p_partkey
where part.p_partkey in (102, 104, 106)"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select part.p_type, partsupp.ps_supplycost from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey where part.p_partkey < 15
union all select part.p_type, avg(partsupp.ps_supplycost) from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey where part.p_partkey < 15 group by part.p_type """
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select part.p_size, part.p_type, partsupp.ps_comment, partsupp.ps_supplycost from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey where part.p_partkey < 15
union all select sum(part.p_size), part.p_brand, part.p_brand, avg(partsupp.ps_supplycost) from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey where part.p_partkey < 15 group by part.p_brand """
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select o_orderpriority, o_orderdate, o_orderstatus from orders where o_orderkey < 10
union all select l_returnflag, l_shipdate, l_linestatus from lineitem where l_orderkey < 10"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """(select o_orderpriority, o_orderdate, o_orderstatus, o_orderkey from orders where o_orderkey < 100 order by o_orderdate, o_orderkey asc limit 15 offset 10)
union all (select l_returnflag, l_shipdate, l_linestatus, l_orderkey from lineitem where l_orderkey < 100 order by l_shipdate,  l_linenumber limit 10 offset 15)"""
altQstr = """(select o_orderpriority, o_orderdate, o_orderstatus, o_orderkey from orders where o_orderkey < 100 order by o_orderdate, o_orderkey asc limit 10, 15)
union all (select l_returnflag, l_shipdate, l_linestatus, l_orderkey from lineitem where l_orderkey < 100 order by l_shipdate,  l_linenumber limit 15, 10)"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, alternateQuery=altQstr)


"""
test union of nested and non nested queries
test nested query with child query having union
test nested query with child query having union which is a nested query

test union query that is nested and has string of length 1
test union query that is nested and has string of length > 1
test union query that is nested and has aggregate
test union query that is nested and has non aggreate number


"""


comp.report()
comp.logResults(logFile, version, memo)
