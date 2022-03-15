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
    
if 'logFile' not in locals():
    logFile = ""
    
comp = PostgresComparisonTestSet(bh, ph)

print "**********************************************************************"
print " Starting TPCH query tests"
print "**********************************************************************"


qStr = """select l_returnflag, l_linestatus, sum(l_quantity) as sum_qty,
sum(l_extendedprice) as sum_base_price,
sum(l_discount) as sum_disc,
sum(l_tax) as sum_tax,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(l_orderkey) as count_order
from
lineitem
where
l_shipdate <= '19981001'
group by
l_returnflag,
l_linestatus
order by
l_returnflag,
l_linestatus;"""
comp.runAndValidateQuery(qStr, showVerboseFalse=True, precision=0.01)

qStr = """select min(partsupp.ps_supplycost) from partsupp
inner join supplier on supplier.s_suppkey = partsupp.ps_suppkey
inner join nation on supplier.s_nationkey = nation.n_nationkey
inner join region on nation.n_regionkey = region.r_regionkey
where region.r_name = 'EUROPE'"""
comp.runAndValidateQuery(qStr, showVerboseQuery=True, precision=0.01)

qStr = "select distinct p_type from part order by p_type desc limit 50"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, precision=0.01)

# returns 0 for a small dataset
qStr = """select supplier.s_acctbal, supplier.s_name, nation.n_name, part.p_partkey, part.p_mfgr, supplier.s_address, supplier.s_phone, supplier.s_comment
from supplier
inner join partsupp on supplier.s_suppkey = partsupp.ps_suppkey
inner join nation on supplier.s_nationkey = nation.n_nationkey
inner join region on nation.n_regionkey = region.r_regionkey
inner join part on part.p_partkey = partsupp.ps_partkey
where part.p_size = 15
and (part.p_type = 'ECONOMY ANODIZED BRASS' or part.p_type = 'ECONOMY BRUSHED BRASS' or part.p_type = 'ECONOMY BURNISHED BRASS' or part.p_type = 'ECONOMY PLATED BRASS' or part.p_type = 'ECONOMY POLISHED BRASS'
or part.p_type = 'LARGE ANODIZED BRASS' or part.p_type = 'LARGE BRUSHED BRASS' or part.p_type = 'LARGE BURNISHED BRASS' or part.p_type = 'LARGE PLATED BRASS' or part.p_type = 'LARGE POLISHED BRASS'
or part.p_type = 'SMALL ANODIZED BRASS' or part.p_type = 'SMALL BRUSHED BRASS' or part.p_type = 'SMALL BURNISHED BRASS' or part.p_type = 'SMALL PLATED BRASS' or part.p_type = 'SMALL POLISHED BRASS'
or part.p_type = 'STANDARD ANODIZED BRASS' or part.p_type = 'STANDARD BRUSHED BRASS' or part.p_type = 'STANDARD BURNISHED BRASS' or part.p_type = 'STANDARD PLATED BRASS' or part.p_type = 'STANDARD POLISHED BRASS')
and region.r_name = 'EUROPE' and partsupp.ps_supplycost = 1.01
order by supplier.s_acctbal desc, nation.n_name, supplier.s_name, part.p_partkey;"""
qStr = """select supplier.s_acctbal, supplier.s_name, nation.n_name, part.p_partkey, part.p_mfgr, supplier.s_address, supplier.s_phone, supplier.s_comment
from supplier
inner join partsupp on supplier.s_suppkey = partsupp.ps_suppkey
inner join nation on supplier.s_nationkey = nation.n_nationkey
inner join region on nation.n_regionkey = region.r_regionkey
inner join part on part.p_partkey = partsupp.ps_partkey
where part.p_size <= 15
and (part.p_type = 'ECONOMY ANODIZED BRASS' or part.p_type = 'ECONOMY BRUSHED BRASS' or part.p_type = 'ECONOMY BURNISHED BRASS' or part.p_type = 'ECONOMY PLATED BRASS' or part.p_type = 'ECONOMY POLISHED BRASS'
or part.p_type = 'LARGE ANODIZED BRASS' or part.p_type = 'LARGE BRUSHED BRASS' or part.p_type = 'LARGE BURNISHED BRASS' or part.p_type = 'LARGE PLATED BRASS' or part.p_type = 'LARGE POLISHED BRASS'
or part.p_type = 'SMALL ANODIZED BRASS' or part.p_type = 'SMALL BRUSHED BRASS' or part.p_type = 'SMALL BURNISHED BRASS' or part.p_type = 'SMALL PLATED BRASS' or part.p_type = 'SMALL POLISHED BRASS'
or part.p_type = 'STANDARD ANODIZED BRASS' or part.p_type = 'STANDARD BRUSHED BRASS' or part.p_type = 'STANDARD BURNISHED BRASS' or part.p_type = 'STANDARD PLATED BRASS' or part.p_type = 'STANDARD POLISHED BRASS')
and region.r_name = 'EUROPE' and partsupp.ps_supplycost <= 10.01
order by supplier.s_acctbal desc, nation.n_name, supplier.s_name, part.p_partkey;"""
# complex predicates with parenthesis and inner join do not work yet comp.runAndValidateQuery(qStr, showVerboseQuery=True, precision=0.01)


