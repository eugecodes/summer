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
print "Starting Aggregations Without Group By With Transformations tests"
print "**********************************************************************"

# agg op agg
qStr = "select avg(o_orderkey) + count(o_orderkey), sum(o_totalprice)/count(o_orderstatus), (max(o_orderkey/o_totalprice) - min(o_orderkey/o_totalprice))/avg(o_orderkey/o_totalprice) from orders"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = "select max(o_orderkey + o_totalprice*o_custkey) - min(o_orderkey - o_custkey)/avg(o_custkey/o_totalprice) from orders"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# agg op literal and viceversa
qStr = "select avg(o_orderkey) - 100168549, sum(o_totalprice)/56410984, (max(o_orderkey/945) - 123)/avg(o_orderkey/81619) from orders"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = "select 100168549 - avg(o_orderkey), 56410984/sum(o_totalprice), (123 - 945/max(o_orderkey))/avg(81619/o_orderkey) from orders"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = "select avg(o_orderkey) - 100168549.346, sum(o_totalprice)/56410984.6496, (max(o_orderkey/945.1) - 123.0)/avg(o_orderkey/81619.9844) from orders"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = "select 100168549.321 - avg(o_orderkey), 56410984.0000001/sum(o_totalprice), (123.965 - 945.11111/max(o_orderkey))/avg(81619.88/o_orderkey) from orders"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)


# same as above with where clause
# agg op agg
qStr = "select avg(o_orderkey) + count(o_orderkey), sum(o_totalprice)/count(o_orderstatus), (max(o_orderkey/o_totalprice) - min(o_orderkey/o_totalprice))/avg(o_orderkey/o_totalprice) from orders where o_custkey < 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = "select max(o_orderkey + o_totalprice*o_custkey) - min(o_orderkey - o_custkey)/avg(o_custkey/o_totalprice) from orders where o_orderkey < 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# agg op literal and viceversa
qStr = "select avg(o_orderkey) - 100168549, sum(o_totalprice)/56410984, (max(o_orderkey/945) - 123)/avg(o_orderkey/81619) from orders where o_custkey < 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = "select 100168549 - avg(o_orderkey), 56410984/sum(o_totalprice), (123 - 945/max(o_orderkey))/avg(81619/o_orderkey) from orders where o_orderkey < 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = "select avg(o_orderkey) - 100168549.346, sum(o_totalprice)/56410984.6496, (max(o_orderkey/945.1) - 123.0)/avg(o_orderkey/81619.9844) from orders where o_custkey < 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = "select 100168549.321 - avg(o_orderkey), 56410984.0000001/sum(o_totalprice), (123.965 - 945.11111/max(o_orderkey))/avg(81619.88/o_orderkey) from orders where o_orderkey < 100"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)


# same as above with joins
# agg op agg
qStr = """select avg(customer.c_nationkey) + count(orders.o_orderkey), sum(orders.o_totalprice)/count(customer.c_name), (max(orders.o_orderkey/customer.c_acctbal) - min(orders.o_orderkey/orders.o_totalprice))/avg(orders.o_orderkey/orders.o_totalprice) from orders
inner join customer on customer.c_custkey = orders.o_custkey where orders.o_orderkey < 100"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select max(customer.c_nationkey + orders.o_totalprice*orders.o_custkey) - min(customer.c_acctbal - orders.o_custkey)/avg(orders.o_custkey/customer.c_acctbal) from customer
inner join orders on customer.c_custkey = orders.o_custkey"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# agg op literal and viceversa
qStr = """select avg(customer.c_custkey) - 100168549, sum(customer.c_acctbal)/56410984, (max(customer.c_custkey/945) - 123)/avg(orders.o_orderkey/81619) from customer
inner join orders on customer.c_custkey = orders.o_custkey where customer.c_custkey < 100"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select 100168549 - avg(customer.c_custkey), 56410984/sum(customer.c_acctbal), (123 - 945/max(customer.c_custkey))/avg(81619/orders.o_orderkey) from orders
inner join customer on orders.o_custkey = customer.c_custkey where orders.o_orderkey < 100 and customer.c_custkey < 100"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select avg(customer.c_custkey) - 100168549.346, sum(customer.c_acctbal)/56410984.6496, (max(customer.c_custkey/945.1) - 123.0)/avg(orders.o_orderkey/81619.9844) from orders
inner join customer on customer.c_custkey = orders.o_custkey where orders.o_orderkey < 100 or customer.c_custkey < 100"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select 100168549.321 - avg(customer.c_custkey), 56410984.0000001/sum(customer.c_acctbal), (123.965 - 945.11111/max(customer.c_custkey))/avg(81619.88/orders.o_orderkey) from orders
inner join customer on orders.o_custkey = customer.c_custkey"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)





# same as above with outer joins so that there are nulls
# agg op agg
qStr = """select avg(customer.c_nationkey) + count(orders.o_orderkey), sum(orders.o_totalprice)/count(customer.c_name), (max(orders.o_orderkey/customer.c_acctbal) - min(orders.o_orderkey/orders.o_totalprice))/avg(orders.o_orderkey/orders.o_totalprice)
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_nationkey = 3"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select max(customer.c_nationkey + orders.o_totalprice*orders.o_custkey) - min(customer.c_acctbal - orders.o_custkey)/avg(orders.o_custkey/customer.c_acctbal)
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_nationkey = 3"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

# agg op literal and viceversa
qStr = """select avg(customer.c_custkey) - 100168549, sum(customer.c_acctbal)/56410984, (max(customer.c_custkey/945) - 123)/avg(orders.o_orderkey/81619)
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_nationkey = 3"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select 100168549 - avg(customer.c_custkey), 56410984/sum(customer.c_acctbal), (123 - 945/max(customer.c_custkey))/avg(81619/orders.o_orderkey)
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_nationkey = 3"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select avg(customer.c_custkey) - 100168549.346, sum(customer.c_acctbal)/56410984.6496, (max(customer.c_custkey/945.1) - 123.0)/avg(orders.o_orderkey/81619.9844)
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_nationkey = 3"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select 100168549.321 - avg(customer.c_custkey), 56410984.0000001/sum(customer.c_acctbal), (123.965 - 945.11111/max(customer.c_custkey))/avg(81619.88/orders.o_orderkey)
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_nationkey = 3"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)


# lets make sure that all aggs have correct output when all agged values are null
qStr = "select count(o_custkey), count(nullif(o_custkey, 5)), min(nullif(o_custkey, 5)), max(nullif(o_custkey, 5)), sum(nullif(o_custkey, 5)), avg(nullif(o_custkey, 5)) from orders where o_custkey = 5"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select count(customer.c_nationkey), count(nullif(customer.c_nationkey, 3)), min(nullif(customer.c_nationkey, 3)), max(nullif(customer.c_nationkey, 3)), sum(nullif(customer.c_nationkey, 3)), avg(nullif(customer.c_nationkey, 3))
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
 where  customer.c_nationkey = 3"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

comp.report()
comp.logResults(logFile, version, memo)
