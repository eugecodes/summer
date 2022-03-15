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
print "Starting Inner Join tests"
print "**********************************************************************"


# single joins
qStr = "select orders.o_totalprice, customer.c_name from orders inner join customer on orders.o_custkey = customer.c_custkey order by orders.o_orderkey limit 10"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
qStr = "select orders.o_totalprice, customer.c_name from orders inner join customer on orders.o_custkey = customer.c_custkey order by customer.c_name, orders.o_orderkey limit 10"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

if db=="tpch50Mb":
    qStr = "select orders.o_totalprice, customer.c_name from orders inner join customer on orders.o_custkey = customer.c_custkey where orders.o_clerk = 'Clerk#000000419'"
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = "select orders.o_orderstatus, customer.c_custkey from orders inner join customer on orders.o_custkey = customer.c_custkey where orders.o_clerk = 'Clerk#000000419' and customer.c_nationkey = 3"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
if db=="tpch50Mb":
    qStr = "select orders.o_orderstatus, customer.c_custkey from orders inner join customer on orders.o_custkey = customer.c_custkey where orders.o_clerk = 'Clerk#000000419' and customer.c_nationkey > 3 and customer.c_nationkey < 10"
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

    qStr = "select orders.o_orderstatus, customer.c_custkey from orders inner join customer on orders.o_custkey = customer.c_custkey where orders.o_clerk = 'Clerk#000000419' and customer.c_nationkey > 3 and customer.c_nationkey < 10 order by orders.o_custkey"
    comp.runAndValidateQuery(qStr, showVerboseFails=True)

qStr = """select orders.o_orderstatus, customer.c_custkey from orders
inner join customer on orders.o_custkey = customer.c_custkey
where orders.o_orderkey > 300 or customer.c_nationkey > 6
order by customer.c_custkey, orders.o_orderstatus  limit 30"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = """select orders.o_orderstatus, customer.c_custkey from orders
inner join customer on orders.o_custkey = customer.c_custkey
where orders.o_orderkey < 300 or customer.c_nationkey > 6
order by customer.c_custkey, orders.o_orderstatus  limit 30"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)



# multi joins, joined on common table
# with simple prediate
qStr = ("select part.p_name, part.p_type, partsupp.ps_supplycost, lineitem.l_discount from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_partkey = part.p_partkey where part.p_partkey < 3 limit 250000")
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

# with aggregates with simple predicate
qStr = ("select max(partsupp.ps_supplycost), count(distinct part.p_size), avg(lineitem.l_discount) from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_partkey = part.p_partkey where part.p_partkey < 20")
altqStr = ("select max(partsupp.ps_supplycost), count_distinct(part.p_size), avg(lineitem.l_discount) from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_partkey = part.p_partkey where part.p_partkey < 20")
#distinct currently not working comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01, alternateQuery=altqStr)

# with aggregates with simple predicate and group by
qStr = ("select max(partsupp.ps_supplycost), count(distinct part.p_size), avg(part.p_size), avg(lineitem.l_discount) from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_partkey = part.p_partkey where part.p_partkey < 20 group by lineitem.l_returnflag")
altqStr = ("select max(partsupp.ps_supplycost), count_distinct(part.p_size), avg(part.p_size), avg(lineitem.l_discount) from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_partkey = part.p_partkey where part.p_partkey < 20 group by lineitem.l_returnflag")
#distinct currently not working for joins with group by comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01, alternateQuery=altqStr)

# with aggregates with simple predicate and group by and order by
qStr = ("select lineitem.l_returnflag, max(partsupp.ps_supplycost), count(distinct part.p_size), avg(part.p_size), avg(lineitem.l_discount) from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_partkey = part.p_partkey where part.p_partkey < 20 group by lineitem.l_returnflag order by lineitem.l_returnflag")
altqStr = ("select lineitem.l_returnflag, max(partsupp.ps_supplycost), count_distinct(part.p_size), avg(part.p_size), avg(lineitem.l_discount) from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_partkey = part.p_partkey where part.p_partkey < 20 group by lineitem.l_returnflag order by lineitem.l_returnflag")
#distinct currently not working for joins with group by comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01, alternateQuery=altqStr)

# with complex predicates
qStr = """select part.p_name, part.p_type, partsupp.ps_supplycost, lineitem.l_discount from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey
inner join lineitem on lineitem.l_partkey = part.p_partkey
where (partsupp.ps_supplycost > 800 and lineitem.l_discount < 0.04)
or ((part.p_retailprice < 250 or partsupp.ps_supplycost < 200) and lineitem.l_discount > 0.06)
order by part.p_name, part.p_type, partsupp.ps_supplycost, lineitem.l_discount   limit 250"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=False)

if db=="tpch50Mb":
    # runs out of memory
    qStr = """select part.p_name, part.p_type, partsupp.ps_supplycost, lineitem.l_discount from part
    inner join partsupp on part.p_partkey = partsupp.ps_partkey
    inner join supplier on supplier.s_suppkey = partsupp.ps_suppkey
    inner join lineitem on lineitem.l_partkey = part.p_partkey
    where (partsupp.ps_supplycost > 800 and lineitem.l_discount < 0.04 and supplier.s_nationkey in (0, 2, 4, 9, 15, 20))
    or (((part.p_retailprice < 250 or partsupp.ps_supplycost < 200) and supplier.s_nationkey in (1, 2, 11, 12)) and lineitem.l_discount > 0.06)
    order by part.p_name, part.p_type, partsupp.ps_supplycost, lineitem.l_discount   limit 250"""
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=False)

# complex predicate whose results are easy to follow
qStr="""select nation.n_nationkey, nation.n_name, region.r_regionkey, region.r_name
from nation
inner join region on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >= 8 and ((region.r_regionkey = 1 and nation.n_nationkey < 24) or (region.r_regionkey = 3 and nation.n_nationkey <= 22))
order by nation.n_nationkey"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=False)
"""should get peru, romania and russia"""

