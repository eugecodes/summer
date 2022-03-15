
import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet
import datetime
from decimal import Decimal

print "&&&&&&&&&&&&&&&&&&&&    Starting Troubleshooting script &&&&&&&&&&&&&&&&&&&&&&&"



#ph = PostgresHandler("host=169.53.37.156 port=5432 dbname=tpch50mbx2 user=postgres password=terry")
# ph = PostgresHandler("host=169.53.37.156 port=5432 dbname=tpch1gb user=postgres password=terry")
# ph = PostgresHandler("host=169.53.37.156 port=5432 dbname=tpch50mb user=postgres password=terry")
ph = PostgresHandler("host='localhost' dbname='integration_test' user='postgres' password='meloleo'")

# schema="testCompSharedAll2"
# db="tpch50Mb"
schema="6"
db="testing"
# Create Blazing database on local
# schema="8"
# db="regeneron7"
bh = LocalBlazingHandler("52.41.136.244", 8890, schema, db)
# bh = ""


# schema="testCompSharedAll2"
# db="tpch50Mb"
# bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)
comp = PostgresComparisonTestSet(bh, ph)

# ph = PostgresHandler("host=169.53.37.156 port=5432 dbname=tpch10gb user=postgres password=terry")
# schema="integrationTests"
# db="tpch10gb"
# bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)
# comp = PostgresComparisonTestSet(bh, ph)
"""
# Testing Emilse - Trying Easy Queries
# The Script has an error that fails when a query runs ok but it doesn't return results
#  File "../Classes\PostgresComparisonTestSet.py", line 95, in validate
#    print range(parr)
#   TypeError: range() integer end argument expected, got list.
#   TypeError: object of type 'int' has no len()

qStr = "create temp table tabla_temporal as select * from customer"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
qStr = "create table tabla_temporal as select * from customer"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
qStr = "create table negatives_test as select ((a[2]::numeric) * -5) as primer_campo from (select regexp_split_to_array(c_name,'#') from tabla_temporal) as dt(a)"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)


qStr = "select * from negatives_test inner join customer on negatives_test.primer_campo = (customer.c_custkey * -5)"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
qStr = "Select * from tabla_temporal as tt left join customer on customer.c_custkey = tt.c_custkey where tt.c_custkey <= (customer.c_acctbal :: bigint)"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
qStr = "Select * from tabla_temporal as tt left join customer on customer.c_custkey = tt.c_custkey where tt.c_custkey <= customer.c_acctbal"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
qStr = "Select * from tabla_temporal as tt left join customer on customer.c_custkey = tt.c_custkey where tt.c_custkey <= (tt.c_acctbal :: bigint)"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
qStr = "Select from tabla_temporal as tt left join customer on customer.c_custkey = tt.c_custkey where tt.c_custkey <= (customer.c_acctbal*(tt.c_address :: bigint))"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
qStr = "Select from tabla_temporal as tt left join customer on customer.c_custkey = tt.c_custkey"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
qStr = "Select sum(c_name::numeric)::bigint as mynumber from tabla_temporal"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
qStr = "select a[1], a[2], a[3], a[4] from (select regexp_split_to_array('a,b,c,d', ',')) as dt(a)"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
qStr = "select sum(a[2]::numeric)::bigint from (select regexp_split_to_array(c_name,'#') from tabla_temporal) as dt(a)"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
#qStr = "drop temp table tabla_temporal"  GIVES ERROR WHEN RUNNING FROM PYTHON, BUT DOESN'T GIVE ERROR RUNNING IN THE DB
#comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
"""


# this is to test issue with group by using copy instead of swap on double data
qStr = "select avg(o_totalprice) from orders where o_orderstatus = 'O' group by o_orderpriority"
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
qStr = "select sum(o_totalprice) from orders where o_orderdate >= '19980701' and o_orderdate < '19980706' group by o_orderdate"
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)
qStr = "select avg(o_totalprice) from orders group by o_orderstatus"
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select customer.c_acctbal, orders.o_totalprice, orders.o_orderkey,
case when customer.c_acctbal < orders.o_orderkey then customer.c_acctbal else orders.o_totalprice end ,
case when customer.c_acctbal < customer.c_acctbal then customer.c_acctbal else 338.66 end ,
case when orders.o_totalprice < customer.c_acctbal then customer.c_acctbal else customer.c_acctbal/123 end
from customer left outer join orders on customer.c_custkey = orders.o_custkey
 where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100 and orders.o_custkey  < 1000000000"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)


