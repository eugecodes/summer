import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet

if 'ph' not in locals():
    ph = PostgresHandler("host='localhost' dbname='integration_test' user='postgres' password='meloleo'")
    
if 'bh' not in locals():
    bh = LocalBlazingHandler("52.41.136.244", 8890, "6", "testing")
    
if 'version' not in locals():
    version = 0
    
if 'memo' not in locals():
    memo = ""
    
if 'logFile' not in locals():
    logFile = ""

comp = PostgresComparisonTestSet(bh, ph)


print "**********************************************************************"
print "Starting Order By Tests"
print "**********************************************************************"

qStr = "select max(n_nationkey), n_regionkey, sum(n_nationkey-n_regionkey) as suma, sum(n_nationkey+n_regionkey) from nation where n_nationkey < 30 group by n_regionkey order by 1"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=False, prescision = 0.01)

qStr = "select n_nationkey, n_regionkey, n_nationkey-n_regionkey from nation where n_nationkey < 30 order by 2, n_nationkey + n_regionkey"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=False, prescision = 0.01)

qStr = "select max(n_nationkey), n_regionkey, sum(n_nationkey-n_regionkey) as suma, sum(n_nationkey+n_regionkey) from nation where n_nationkey < 30 group by n_regionkey order by sum(n_nationkey+n_regionkey), sum(n_nationkey+n_regionkey)-n_regionkey"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=False, prescision = 0.01)

qStr = "select max(n_nationkey), n_regionkey, sum(n_nationkey-n_regionkey) as suma, sum(n_nationkey+n_regionkey) from nation where n_nationkey < 30 group by n_regionkey order by sum(n_nationkey+n_regionkey)"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=False, prescision = 0.01)

qStr = "select max(n_nationkey), n_regionkey, sum(n_nationkey-n_regionkey) as suma, sum(n_nationkey+n_regionkey) from nation where n_nationkey < 30 group by n_regionkey order by sum(n_nationkey+n_regionkey + 5)"
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=False, prescision = 0.01)

# order by long asc
qStr = "select * from customer order by c_custkey asc limit 10"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# order by long asc, double desc
qStr = "select * from customer order by c_custkey asc, c_acctbal desc limit 10"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# order by string asc, string desc
qStr = "select * from customer order by c_phone asc, c_name desc limit 10"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# order by date asc, string desc
qStr = "select * from lineitem order by l_receiptdate asc, l_shipinstruct desc limit 10"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# order by date asc, string desc, alias field
qStr = "select (l_quantity / 0.85) as quantity_tax from lineitem order by l_receiptdate asc, l_shipinstruct desc, quantity_tax limit 10"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# order by date asc, string desc, transformation, group by transformation field
qStr = "select * from lineitem group by l_quantity order by l_receiptdate asc, l_shipinstruct desc, (l_quantity*0.25) limit 10"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# order by, group by, where not
qStr = "select o_orderkey, o_orderdate from orders where not(o_orderdate < '19920103' or o_orderdate >= '19980801') group by o_orderkey order by (o_orderkey*0.05), o_orderdate limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# order by with inner join DOES NOT WORK
qStr = "select * from customer inner join orders on customer.c_custkey = orders.o_custkey order by (orders.o_custkey * 50) limit 10"
#comp.runAndValidateQuery(qStr, showVerboseFails=True)
# order by with outer left join DOES NOT WORK
qStr = "select * from customer left outer join orders on customer.c_custkey = orders.o_custkey order by (orders.o_custkey * 50) limit 10"
#comp.runAndValidateQuery(qStr, showVerboseFails=True)
# order by with outer full join DOES NOT WORK
qStr = "select * from customer full outer join orders on customer.c_custkey = orders.o_custkey order by (orders.o_custkey * 50) limit 10"
#comp.runAndValidateQuery(qStr, showVerboseFails=True)

# order by not # Comentario: Necesita el group by si o si en una transformacion en el order by si la misma no necesita agrupacion?
qStr = "select o_orderkey, o_orderstatus from orders where o_custkey < 10 or not(o_orderstatus = 'O') group by o_orderkey order by (o_orderkey*85), (o_orderstatus-52) limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# order by transform, select transform
qStr = "select c_custkey * 255 as resultado from customer order by c_custkey * 255"
comp.runAndValidateQuery(qStr, showVerboseFails=True)


# order by datediff
qStr = "select o_orderkey, o_orderstatus from orders where o_custkey < 10 or not(o_orderstatus != 'O') group by o_orderdate order by datediff(o_orderdate, o_orderdate+5), o_orderstatus limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# order by transformation
qStr = "select (o_orderkey*o_custkey) as primero, o_orderstatus from orders where o_custkey < 10 and not(o_orderstatus <> 'O') order by (o_orderkey*o_custkey), o_orderstatus limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)


# order by date with transformation
qStr = "select o_orderkey, o_orderstatus from orders where not(o_custkey >= 100) and not(o_orderdate = '19920103') group by o_orderdate order by not(o_orderdate = '19920103') asc"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

# order by avg
qStr = "select avg(o_orderkey+o_custkey) as second from orders where not(o_custkey < 10 or o_orderstatus = 'O') or o_orderstatus = 'F' order by o_orderstatus = 'F', o_orderstatus order by avg(o_orderkey+o_custkey) limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# order by count
qStr = "select count(o_orderkey)*8 as id, o_orderstatus from orders where o_totalprice < 50000 and not(o_orderdate < '19980303' and o_orderdate > '19920103') order by id, o_orderkey, o_orderstatus limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

# order by with multiple combinations
qStr = "select o_orderkey, o_orderstatus from orders where not(o_custkey > 50 or (o_orderdate = '19920103' or o_orderdate = '19920105')) group by o_orderdate order by datediff(o_orderdate,'19920105')"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

qStr = "select o_orderkey, o_orderstatus from orders group by o_custkey, o_orderdate order by not((o_custkey <= 500 and o_orderdate = '19920103') or o_orderdate <> '19920105')"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
    
qStr = "select o_orderkey, o_orderstatus from orders group by o_custkey, o_orderstatus, o_orderdate order by not(o_custkey >= 100 and (o_orderstatus = 'O'  or (o_orderstatus = 'F' and o_custkey > 100)) and o_orderdate >= '19920105') limit 50"
comp.runAndValidateQuery(qStr, showVerboseFails=True)


comp.report()
comp.logResults(logFile, version,memo)