# add more complex queries


# multi joins, joined by daisy chain
# with simple predicate and limit
qStr = ("select part.p_name, part.p_type, partsupp.ps_supplycost, lineitem.l_discount from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_suppkey = partsupp.ps_suppkey where  part.p_partkey < 10 and lineitem.l_orderkey < 50 limit 250")
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

# with compound predicate and with order by
qStr = ("select part.p_name, part.p_type, partsupp.ps_supplycost, lineitem.l_discount from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_suppkey = partsupp.ps_suppkey where lineitem.l_orderkey = 1 and part.p_partkey <= 80 order by part.p_name")
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# with aggregates with simple predicate and group by
qStr = ("select max(partsupp.ps_supplycost), count(distinct part.p_size), avg(lineitem.l_discount) from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_partkey = part.p_partkey where part.p_partkey < 20 group by lineitem.l_returnflag")
altqStr = ("select max(partsupp.ps_supplycost), count_distinct(part.p_size), avg(lineitem.l_discount) from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_suppkey = partsupp.ps_suppkey where part.p_partkey < 20 group by lineitem.l_returnflag")
#distinct currently not working for joins with group by comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01, alternateQuery=altqStr)

# with aggregates with simple predicate and group by and order by
qStr = ("select lineitem.l_returnflag, max(partsupp.ps_supplycost), count(distinct part.p_size), avg(lineitem.l_discount) from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_partkey = part.p_partkey where part.p_partkey < 20 group by lineitem.l_returnflag order by lineitem.l_returnflag")
altqStr = ("select lineitem.l_returnflag, max(partsupp.ps_supplycost), count_distinct(part.p_size), avg(lineitem.l_discount) from part " +
"inner join partsupp on part.p_partkey = partsupp.ps_partkey " +
"inner join lineitem on lineitem.l_suppkey = partsupp.ps_suppkey where part.p_partkey < 20 group by lineitem.l_returnflag order by lineitem.l_returnflag")
#distinct currently not working for joins with group by comp.runAndValidateQuery(qStr, showVerboseFails=True, precision=0.01, alternateQuery=altqStr)


qStr = ("""select customer.c_mktsegment, min(nation.n_nationkey), max(nation.n_nationkey), sum(nation.n_nationkey), avg(nation.n_nationkey), count(nation.n_nationkey) from region
inner join nation on region.r_regionkey = nation.n_regionkey
inner join customer on customer.c_nationkey = nation.n_nationkey
where (nation.n_regionkey = 2 or nation.n_regionkey = 3) and customer.c_custkey < 30
group by customer.c_mktsegment
order by customer.c_mktsegment asc""")
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr= ("""select customer.c_mktsegment, min(nation.n_nationkey), max(nation.n_nationkey), sum(nation.n_nationkey), avg(nation.n_nationkey), count(nation.n_nationkey),
min(region.r_regionkey), max(region.r_regionkey), sum(region.r_regionkey), avg(region.r_regionkey), count(region.r_regionkey),
sum(customer.c_acctbal), avg(customer.c_acctbal), count(customer.c_acctbal) from region
inner join nation on region.r_regionkey = nation.n_regionkey
inner join customer on customer.c_nationkey = nation.n_nationkey
group by customer.c_mktsegment""")
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# should return all nulls or none
qStr= ("""select customer.c_mktsegment, min(nation.n_nationkey), max(nation.n_nationkey), sum(nation.n_nationkey), avg(nation.n_nationkey), count(nation.n_nationkey),
min(region.r_regionkey), max(region.r_regionkey), sum(region.r_regionkey), avg(region.r_regionkey), count(region.r_regionkey),
sum(customer.c_acctbal), avg(customer.c_acctbal), count(customer.c_acctbal) from region
inner join nation on region.r_regionkey = nation.n_regionkey
inner join customer on customer.c_nationkey = nation.n_nationkey
where nation.n_nationkey is null
group by customer.c_mktsegment""")
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)


qStr = """select supplier.s_nationkey, part.p_size
from part
inner join partsupp on part.p_partkey = partsupp.ps_partkey
inner join supplier on supplier.s_suppkey = partsupp.ps_suppkey
group by supplier.s_nationkey, part.p_size
order by supplier.s_nationkey, part.p_size limit 30"""
comp.runAndValidateQuery(qStr, showVerboseFails=True)

comp.report()
comp.logResults(logFile, version, memo)