qStr = """select customer.c_name, orders.o_orderkey, case when orders.o_orderkey >= 261338.66 then 5 else orders.o_orderkey end ,
case when customer.c_acctbal > customer.c_acctbal then 5 else 5 end ,
case when orders.o_totalprice > 261338.66 then 5 else nullif(orders.o_orderkey % 8, 3) end
from customer left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100 and orders.o_custkey  < 1000000000."""
"""order by customer.c_name, orders.o_orderkey"""
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)




qStr = """select 100168549 - avg(customer.c_custkey), 56410984/sum(customer.c_acctbal), (123 - 945/max(customer.c_custkey))/avg(81619/orders.o_orderkey) from orders
inner join customer on orders.o_custkey = customer.c_custkey where orders.o_orderkey < 1000 and customer.c_custkey < 1000
"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select avg(customer.c_nationkey) + count(orders.o_orderkey), sum(orders.o_totalprice)/count(customer.c_name), (max(orders.o_orderkey/customer.c_acctbal) - min(orders.o_orderkey/orders.o_totalprice))/avg(orders.o_orderkey/orders.o_totalprice)
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
where  customer.c_nationkey = 3
"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)




qStr = """select region.r_regionkey, sum(region.r_regionkey), count(region.r_regionkey), sum(nation.n_nationkey) from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5 group by region.r_regionkey"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select region.r_regionkey, avg(region.r_regionkey), sum(nation.n_nationkey) from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5 group by region.r_regionkey"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select region.r_regionkey, avg(region.r_regionkey), avg(region.r_regionkey*nation.n_nationkey), sum(region.r_regionkey*nation.n_nationkey) from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5 group by region.r_regionkey"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select region.r_regionkey, sum(region.r_regionkey*nation.n_nationkey)/count(region.r_regionkey*nation.n_nationkey) from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5 group by region.r_regionkey"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select region.r_regionkey, max(nation.n_nationkey), max(region.r_regionkey*nation.n_nationkey) from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5 group by region.r_regionkey"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select region.r_regionkey*region.r_regionkey, region.r_regionkey*avg(region.r_regionkey)-300, region.r_regionkey*avg(region.r_regionkey*nation.n_nationkey)-300, (max(region.r_regionkey*nation.n_nationkey/10) - min(region.r_regionkey*nation.n_nationkey*10))/sum(nation.n_regionkey) from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5 group by region.r_regionkey"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select region.r_regionkey*region.r_regionkey from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5 group by region.r_regionkey"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

# this is crashing cuda
qStr = """select region.r_regionkey*avg(region.r_regionkey)-300 from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5 group by region.r_regionkey"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select region.r_regionkey*avg(region.r_regionkey*nation.n_nationkey)-300 from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5 group by region.r_regionkey"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select (max(region.r_regionkey*nation.n_nationkey/10) - min(region.r_regionkey*nation.n_nationkey*10))/sum(nation.n_regionkey) from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5 group by region.r_regionkey"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select max(region.r_regionkey*nation.n_nationkey/10) from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select (max(region.r_regionkey*nation.n_nationkey/10) -  min(region.r_regionkey*nation.n_nationkey*10))/sum(nation.n_regionkey),  avg(region.r_regionkey)*2, avg(region.r_regionkey*nation.n_nationkey)+5 from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = """select region.r_regionkey*nation.n_nationkey/10,  nation.n_nationkey, region.r_regionkey*nation.n_nationkey*10 + nation.n_regionkey,  region.r_regionkey from region
inner join nation on nation.n_regionkey = region.r_regionkey
where nation.n_nationkey >5"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = "select n_nationkey, n_regionkey from nation where n_nationkey > 5"
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = "select n_nationkey * n_regionkey, n_nationkey/n_regionkey from nation where n_nationkey > 5 and n_regionkey>0"
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = "select max(n_nationkey), max(n_nationkey * n_regionkey), avg( n_nationkey/n_regionkey) from nation where n_nationkey > 5  and n_regionkey>0"
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

qStr = "select max(n_nationkey), max(n_nationkey * n_regionkey), avg( n_nationkey/n_regionkey) from nation where n_nationkey > 5  and n_regionkey>0 group by n_regionkey"
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, precision=0.01)

comp.report()
comp.logResults("log2.txt", "version", "memo")
