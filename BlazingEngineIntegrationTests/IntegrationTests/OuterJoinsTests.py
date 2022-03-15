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
print "Starting Outer Join tests"
print "**********************************************************************"


qStr = """select region.r_regionkey, region.r_name, nation.n_nationkey, nation.n_name, nation.n_comment from region
left outer join nation on region.r_regionkey = nation.n_regionkey
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select region.r_regionkey, region.r_name, nation.n_nationkey, nation.n_name, nation.n_comment from region
left outer join nation on region.r_regionkey = nation.n_regionkey
where region.r_regionkey <= 2
order by region.r_regionkey, nation.n_name
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)



qStr = """select customer.c_custkey, count(orders.o_orderkey) from customer
left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_nationkey = 3
group by customer.c_custkey limit 350000
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select count(orders.o_totalprice), min(orders.o_totalprice), max(orders.o_totalprice), sum(orders.o_totalprice), avg(orders.o_totalprice),
count(orders.o_orderkey), min(orders.o_orderkey), max(orders.o_orderkey), sum(orders.o_orderkey), avg(orders.o_orderkey),
min(orders.o_orderdate), max(orders.o_orderdate),
count(customer.c_custkey), min(customer.c_custkey), max(customer.c_custkey), sum(customer.c_custkey), avg(customer.c_custkey)
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_nationkey = 3
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select customer.c_custkey, customer.c_nationkey, orders.o_orderkey from customer
left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_custkey <= 10
order by customer.c_custkey, orders.o_orderkey
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

if db=="tpch50Mb":
    # code cannot support this for large dataset
    qStr = """select part.p_partkey, count(lineitem.l_linenumber) from part
    left outer join lineitem on part.p_partkey = lineitem.l_partkey
    where  part.p_partkey in (2, 4, 6)
    group by part.p_partkey
    order by part.p_partkey
    """
    comp.runAndValidateQuery(qStr, showVerboseFails=True)

    qStr = """select part.p_name, count(lineitem.l_linenumber) from part
    left outer join lineitem on lineitem.l_partkey = part.p_partkey
    where  part.p_partkey in (2, 4, 6)
    group by part.p_name
    order by part.p_name
    """
    comp.runAndValidateQuery(qStr, showVerboseFails=True)

    qStr = """select part.p_name, lineitem.l_linenumber, lineitem.l_returnflag from part
    left outer join lineitem on part.p_partkey = lineitem.l_partkey
    where  lineitem.l_returnflag in ('A', 'R')
    order by part.p_name, lineitem.l_linenumber, lineitem.l_returnflag limit 30
    """
    comp.runAndValidateQuery(qStr, showVerboseFails=True)


qStr = """select orders.o_orderdate, lineitem.l_linenumber, lineitem.l_quantity from orders
left outer join lineitem on orders.o_orderkey >= lineitem.l_orderkey
where orders.o_custkey = 1
order by orders.o_orderdate, lineitem.l_linenumber, lineitem.l_quantity limit 30"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select orders.o_orderdate, sum(lineitem.l_quantity) from orders
left outer join lineitem on orders.o_orderkey >= lineitem.l_orderkey
where orders.o_custkey = 1
group by orders.o_orderdate
order by orders.o_orderdate limit 30"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select orders.o_clerk, avg(lineitem.l_discount) from orders
left outer join lineitem on orders.o_orderkey <= lineitem.l_orderkey
where orders.o_custkey = 1
group by orders.o_clerk
order by orders.o_clerk limit 30"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)


qStr = """select part.p_name, partsupp.ps_partkey, partsupp.ps_suppkey from part
left outer join partsupp on part.p_partkey = partsupp.ps_partkey
inner join supplier on supplier.s_suppkey = partsupp.ps_suppkey
where supplier.s_acctbal > 1000
order by part.p_name, partsupp.ps_partkey, partsupp.ps_suppkey limit 50"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select part.p_name, partsupp.ps_partkey, partsupp.ps_suppkey from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey
left outer join supplier on supplier.s_suppkey = partsupp.ps_suppkey
where supplier.s_acctbal > 1000
order by part.p_name, partsupp.ps_partkey, partsupp.ps_suppkey limit 50"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select part.p_name, partsupp.ps_partkey, partsupp.ps_suppkey from part
left outer join partsupp on part.p_partkey = partsupp.ps_partkey
left outer join supplier on supplier.s_suppkey = partsupp.ps_suppkey
where supplier.s_acctbal > 1000
order by part.p_name, partsupp.ps_partkey, partsupp.ps_suppkey limit 50"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select count(part.p_partkey), min(part.p_partkey), max(part.p_partkey), sum(part.p_partkey), avg(part.p_partkey),
count(supplier.s_suppkey), min(supplier.s_suppkey), max(supplier.s_suppkey), sum(supplier.s_suppkey), avg(supplier.s_suppkey),
count(supplier.s_acctbal), min(supplier.s_acctbal), max(supplier.s_acctbal), sum(supplier.s_acctbal), avg(supplier.s_acctbal),
count(partsupp.ps_supplycost), min(partsupp.ps_supplycost), max(partsupp.ps_supplycost), sum(partsupp.ps_supplycost), avg(partsupp.ps_supplycost)
from part
left outer join partsupp on part.p_partkey = partsupp.ps_partkey
left outer join supplier on supplier.s_suppkey = partsupp.ps_suppkey
where supplier.s_acctbal > 1000
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)