qStr="""select lineitem.l_orderkey, sum(lineitem.l_extendedprice) as sum_price, orders.o_orderdate, orders.o_shippriority
from customer
inner join orders on customer.c_custkey = orders.o_custkey
inner join lineitem on lineitem.l_orderkey = orders.o_orderkey
where customer.c_mktsegment = 'BUILDING'
and orders.o_orderdate < '19950315'
and lineitem.l_shipdate > '19950315'
group by lineitem.l_orderkey, orders.o_orderdate, orders.o_shippriority
order by sum_price desc, orders.o_orderdate;"""
qStr="""select lineitem.l_orderkey, sum(lineitem.l_extendedprice) as sum_price, orders.o_orderdate, orders.o_shippriority
from customer
inner join orders on customer.c_custkey = orders.o_custkey
inner join lineitem on lineitem.l_orderkey = orders.o_orderkey
where customer.c_mktsegment = 'BUILDING'
and orders.o_orderdate < '19950315'
and lineitem.l_shipdate > '19950315'
group by lineitem.l_orderkey, orders.o_orderdate, orders.o_shippriority
order by orders.o_orderdate, lineitem.l_orderkey;"""
# cannot currently order by an aggregate value
comp.runAndValidateQuery(qStr, showVerboseQuery=True, precision=0.01)

qStr = """select nation.n_name, sum(lineitem.l_extendedprice) as sum_extendedprice
from customer
inner join orders on customer.c_custkey = orders.o_custkey
inner join lineitem on lineitem.l_orderkey = orders.o_orderkey
inner join supplier on lineitem.l_suppkey = supplier.s_suppkey
inner join nation on supplier.s_nationkey = nation.n_nationkey
inner join region on nation.n_regionkey = region.r_regionkey
where supplier.s_nationkey = nation.n_nationkey
and region.r_name = 'ASIA;'
and orders.o_orderdate >= '19940101'
and orders.o_orderdate < '19950101'
group by nation.n_name order by sum_extendedprice desc;"""
qStr = """select nation.n_name, sum(lineitem.l_extendedprice) as sum_extendedprice
from customer
inner join orders on customer.c_custkey = orders.o_custkey
inner join lineitem on lineitem.l_orderkey = orders.o_orderkey
inner join supplier on lineitem.l_suppkey = supplier.s_suppkey
inner join nation on supplier.s_nationkey = nation.n_nationkey
inner join region on nation.n_regionkey = region.r_regionkey
where supplier.s_nationkey = nation.n_nationkey
and region.r_name = 'ASIA;'
and orders.o_orderdate >= '19940101'
and orders.o_orderdate < '19950101'
group by nation.n_name
order by nation.n_name;"""
# cannot currently order by an aggregate value
comp.runAndValidateQuery(qStr, showVerboseQuery=True, precision=0.01)

qStr = """select sum(l_extendedprice) as sum_exprice, sum(l_discount) as sum_discount
from lineitem
where l_shipdate >= '19940101'
and l_shipdate < '19950101'
and l_discount >= 0.05 and l_discount <= 0.07
and l_quantity < 24;"""
comp.runAndValidateQuery(qStr, showVerboseQuery=True, precision=0.01)

qStr = """select n1.n_name as supp_nation, n2.n_name as cust_nation,
lineitem.l_shipdate,  lineitem.l_extendedprice, lineitem.l_discount
from supplier
inner join lineitem on supplier.s_suppkey = lineitem.l_suppkey
inner join orders on orders.o_orderkey = lineitem.l_orderkey
inner join customer on customer.c_custkey = orders.o_custkey
inner join nation as n1 on supplier.s_nationkey = n1.n_nationkey
inner join nation as n2 on customer.c_nationkey = n2.n_nationkey
where n1.n_name = 'FRANCE' and n2.n_name = 'GERMANY'
and lineitem.l_shipdate >= '19950101' and lineitem.l_shipdate <= '19961231'"""
comp.runAndValidateQuery(qStr, showVerboseQuery=True, precision=0.01)
