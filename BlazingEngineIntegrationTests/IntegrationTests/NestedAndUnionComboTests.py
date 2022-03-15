import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet

if 'ph' not in locals():
    ph = PostgresHandler("host=169.53.37.156 port=5432 dbname=tpch1gb user=postgres password=terry")
    
if 'bh' not in locals():
    schema="testCompSharedAll"
    db="tpch1Gb"
    # bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)
    bh = ""

if 'version' not in locals():
    version = 0

if 'memo' not in locals():
    memo = ""
    
if 'logFile' not in locals():
    logFile = ""
    
comp = PostgresComparisonTestSet(bh, ph)

print "**********************************************************************"
print "Starting Nested And Union Query Combination tests"
print "**********************************************************************"



qStr = """select type, avg(size) from
((select p_type as type, p_size as size from part where p_type = 'ECONOMY BRUSHED NICKEL' order by p_size limit 5)
union all (select p_type as type, p_size as size from part where p_type = 'ECONOMY BRUSHED COPPER' order by p_size limit 5)
union all (select p_type as type, p_size as size from part where p_type = 'STANDARD BRUSHED NICKEL' order by p_size limit 5)
union all (select p_type as type, p_size as size from part where p_type = 'STANDARD BRUSHED COPPER' order by p_size limit 5)) as thing
group by type"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select type, avg(size) from
((select p_size as size, p_type as type from part where p_type = 'ECONOMY BRUSHED NICKEL')
union all (select p_size as size, p_type as type from part where p_type = 'ECONOMY BRUSHED COPPER')
union all (select p_size as size, p_type as type from part where p_type = 'STANDARD BRUSHED NICKEL' )
union all (select p_size as size, p_type as type from part where p_type = 'STANDARD BRUSHED COPPER')) as thing
group by type"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """(select type, avg(size) from
((select p_type as type, p_size as size from part where p_type = 'ECONOMY BRUSHED NICKEL' order by p_size limit 5)
union all (select p_type as type, p_size as size from part where p_type = 'ECONOMY BRUSHED COPPER' order by p_size limit 5)
union all (select p_type as type, p_size as size from part where p_type = 'STANDARD BRUSHED NICKEL' order by p_size limit 5)
union all (select p_type as type, p_size as size from part where p_type = 'STANDARD BRUSHED COPPER' order by p_size limit 5)) as thing
group by type) union all
(select type, avg(size) from
((select p_type as type, p_size as size from part where p_type = 'ECONOMY BRUSHED NICKEL' order by p_size desc limit 5)
union all (select p_type as type, p_size as size from part where p_type = 'ECONOMY BRUSHED COPPER' order by p_size desc limit 5)
union all (select p_type as type, p_size as size from part where p_type = 'STANDARD BRUSHED NICKEL' order by p_size desc limit 5)
union all (select p_type as type, p_size as size from part where p_type = 'STANDARD BRUSHED COPPER' order by p_size desc limit 5)) as thing
group by type)"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)


qStr = """select s1, s2, d1, l1 from ((select o_orderpriority as s1, o_orderdate as d1, o_orderstatus as s2, o_orderkey as l1 from orders
where o_orderkey < 100 order by o_orderdate, o_orderkey asc limit 15 offset 10)
union all (select l_returnflag as s1, l_shipdate as d1, l_linestatus as s2, l_orderkey as l1 from lineitem
where l_orderkey < 100 order by l_shipdate,  l_linenumber limit 10 offset 15)) as data where l1 > 50 order by s1, s2, d1, l1"""
altQstr = """select s1, s2, d1, l1 from ((select o_orderpriority as s1, o_orderdate as d1, o_orderstatus as s2, o_orderkey as l1 from orders
where o_orderkey < 100 order by o_orderdate, o_orderkey asc limit 10, 15)
union all (select l_returnflag as s1, l_shipdate as d1, l_linestatus as s2, l_orderkey as l1 from lineitem
where l_orderkey < 100 order by l_shipdate,  l_linenumber limit 15, 10)) as data where l1 > 50 order by s1, s2, d1, l1"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, alternateQuery=altQstr)

qStr = """select s1, s2, d1, l1 from (
(select o_orderdate as d1, o_orderpriority as s1, o_orderstatus as s2, o_orderkey as l1 from orders where o_orderkey < 100)
union all
(select l_shipdate as d1, l_linestatus as s1, l_returnflag as s2, l_orderkey as l1 from lineitem where l_orderkey < 100)
) as data where l1 > 50 order by s1, s2, d1, l1"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """(select s1 as le_string, min(min_l1) as minmin, max(max_l1) as maxmax, avg(avg_l1) as avgavg from (
select s1, s2, d1, avg(l1) as avg_l1, min(l1) as min_l1, max(l1) as max_l1 from (
(select o_orderdate as d1, o_orderpriority as s1, o_orderstatus as s2, o_orderkey as l1 from orders where o_orderkey < 100)
union all
(select l_shipdate as d1, l_linestatus as s1, l_returnflag as s2, l_orderkey as l1 from lineitem where l_orderkey < 100)
) as data where l1 > 50 group by d1, s1, s2) as superCombo group by le_string)
union all
(select s2 as le_string, min(min_l1) as minmin, max(max_l1) as maxmax, avg(avg_l1) as avgavg from (
select s1, s2, d1, avg(l1) as avg_l1, min(l1) as min_l1, max(l1) as max_l1 from (
(select o_orderdate as d1, o_orderpriority as s1, o_orderstatus as s2, o_orderkey as l1 from orders where o_orderkey < 100)
union all
(select l_shipdate as d1, l_linestatus as s1, l_returnflag as s2, l_orderkey as l1 from lineitem where l_orderkey < 100)
) as data where l1 > 50 group by d1, s1, s2) as superCombo group by le_string)
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select part.p_type, partsupp.ps_supplycost from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey where part.p_partkey < 15
union all select part.p_type, avg(partsupp.ps_supplycost) from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey where part.p_partkey < 15 group by part.p_type """
# comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select part.p_size, part.p_type, partsupp.ps_comment, partsupp.ps_supplycost from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey where part.p_partkey < 15
union all select sum(part.p_size), part.p_brand, part.p_brand, avg(partsupp.ps_supplycost) from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey where part.p_partkey < 15 group by part.p_brand """
# comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select o_orderpriority, o_orderdate, o_orderstatus from orders where l_orderkey < 10
union all select l_returnflag, l_shipdate, l_linestatus from lineitem where l_orderkey < 10"""
# comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)


comp.report()
comp.logResults(logFile, version, memo)