qStr = """select supplier.s_nationkey, min(part.p_size), max(part.p_size), avg(part.p_size), sum(part.p_size), count(part.p_size),
min(supplier.s_acctbal), max(supplier.s_acctbal), avg(supplier.s_acctbal), sum(supplier.s_acctbal), count(supplier.s_acctbal),
min(partsupp.ps_availqty), max(partsupp.ps_availqty), avg(partsupp.ps_availqty), sum(partsupp.ps_availqty), count(partsupp.ps_availqty)
from part
left outer join partsupp on part.p_partkey = partsupp.ps_partkey
left outer join supplier on supplier.s_suppkey = partsupp.ps_suppkey
group by supplier.s_nationkey"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless = True, precision=0.01)

qStr = """select supplier.s_nationkey, min(part.p_size), max(part.p_size), avg(part.p_size), sum(part.p_size), count(part.p_size),
min(supplier.s_acctbal), max(supplier.s_acctbal), avg(supplier.s_acctbal), sum(supplier.s_acctbal), count(supplier.s_acctbal),
min(partsupp.ps_availqty), max(partsupp.ps_availqty), avg(partsupp.ps_availqty), sum(partsupp.ps_availqty), count(partsupp.ps_availqty)
from part
left outer join partsupp on part.p_partkey = partsupp.ps_partkey
left outer join supplier on supplier.s_suppkey = partsupp.ps_suppkey
group by supplier.s_nationkey
order by supplier.s_nationkey limit 50"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)

qStr = """select supplier.s_nationkey, min(part.p_size), max(part.p_size), avg(part.p_size), sum(part.p_size), count(part.p_size),
min(supplier.s_acctbal), max(supplier.s_acctbal), avg(supplier.s_acctbal), sum(supplier.s_acctbal), count(supplier.s_acctbal),
min(partsupp.ps_availqty), max(partsupp.ps_availqty), avg(partsupp.ps_availqty), sum(partsupp.ps_availqty), count(partsupp.ps_availqty)
from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey
left outer join supplier on supplier.s_suppkey = partsupp.ps_suppkey
group by supplier.s_nationkey
order by supplier.s_nationkey limit 50"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)

qStr = """select supplier.s_nationkey, part.p_size
from part
left outer join partsupp on part.p_partkey = partsupp.ps_partkey
left outer join supplier on supplier.s_suppkey = partsupp.ps_suppkey
group by supplier.s_nationkey, part.p_size
order by supplier.s_nationkey, part.p_size limit 30"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# these three together check the count and avg logic
qStr = """select supplier.s_nationkey, min(part.p_size), max(part.p_size), avg(part.p_size), sum(part.p_size), count(part.p_size),
min(supplier.s_acctbal), max(supplier.s_acctbal), avg(supplier.s_acctbal), sum(supplier.s_acctbal), count(supplier.s_acctbal),
min(partsupp.ps_availqty), max(partsupp.ps_availqty), avg(partsupp.ps_availqty), sum(partsupp.ps_availqty), count(partsupp.ps_availqty)
from part
left outer join partsupp on part.p_partkey = partsupp.ps_partkey
inner join supplier on supplier.s_suppkey = partsupp.ps_suppkey
group by supplier.s_nationkey
order by supplier.s_nationkey limit 50"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)
qStr = """select supplier.s_nationkey, min(part.p_size), max(part.p_size), avg(part.p_size), sum(part.p_size), count(part.p_size),
min(supplier.s_acctbal), max(supplier.s_acctbal), avg(supplier.s_acctbal), sum(supplier.s_acctbal),
min(partsupp.ps_availqty), max(partsupp.ps_availqty), avg(partsupp.ps_availqty), sum(partsupp.ps_availqty)
from part
left outer join partsupp on part.p_partkey = partsupp.ps_partkey
inner join supplier on supplier.s_suppkey = partsupp.ps_suppkey
group by supplier.s_nationkey
order by supplier.s_nationkey limit 50"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)
qStr = """select supplier.s_nationkey, min(part.p_size), max(part.p_size), avg(part.p_size), sum(part.p_size),
min(supplier.s_acctbal), max(supplier.s_acctbal), avg(supplier.s_acctbal), sum(supplier.s_acctbal),
min(partsupp.ps_availqty), max(partsupp.ps_availqty), avg(partsupp.ps_availqty), sum(partsupp.ps_availqty)
from part
left outer join partsupp on part.p_partkey = partsupp.ps_partkey
inner join supplier on supplier.s_suppkey = partsupp.ps_suppkey
group by supplier.s_nationkey
order by supplier.s_nationkey limit 50"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01)


qStr = """select part.p_name, count(lineitem.l_linenumber) from part
left outer join lineitem on part.p_partkey >= lineitem.l_partkey
where  part.p_partkey in (2, 4, 6)
group by part.p_name
order by part.p_name
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)


