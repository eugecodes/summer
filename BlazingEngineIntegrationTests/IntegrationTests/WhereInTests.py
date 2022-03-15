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
print "Starting Where In tests"
print "**********************************************************************"

# where equals long
qStr = "select * from customer where c_custkey in (50, 51, 20, 60)"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
# where equals string
qStr = "select * from customer where c_name in ('Customer#000000009', 'Customer#000000080', 'Customer#000000001', 'Customer#0000000011')"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
if db=="tpch50Mb":
    # where equals date
    qStr = "select * from orders where o_orderdate in ('19961201', '19970102')"
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

# where equals long with order by
qStr = "select * from customer where c_custkey in (50, 51, 20, 60) order by c_custkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
# where equals string with order by
qStr = "select * from customer where c_name in ('Customer#000000009', 'Customer#000000080', 'Customer#000000001', 'Customer#0000000011')  order by c_custkey desc"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
if db=="tpch50Mb":
    # where equals date with order by
    qStr = "select * from orders where o_orderdate in ('19961201', '19970102') order by o_orderkey"
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = "select o_orderkey, o_orderstatus from orders where o_custkey <= 500 and (o_orderstatus in ('O', 'F')  or o_custkey > 100) and o_orderdate in ('19920105','19930105', '19940105') order by o_orderkey limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = "select o_orderpriority, count(o_custkey) from orders where o_orderstatus in ('P', 'O') group by o_orderpriority"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = ("""select max(partsupp.ps_supplycost), count(part.p_size), avg(lineitem.l_discount) from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey
inner join lineitem on lineitem.l_partkey = part.p_partkey
where part.p_partkey < 300 and partsupp.ps_availqty in (10, 1, 20, 100)""")
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)

qStr = """select part.p_name, part.p_type, partsupp.ps_supplycost, lineitem.l_discount from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey
inner join supplier on supplier.s_suppkey = partsupp.ps_suppkey
inner join lineitem on lineitem.l_partkey = part.p_partkey
where (partsupp.ps_supplycost > 800 and lineitem.l_discount < 0.04 and supplier.s_nationkey in (0, 2, 4, 9, 15, 20))
or ((part.p_retailprice < 250 or (partsupp.ps_supplycost < 200 and supplier.s_nationkey in (1, 2, 11, 12))) and lineitem.l_discount < 0.01)
order by part.p_name, part.p_type, partsupp.ps_supplycost, lineitem.l_discount   limit 25000"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)


qStr = """select part.p_name, lineitem.l_linenumber, lineitem.l_returnflag from part
inner join lineitem on part.p_partkey = lineitem.l_partkey
where  lineitem.l_returnflag in ('A', 'R')
order by part.p_name, lineitem.l_linenumber, lineitem.l_returnflag limit 30
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select region.r_regionkey, region.r_name, nation.n_nationkey, nation.n_name from nation
inner join region on nation.n_regionkey = region.r_regionkey
where region.r_name in ('AFRICA', 'ASIA')
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select part.p_name, lineitem.l_partkey, lineitem.l_linenumber, lineitem.l_returnflag from lineitem
inner join part on lineitem.l_partkey = part.p_partkey
where  part.p_name in ('almond aquamarine mint misty red', 'almond blush cyan misty mint')
order by part.p_name, lineitem.l_linenumber, lineitem.l_returnflag limit 30
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select part.p_name, lineitem.l_linenumber, lineitem.l_returnflag from lineitem
inner join part on lineitem.l_partkey = part.p_partkey
where  part.p_name in ('almond aquamarine mint misty red', 'almond aquamarine frosted tomato green', 'almond azure drab ghost mint')
order by part.p_name, lineitem.l_linenumber, lineitem.l_returnflag limit 30
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select part.p_name, lineitem.l_linenumber, lineitem.l_returnflag from lineitem
inner join part on lineitem.l_partkey = part.p_partkey
where  part.p_name = 'almond aquamarine mint misty red' or part.p_name = 'almond blush cyan misty mint'
order by part.p_name, lineitem.l_linenumber, lineitem.l_returnflag limit 30
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select part.p_name, lineitem.l_linenumber, lineitem.l_returnflag from lineitem
inner join part on lineitem.l_partkey = part.p_partkey
where  (part.p_name = 'almond aquamarine mint misty red' or part.p_name = 'almond aquamarine frosted tomato green' or part.p_name = 'almond azure drab ghost mint')
and lineitem.l_returnflag = 'N'
order by part.p_name, lineitem.l_linenumber, lineitem.l_returnflag limit 30
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

if db=="tpch50Mb":
    
    # currently code cant handle this one for large data
    qStr = """select part.p_name, lineitem.l_linenumber, lineitem.l_returnflag from part
    left outer join lineitem on part.p_partkey = lineitem.l_partkey
    where  lineitem.l_returnflag in ('A', 'R')
    order by part.p_name, lineitem.l_linenumber, lineitem.l_returnflag limit 30
    """
    comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select region.r_regionkey, region.r_name, nation.n_nationkey, nation.n_name from nation
left outer join region on nation.n_regionkey = region.r_regionkey
where region.r_name in ('AFRICA', 'ASIA')
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select part.p_name, lineitem.l_partkey, lineitem.l_linenumber, lineitem.l_returnflag from lineitem
left outer join part on lineitem.l_partkey = part.p_partkey
where  part.p_name in ('almond aquamarine mint misty red', 'almond blush cyan misty mint')
order by part.p_name, lineitem.l_linenumber, lineitem.l_returnflag limit 30
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select part.p_name, lineitem.l_linenumber, lineitem.l_returnflag from lineitem
left outer join part on lineitem.l_partkey = part.p_partkey
where  part.p_name in ('almond aquamarine mint misty red', 'almond aquamarine frosted tomato green', 'almond azure drab ghost mint')
order by part.p_name, lineitem.l_linenumber, lineitem.l_returnflag limit 30
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select part.p_name, lineitem.l_linenumber, lineitem.l_returnflag from lineitem
left outer join part on lineitem.l_partkey = part.p_partkey
where  part.p_name = 'almond aquamarine mint misty red' or part.p_name = 'almond blush cyan misty mint'
order by part.p_name, lineitem.l_linenumber, lineitem.l_returnflag limit 30
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select part.p_name, lineitem.l_linenumber, lineitem.l_returnflag from lineitem
left outer join part on lineitem.l_partkey = part.p_partkey
where  (part.p_name = 'almond aquamarine mint misty red' or part.p_name = 'almond aquamarine frosted tomato green' or part.p_name = 'almond azure drab ghost mint')
and lineitem.l_returnflag = 'N'
order by part.p_name, lineitem.l_linenumber, lineitem.l_returnflag limit 30
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select l_linenumber, l_returnflag from lineitem
where l_returnflag in ('A', 'R')
order by l_linenumber, l_returnflag limit 30
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select p_name from part
where  p_name in ('almond aquamarine mint misty red', 'almond blush cyan misty mint')
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select p_name from part
where  p_name in ('almond aquamarine mint misty red', 'almond aquamarine frosted tomato green', 'almond azure drab ghost mint')
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)


comp.report()
comp.logResults(logFile, version, memo)
