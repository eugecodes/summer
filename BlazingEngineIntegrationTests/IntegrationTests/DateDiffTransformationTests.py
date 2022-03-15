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
print "Starting DATEDIFF Transformations tests"
print "**********************************************************************"


#
# # datediff combinations
# # test all transformationProcessor combinations
# dateDiffOptions = ["datediff(day, orders.o_orderdate, lineitem.l_receiptdate)",
# "datediff(month, orders.o_orderdate, lineitem.l_receiptdate)",
# "datediff(year, orders.o_orderdate, lineitem.l_receiptdate)",
# "datediff(day, 19850101, lineitem.l_receiptdate)", "datediff(day, orders.o_orderdate, 20161010)",
# "datediff(month, 19850101, lineitem.l_receiptdate)", "datediff(month, orders.o_orderdate, 20161010)",
# "datediff(year, 19850101, lineitem.l_receiptdate)", "datediff(year, orders.o_orderdate, 20161010)",
# "(datediff(month, orders.o_orderdate, lineitem.l_receiptdate) * datediff(day, orders.o_orderdate, lineitem.l_receiptdate)",
# "(datediff(month, orders.o_orderdate, lineitem.l_receiptdate) * orders.o_custkey)",
# "(datediff(month, orders.o_orderdate, lineitem.l_receiptdate) * lineitem.l_quantity)"]
#
# postgresDateDiffOptions = ["DATE_PART('day', lineitem.l_receiptdate::timestamp - orders.o_orderdate::timestamp)",
# "DATE_PART('month', lineitem.l_receiptdate::timestamp - orders.o_orderdate::timestamp)",
# "DATE_PART('year', lineitem.l_receiptdate::timestamp - orders.o_orderdate::timestamp)",
# "DATE_PART('day', lineitem.l_receiptdate::timestamp - '1985-01-01'::timestamp)",
# "DATE_PART('day', '2016-10-10'::timestamp - orders.o_orderdate::timestamp)",
# "DATE_PART('month', lineitem.l_receiptdate::timestamp - '1985-01-01'::timestamp)",
# "DATE_PART('month', '2016-10-10'::timestamp - orders.o_orderdate::timestamp)",
# "DATE_PART('year', lineitem.l_receiptdate::timestamp - '1985-01-01'::timestamp)",
# "DATE_PART('year', '2016-10-10'::timestamp - orders.o_orderdate::timestamp)",
# "(DATE_PART('month', lineitem.l_receiptdate::timestamp - orders.o_orderdate::timestamp) * DATE_PART('day', lineitem.l_receiptdate::timestamp - orders.o_orderdate::timestamp))",
# "(DATE_PART('month', lineitem.l_receiptdate::timestamp - orders.o_orderdate::timestamp) * orders.o_custkey)",
# "(DATE_PART('month', lineitem.l_receiptdate::timestamp - orders.o_orderdate::timestamp) * lineitem.l_quantity)"]
#
# otherOptions = ["orders.o_custkey", "lineitem.l_quantity", "5", "5.5"]
#
# for o1 in range(0,len(dateDiffOptions)):
#     qStr = "select " + dateDiffOptions[o1]  + " from orders inner join lineitem on lineitem.l_orderkey = orders.o_orderkey where orders.o_orderkey < 30 and lineitem.l_orderkey < 20 group by lineitem.l_quantity, orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate order by orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate"
#     postgresQStr = "select " + postgresDateDiffOptions[o1] + " from orders inner join lineitem on lineitem.l_orderkey = orders.o_orderkey where orders.o_orderkey < 30 and lineitem.l_orderkey < 20 group by lineitem.l_quantity, orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate order by orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate"
#     comp.runAndValidateQuery(postgresQStr, showVerboseQuery=True, orderless=False, alternateQuery=qStr)
#
# for o1 in range(0,len(dateDiffOptions)):
#     for o2 in range(0, len(dateDiffOptions)):
#         qStr = "select " + dateDiffOptions[o1] + " + " + dateDiffOptions[o2] + " from orders inner join lineitem on lineitem.l_orderkey = orders.o_orderkey where orders.o_orderkey < 30 and lineitem.l_orderkey < 20 group by lineitem.l_quantity, orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate order by orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate"
#         postgresQStr = "select " + postgresDateDiffOptions[o1] + " + " + postgresDateDiffOptions[o2] + " from orders inner join lineitem on lineitem.l_orderkey = orders.o_orderkey where orders.o_orderkey < 30 and lineitem.l_orderkey < 20 group by lineitem.l_quantity, orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate order by orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate"
#         comp.runAndValidateQuery(postgresQStr, showVerboseQuery=True, orderless=False, alternateQuery=qStr)
#
# for o1 in range(0,len(dateDiffOptions)):
#     for o2 in range(0, len(otherOptions)):
#         qStr = "select " + dateDiffOptions[o1] + " + " + otherOptions[o2] + " from orders inner join lineitem on lineitem.l_orderkey = orders.o_orderkey where orders.o_orderkey < 30 and lineitem.l_orderkey < 20 group by lineitem.l_quantity, orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate order by orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate"
#         postgresQStr = "select " + postgresDateDiffOptions[o1] + " + " + otherOptions[o2] + " from orders inner join lineitem on lineitem.l_orderkey = orders.o_orderkey where orders.o_orderkey < 30 and lineitem.l_orderkey < 20 group by lineitem.l_quantity, orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate order by orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate"
#         comp.runAndValidateQuery(postgresQStr, showVerboseQuery=True, orderless=False, alternateQuery=qStr)
#
# for o1 in range(0,len(otherOptions)):
#     for o2 in range(0, len(dateDiffOptions)):
#         qStr = "select " + otherOptions[o1] + " + " + dateDiffOptions[o2] + " from orders inner join lineitem on lineitem.l_orderkey = orders.o_orderkey where orders.o_orderkey < 30 and lineitem.l_orderkey < 20 group by lineitem.l_quantity, orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate order by orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate"
#         postgresQStr = "select " + otherOptions[o1] + " + " + postgresDateDiffOptions[o2] + " from orders inner join lineitem on lineitem.l_orderkey = orders.o_orderkey where orders.o_orderkey < 30 and lineitem.l_orderkey < 20 group by lineitem.l_quantity, orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate order by orders.o_custkey, orders.o_orderdate, lineitem.l_receiptdate"
#         comp.runAndValidateQuery(postgresQStr, showVerboseQuery=True, orderless=False, alternateQuery=qStr)
