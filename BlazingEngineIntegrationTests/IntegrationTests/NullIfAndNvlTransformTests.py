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
print "Starting NULLIF and NVL Transformations tests"
print "**********************************************************************"

# nullif for dates not working yet
# qStr = """select nullif(o_orderkey, 5), nullif(o_orderdate, '19931014'), nullif(o_orderstatus, 'O'), nullif(o_totalprice, 193846.25), nullif(o_clerk, 'Clerk#000000955') from orders where o_orderkey <= 10"""
qStr = """select nullif(o_orderkey, 5), nullif(o_orderstatus, 'O'), nullif(o_totalprice, 193846.25), nullif(o_clerk, 'Clerk#000000955') from orders where o_orderkey <= 10"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# qStr = """select nullif(orders.o_orderkey, orders.o_custkey % 5), nullif(orders.o_orderstatus, lineitem.l_linestatus),
# nullif(orders.o_totalprice, lineitem.l_extendedprice * (1-lineitem.l_discount) * (1 + lineitem.l_tax)),
# nullif(orders.o_orderpriority, lineitem.l_shipmode), nullif(orders.o_orderdate, lineitem.l_commitdate)
# from orders inner join lineitem on lineitem.l_orderkey = orders.o_orderkey
# where orders.o_orderkey <= 80"""
qStr = """select nullif(orders.o_orderkey, orders.o_custkey % 5), nullif(orders.o_orderstatus, lineitem.l_linestatus),
nullif(orders.o_totalprice, lineitem.l_extendedprice * (1-lineitem.l_discount) * (1 + lineitem.l_tax)),
nullif(orders.o_orderpriority, lineitem.l_shipmode)
from orders inner join lineitem on lineitem.l_orderkey = orders.o_orderkey
where orders.o_orderkey <= 80"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# qStr = """select nvl(orders.o_orderkey, 100), nvl(orders.o_totalprice, 0.01), nvl(orders.o_orderstatus, 'nulo'),
# nvl(orders.o_clerk, 'El Sr. Nulo'), nvl(orders.o_orderdate, '19900101')
# from customer
# left outer join orders on customer.c_custkey = orders.o_custkey
#  where  customer.c_nationkey = 3"""
altQStr = """select nvl(orders.o_orderkey, 100), nvl(orders.o_totalprice, 0.01), nvl(orders.o_orderstatus, 'nulo'),
nvl(orders.o_clerk, 'El Sr. Nulo')
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
 where  customer.c_nationkey = 3 and customer.c_custkey < 500"""
qStr = """select COALESCE(orders.o_orderkey, 100), COALESCE(orders.o_totalprice, 0.01), COALESCE(orders.o_orderstatus, 'nulo'),
COALESCE(orders.o_clerk, 'El Sr. Nulo')
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
 where  customer.c_nationkey = 3 and customer.c_custkey < 500"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01, alternateQuery=altQStr)

altQStr = """select nvl(orders.o_orderkey, customer.c_custkey), nvl(orders.o_totalprice, customer.c_acctbal),
nvl(orders.o_orderstatus, customer.c_mktsegment), nvl(orders.o_clerk, customer.c_name)
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
 where  customer.c_nationkey = 3 and customer.c_custkey < 500"""
qStr = """select COALESCE(orders.o_orderkey, customer.c_custkey), COALESCE(orders.o_totalprice, customer.c_acctbal),
COALESCE(orders.o_orderstatus, customer.c_mktsegment), COALESCE(orders.o_clerk, customer.c_name)
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
 where  customer.c_nationkey = 3 and customer.c_custkey < 500"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01, alternateQuery=altQStr)


#  add tests with nested nvl and nested nullif and nullif and nvl combined
altQStr = """select customer.c_custkey, nvl(nullif(orders.o_orderkey % 6, 5),nvl(orders.o_custkey,123456)), nullif(nullif(orders.o_orderkey % 6, 777), nullif(555, orders.o_orderkey % 7))
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
 where  customer.c_nationkey = 3 and customer.c_custkey < 500 order by customer.c_custkey"""
qStr = """select customer.c_custkey, COALESCE(nullif(orders.o_orderkey % 6, 5),COALESCE(orders.o_custkey,123456)), nullif(nullif(orders.o_orderkey % 6, 777), nullif(555, orders.o_orderkey % 7))
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
 where  customer.c_nationkey = 3 and customer.c_custkey < 500 order by customer.c_custkey"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=False, precision=0.01, alternateQuery=altQStr)

# comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

comp.report()
comp.logResults(logFile, version, memo)
