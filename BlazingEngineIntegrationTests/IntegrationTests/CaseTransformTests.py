import sys
import random
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
print "Starting CASE Transformations tests"
print "**********************************************************************"

qStr = """select case when o_custkey > 20 then o_orderkey else o_custkey - 20 end from orders where o_orderkey <= 50"""
# comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)

qStr = """select case when o_custkey > 20 then o_orderkey when o_custkey > 10 then o_custkey - 20 else o_custkey - 10 end from orders where o_orderkey <= 50"""
# comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision=0.01)


qStr = """select customer.c_custkey, customer.c_acctbal, orders.o_orderkey, orders.o_totalprice
from customer
left outer join orders on customer.c_custkey = orders.o_custkey
 where  customer.c_nationkey = 3 and customer.c_custkey < 100 order by customer.c_custkey"""
# comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=False, precision=0.01)

# different comparison options
comparisonOptions = ["customer.c_custkey", "customer.c_acctbal", "orders.o_orderkey", "orders.o_totalprice", "9154", "261338.66"]
boolOperatorOptions = [">=", ">", "<=", "<", "=", "<>", "!="]

boolOptions = []
for i in range(0,len(comparisonOptions)-1):
    for j in range(1,len(comparisonOptions)):
        for op in range (0, len(boolOperatorOptions)):
            boolOptions.append(comparisonOptions[i] + " " + boolOperatorOptions[op] + " " + comparisonOptions[j])
            
boolOptions.append("true")
boolOptions.append("false")

boolInd = 0
while (boolInd < len(boolOptions)):
    selInd = 0
    selCols = ""
    while (selInd < 10 and boolInd < len(boolOptions)):
        if selInd > 0:
            selCols = selCols + ", " + "case when " + boolOptions[boolInd] + " then orders.o_orderkey else 5 end "
        else:
            selCols = selCols + "case when " + boolOptions[boolInd] + " then orders.o_orderkey else 5 end "
        boolInd = boolInd + 1
        selInd = selInd + 1
    qStr = "select " + selCols + " from customer left outer join orders on customer.c_custkey = orders.o_custkey where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100"
    qStr = "select " + selCols + " from customer left outer join orders on customer.c_custkey = orders.o_custkey where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100 and orders.o_custkey < 1000000000"
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
    

longOptions = ["customer.c_custkey", "orders.o_orderkey", "5", "nullif(orders.o_orderkey % 8, 3)"]
doubleOptions = ["customer.c_acctbal", "orders.o_totalprice", "338.66", "customer.c_acctbal/123"]
stringOptions = ["customer.c_name", "orders.o_comment", "orders.o_orderstatus", "' literal con punto y coma , . esta aqui'", "'corto'"]


for i in range(0, len(longOptions)-1):
    selCols = ""
    for j in range(1, len(longOptions)):
        boolInd = random.randint(0, len(boolOptions) - 1)
        if j > 1:
            selCols = selCols + ", " + "case when " + boolOptions[boolInd] + " then " + longOptions[i] + " else " + longOptions[j] + " end "
        else:
            selCols = selCols + "case when " + boolOptions[boolInd] + " then " + longOptions[i] + " else " + longOptions[j] + " end "
    
    qStr = "select " + selCols + " from customer left outer join orders on customer.c_custkey = orders.o_custkey where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100"
    qStr = "select " + selCols + " from customer left outer join orders on customer.c_custkey = orders.o_custkey where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100 and orders.o_custkey  < 1000000000"
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)

for i in range(0, len(doubleOptions)-1):
    selCols = ""
    for j in range(1, len(doubleOptions)):
        boolInd = random.randint(0, len(boolOptions) - 1)
        if j > 1:
            selCols = selCols + ", " + "case when " + boolOptions[boolInd] + " then " + doubleOptions[i] + " else " + doubleOptions[j] + " end "
        else:
            selCols = selCols + "case when " + boolOptions[boolInd] + " then " + doubleOptions[i] + " else " + doubleOptions[j] + " end "
    
    qStr = "select " + selCols + " from customer left outer join orders on customer.c_custkey = orders.o_custkey where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100"
    qStr = "select " + selCols + " from customer left outer join orders on customer.c_custkey = orders.o_custkey where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100 and orders.o_custkey  < 1000000000"
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)
    
for i in range(0, len(stringOptions)-1):
    selCols = ""
    for j in range(1, len(stringOptions)):
        boolInd = random.randint(0, len(boolOptions) - 1)
        if j > 1:
            selCols = selCols + ", " + "case when " + boolOptions[boolInd] + " then " + stringOptions[i] + " else " + stringOptions[j] + " end "
        else:
            selCols = selCols + "case when " + boolOptions[boolInd] + " then " + stringOptions[i] + " else " + stringOptions[j] + " end "
    
    qStr = "select " + selCols + " from customer left outer join orders on customer.c_custkey = orders.o_custkey where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100"
    qStr = "select " + selCols + " from customer left outer join orders on customer.c_custkey = orders.o_custkey where  customer.c_nationkey = 3 and customer.c_custkey between 20 and 100 and orders.o_custkey  < 1000000000"
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True, precision = 0.01)



comp.report()
comp.logResults(logFile, version, memo)