qStr = """select part.p_name, count(lineitem.l_linenumber) from part
left outer join lineitem on part.p_partkey <= lineitem.l_partkey
where  part.p_partkey in (2, 4, 6)
group by part.p_name
order by part.p_name
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)


qStr = """select nation.n_nationkey, nation.n_name,  nation.n_regionkey, customer.c_custkey, customer.c_nationkey
from nation
left outer join customer on nation.n_nationkey = customer.c_nationkey and nation.n_regionkey >= customer.c_custkey
order by nation.n_nationkey, nation.n_name,  nation.n_regionkey, customer.c_custkey, customer.c_nationkey limit 50
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)


qStr = """select nation.n_nationkey, nation.n_name,  nation.n_regionkey, customer.c_custkey, customer.c_nationkey
from nation
left outer join customer on nation.n_nationkey = customer.c_nationkey and nation.n_nationkey <= customer.c_custkey
order by nation.n_nationkey, nation.n_name,  nation.n_regionkey, customer.c_custkey, customer.c_nationkey limit 50
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select nation.n_nationkey, nation.n_name,  nation.n_regionkey, customer.c_custkey, customer.c_nationkey
from nation
left outer join customer on nation.n_regionkey <= customer.c_nationkey and nation.n_nationkey >= customer.c_nationkey
order by nation.n_nationkey, nation.n_name,  nation.n_regionkey, customer.c_custkey, customer.c_nationkey limit 50
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select nation.n_nationkey, nation.n_name,  nation.n_regionkey, customer.c_custkey, customer.c_nationkey
from nation
left outer join customer on nation.n_nationkey = customer.c_nationkey
left outer join supplier on nation.n_nationkey = supplier.s_nationkey and customer.c_custkey = supplier.s_suppkey and nation.n_regionkey <= supplier.s_nationkey
order by nation.n_nationkey, nation.n_name,  nation.n_regionkey, customer.c_custkey, customer.c_nationkey limit 50
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select nation.n_nationkey, nation.n_name,  nation.n_regionkey, customer.c_custkey, customer.c_nationkey
from nation
left outer join customer on nation.n_nationkey = customer.c_nationkey
left outer join supplier on nation.n_nationkey = supplier.s_nationkey and customer.c_custkey <= supplier.s_suppkey and nation.n_regionkey <= supplier.s_nationkey
order by nation.n_nationkey, nation.n_name,  nation.n_regionkey, customer.c_custkey, customer.c_nationkey limit 50
"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select orders.o_custkey, count(lineitem.l_linenumber), sum(lineitem.l_linenumber) from orders
left outer join lineitem on orders.o_orderkey = lineitem.l_orderkey and orders.o_custkey <= lineitem.l_linenumber
where orders.o_custkey <= 35
group by orders.o_custkey
order by orders.o_custkey"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)


# testing that predicates work on nulls
qSrt = """selelct customer.c_custkey, orders.o_orderkey from customer left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100 and orders.o_custkey > 1
order by customer.c_custkey, orders.o_orderkey"""
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=False, precision=0.01)

qSrt = """selelct customer.c_custkey, orders.o_orderkey from customer left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100 and orders.o_totalprice > 1
order by customer.c_custkey, orders.o_orderkey"""
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=False, precision=0.01)


comp.report()
comp.logResults(logFile, version, memo)
