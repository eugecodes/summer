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
print "Starting Nested Queries tests"
print "**********************************************************************"


qStr = """select manufacturer, maxPrice, avgSize from
(select avg(p_size) as avgSize, max(p_retailprice) as maxPrice, min(p_retailprice) as minPrice, p_mfgr as manufacturer from part group by p_mfgr) as partAnalysis
order by maxPrice desc
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=False, precision=0.01)

qStr = """select customer.c_name, custOrders.avgPrice, custOrders.numOrders from customer
inner join
(select o_custkey as o_custkey, avg(o_totalprice) as avgPrice, count(o_totalprice) as numOrders from orders
where o_custkey <= 100 group by o_custkey) as custOrders
on custOrders.o_custkey = customer.c_custkey
where customer.c_nationkey <= 5"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select partSuppTemp.partKey, partAnalysis.avgSize, supplier.name from
(select min(p_partkey) as partKey, avg(p_size) as avgSize, max(p_retailprice) as maxPrice, min(p_retailprice) as minPrice, p_mfgr as manufacturer from part group by p_mfgr) as partAnalysis
inner join (select ps_partkey as partKey, ps_suppkey as suppKey from partsupp where ps_availqty > 2) as partSuppTemp on partAnalysis.partKey = partSuppTemp.partKey
inner join (select s_suppkey as suppKey, s_name as name from supplier) as supplier on supplier.suppKey = partSuppTemp.suppKey"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)


qStr = """select avg(custKey), orderStatus from
(select tempOrders.orderstatus2 as orderStatus, customer.c_name as custName, customer.c_custkey as custKey from
(select o_orderstatus as orderstatus2, min(o_custkey) as o_custkey from orders group by o_orderstatus) as tempOrders
inner join customer on tempOrders.o_custkey = customer.c_custkey
where customer.c_nationkey > 6) as joinedTables
group by orderStatus"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select manufacturer, maxPrice, avgSize from
(select avg(p_size) as avgSize, max(p_retailprice) as maxPrice, min(p_retailprice) as minPrice, p_mfgr as manufacturer from part group by p_mfgr) as partAnalysis
order by maxPrice desc
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=False, precision=0.01)

qStr = """select customer.c_name, custOrders.avgPrice, custOrders.numOrders from customer
inner join
(select o_custkey as o_custkey, avg(o_totalprice) as avgPrice, count(o_totalprice) as numOrders from orders
where o_custkey <= 100 group by o_custkey) as custOrders
on custOrders.o_custkey = customer.c_custkey
where customer.c_nationkey <= 5"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select partSuppTemp.partKey, partAnalysis.avgSize, supplier.name from
(select min(p_partkey) as partKey, avg(p_size) as avgSize, max(p_retailprice) as maxPrice, min(p_retailprice) as minPrice, p_mfgr as manufacturer from part group by p_mfgr) as partAnalysis
inner join (select ps_partkey as partKey, ps_suppkey as suppKey from partsupp where ps_availqty > 2) as partSuppTemp on partAnalysis.partKey = partSuppTemp.partKey
inner join (select s_suppkey as suppKey, s_name as name from supplier) as supplier on supplier.suppKey = partSuppTemp.suppKey"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)


qStr = """select avg(custKey), orderStatus from
(select tempOrders.orderstatus2 as orderStatus, customer.c_name as custName, customer.c_custkey as custKey from
(select o_orderstatus as orderstatus2, min(o_custkey) as o_custkey from orders group by o_orderstatus) as tempOrders
inner join customer on tempOrders.o_custkey = customer.c_custkey
where customer.c_nationkey > 6) as joinedTables
group by orderStatus"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)


qStr = """select partSuppTemp.partKey, partAnalysis.avgSize, suppl.suppKey, suppl.name from
(select min(p_partkey) as partKey, avg(p_size) as avgSize, max(p_retailprice) as maxPrice, min(p_retailprice) as minPrice,
p_mfgr as manufacturer from part group by p_mfgr order by p_mfgr limit 10) as partAnalysis
inner join (select ps_partkey as partKey, ps_suppkey as suppKey from partsupp where ps_availqty > 2) as partSuppTemp
on partAnalysis.partKey = partSuppTemp.partKey
inner join (select s_suppkey as suppKey, s_name as name from supplier order by s_suppkey desc limit 500) as suppl
on suppl.suppKey = partSuppTemp.suppKey"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select partSuppTemp.partKey, partAnalysis.avgSize, suppl.suppKey, suppl.name from
(select min(p_partkey) as partKey, avg(p_size) as avgSize, max(p_retailprice) as maxPrice, min(p_retailprice) as minPrice,
p_mfgr as manufacturer from part group by p_mfgr order by p_mfgr limit 5) as partAnalysis
inner join (select ps_partkey as partKey, ps_suppkey as suppKey from partsupp where ps_availqty > 2) as partSuppTemp
on partAnalysis.partKey = partSuppTemp.partKey
inner join (select s_suppkey as suppKey, s_name as name from supplier order by s_suppkey desc limit 10) as suppl
on partSuppTemp.suppKey = suppl.suppKey"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# test nested query where the nested query results are empty


comp.report()
comp.logResults(logFile, version, memo)
