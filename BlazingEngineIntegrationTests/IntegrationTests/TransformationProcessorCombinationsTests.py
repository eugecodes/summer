import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet

if 'ph' not in locals():
    ph = PostgresHandler("host=127.0.0.1 port=5432 dbname=tpch1gb user=wmalpica password=blazingIsBetter")
    
if 'bh' not in locals():
    schema="testCompSharedAll"
    db="tpch1Gb"
    bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)

if 'version' not in locals():
    version = 0

if 'memo' not in locals():
    memo = ""
    
if 'logFile' not in locals():
    logFile = ""
    
comp = PostgresComparisonTestSet(bh, ph)

print "**********************************************************************"
print "Starting transformationProcessor combinations tests"
print "**********************************************************************"


# test all transformationProcessor combinations
qStr = """select nation.n_nationkey + nation.n_nationkey from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select nation.n_nationkey + 5 from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select nation.n_nationkey + customer.c_acctbal from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select nation.n_nationkey + 5.5 from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select nation.n_nationkey + (nation.n_nationkey * 2) from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select nation.n_nationkey + (customer.c_acctbal * 2) from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)

qStr = """select 5 + nation.n_nationkey from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select 5 + 5 from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
# cant do this
# comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select 5 + customer.c_acctbal from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select 5 + 5.5 from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
# cant do this
# comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select 5 + (nation.n_nationkey * 2) from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select 5 + (customer.c_acctbal * 2) from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)

qStr = """select customer.c_acctbal + nation.n_nationkey from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select customer.c_acctbal + 5 from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select customer.c_acctbal + customer.c_acctbal from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select customer.c_acctbal + 5.5 from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select customer.c_acctbal + (nation.n_nationkey * 2) from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select customer.c_acctbal + (customer.c_acctbal * 2) from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)

qStr = """select 5.5 + nation.n_nationkey from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select 5.5 + 5 from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
# cant do this
# comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select 5.5 + customer.c_acctbal from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select 5.5 + 5.5 from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
# cant do this
# comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select 5.5 + (nation.n_nationkey * 2) from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select 5.5 + (customer.c_acctbal * 2) from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)

qStr = """select (nation.n_nationkey * 2) + nation.n_nationkey from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select (nation.n_nationkey * 2) + 5 from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select (nation.n_nationkey * 2) + customer.c_acctbal from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select (nation.n_nationkey * 2) + 5.5 from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select (nation.n_nationkey * 2) + (nation.n_nationkey * 2) from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select (nation.n_nationkey * 2) + (customer.c_acctbal * 2) from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)

qStr = """select (customer.c_acctbal * 2) + nation.n_nationkey from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select (customer.c_acctbal * 2) + 5 from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select (customer.c_acctbal * 2) + customer.c_acctbal from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select (customer.c_acctbal * 2) + 5.5 from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select (customer.c_acctbal * 2) + (nation.n_nationkey * 2) from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
qStr = """select (customer.c_acctbal * 2) + (customer.c_acctbal * 2) from nation
 inner join customer on nation.n_nationkey = customer.c_nationkey where customer.c_custkey < 10
 group by nation.n_nationkey, customer.c_acctbal"""
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)


# combinations with nulls
qStr = """select customer.c_custkey, orders.o_orderkey, orders.o_orderkey % 6, orders.o_orderkey + 6, orders.o_orderkey - 6, orders.o_orderkey * 6, orders.o_orderkey / 6,
orders.o_totalprice, orders.o_totalprice % 6.6, orders.o_totalprice + 6.6, orders.o_totalprice - 6.6, orders.o_totalprice * 6.6, orders.o_totalprice / 6.6
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
 where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100"""
 
options = ["customer.c_custkey", "customer.c_acctbal", "orders.o_orderkey", "orders.o_totalprice", "5", "6.7"]
operators = [" + ", " - ", " * ", " / "]
for i in range(0,len(options)):
    for j in range(0,len(options)):
        for o in range(0, len(operators)):
            qStr = "select " + options[i] + operators[o] + options[j] + " from customer left outer join orders on customer.c_custkey = orders.o_custkey where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100"
            comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)

options = ["customer.c_custkey", "orders.o_orderkey", "5"]
for i in range(0,len(options)):
    for j in range(0,len(options)):
        qStr = "select " + options[i] + " % " + options[j] + " from customer left outer join orders on customer.c_custkey = orders.o_custkey where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100"
        comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)


comp.report()
comp.logResults(logFile, version, memo)
