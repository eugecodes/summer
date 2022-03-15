# coding=utf-8
import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler


path = "../DataSets/TPCH50Mb/"
# path = "../DataSets/TPCH50Mb/"
#path = "http://s3.data-set-builder/"
tableFileList = ["customer.tbl", "lineitem.tbl", "nation.tbl", "orders.tbl", "part.tbl", "partsupp.tbl", "region.tbl", "supplier.tbl"]
tableNameList = ["customer", "lineitem", "nation", "orders", "part", "partsupp", "region", "supplier"]




# Create database on Postgres on maggie
ph = PostgresHandler("host=localhost port=5432 dbname=test user=postgres password=postgres")

#ph.createDatabase("host=localhost port=5432 user=postgres password=postgres", "testing")


#ph = PostgresHandler("host=tpch-100gb.cdmjeav81oyg.us-west-2.rds.amazonaws.com port=5432 dbname=tpch100gb3 user=postgres password=terry671")

#ph.createDatabase("host=tpch-100gb.cdmjeav81oyg.us-west-2.rds.amazonaws.com port=5432 user=postgres password=terry671", "tpch100gb3")


customerDesc = "c_custkey INT, c_name VARCHAR(32), c_address VARCHAR(128), c_nationkey INT, c_phone VARCHAR(16), c_acctbal FLOAT, c_mktsegment VARCHAR(16), c_comment VARCHAR(120)"
lineItemDesc = "l_orderkey INT, l_partkey INT, l_suppkey INT, l_linenumber INT, l_quantity FLOAT, l_extendedprice FLOAT, l_discount FLOAT, l_tax FLOAT, l_returnflag VARCHAR(8), l_linestatus VARCHAR(8), l_shipdate DATE, l_commitdate  DATE, l_receiptdate  DATE, l_shipinstruct VARCHAR(32), l_shipmode VARCHAR(16), l_comment VARCHAR(48)"
nationDesc = "n_nationkey INT, n_name VARCHAR(32), n_regionkey INT, n_comment VARCHAR(152)"
ordersDesc = "o_orderkey INT, o_custkey INT, o_orderstatus VARCHAR(8), o_totalprice FLOAT, o_orderdate DATE, o_orderpriority VARCHAR(16), o_clerk VARCHAR(16), o_shippriority INT, o_comment VARCHAR(80)"
partDesc = "p_partkey INT, p_name VARCHAR(56), p_mfgr VARCHAR(32), p_brand VARCHAR(16), p_type VARCHAR(32), p_size INT, p_container VARCHAR(16), p_retailprice FLOAT, p_comment VARCHAR(24)"
partsuppDesc = "ps_partkey INT, ps_suppkey INT, ps_availqty INT, ps_supplycost FLOAT, ps_comment VARCHAR(200)"
regionDesc = "r_regionkey INT, r_name VARCHAR(32), r_comment VARCHAR(152)"
supplierDesc = "s_suppkey INT, s_name VARCHAR(32), s_address VARCHAR(40), s_nationkey INT, s_phone VARCHAR(16), s_acctbal FLOAT, s_comment VARCHAR(104)"
tableDescriptionList = [customerDesc, lineItemDesc, nationDesc, ordersDesc, partDesc, partsuppDesc, regionDesc, supplierDesc]

#ph.dropTables(tableNameList)
ph.importDatabaseTables(tableNameList, path, tableFileList, tableDescriptionList)
ph.importDatabaseTables(tableNameList, path, tableFileList, tableDescriptionList)
print "Done Importing"
ph.describeDatabaseVerbose()



# Create Blazing database on local
# schema="testCompSharedAll2"
# db="tpch1Gb"
# # db="tpch50Mb"
# schema="testCompNothingMasterAll34"
schema="2"
db="tpch170"

#bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)


#bh.dropDatabase()
"""
customerDesc = "c_custkey long, c_name string(32), c_address string(128), c_nationkey long, c_phone string(16), c_acctbal double, c_mktsegment string(16), c_comment string(120)"
lineItemDesc = "l_orderkey long, l_partkey long, l_suppkey long, l_linenumber long, l_quantity double, l_extendedprice double, l_discount double, l_tax double, l_returnflag string(8), l_linestatus string(8), l_shipdate date, l_commitdate  date, l_receiptdate  date, l_shipinstruct string(32), l_shipmode string(16), l_comment string(48)"
nationDesc = "n_nationkey long, n_name string(32), n_regionkey long, n_comment string(152)"
ordersDesc = "o_orderkey long, o_custkey long, o_orderstatus string(8), o_totalprice double, o_orderdate date, o_orderpriority string(16), o_clerk string(16), o_shippriority long, o_comment string(80)"
partDesc = "p_partkey long, p_name string(56), p_mfgr string(32), p_brand string(16), p_type string(32), p_size long, p_container string(16), p_retailprice double, p_comment string(24)"
partsuppDesc = "ps_partkey long, ps_suppkey long, ps_availqty long, ps_supplycost double, ps_comment string(200)"
regionDesc = "r_regionkey long, r_name string(32), r_comment string(152)"
supplierDesc = "s_suppkey long, s_name string(32), s_address string(40), s_nationkey long, s_phone string(16), s_acctbal double, s_comment string(104)"
tableDescriptionList = [customerDesc, lineItemDesc, nationDesc, ordersDesc, partDesc, partsuppDesc, regionDesc, supplierDesc]

try:
    bh.initializeDatabase(tableNameList, path, tableFileList, tableDescriptionList, compressed=False, createSchema=False, createDatabase=False, copyUploadFiles=True)
    bh.runQuery("list tables",verbose=True)
except RuntimeError as detail:
    print "Error: ",  detail
    #bh.dropDatabase()
"""

# this is for loading the table data again
"""
for t in range(0,len(tableFileList)):
    bh.loadDataInfile(tableFileList[t], tableNameList[t])

for t in range(0,len(tableFileList)):
    bh.loadDataInfile(tableFileList[t], tableNameList[t])

print "reloaded the data"
"""
