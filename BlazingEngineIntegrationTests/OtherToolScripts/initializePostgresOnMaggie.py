# coding=utf-8
import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler


path = "../DataSets/TPCH1Gb/"
tableFileList = ["customer.tbl", "lineitem.tbl", "nation.tbl", "orders.tbl", "part.tbl", "partsupp.tbl", "region.tbl", "supplier.tbl"]
tableNameList = ["customer", "lineitem", "nation", "orders", "part", "partsupp", "region", "supplier"]


# Create database on Postgres on maggie
# ph = PostgresHandler("host=127.0.0.1 port=5432 dbname=tpch1gb user=postgres password=terry")
# ph.createDatabase("host=127.0.0.1 port=5432 user=postgres password=terry", "tpch1gb")

ph = PostgresHandler("host=127.0.0.1 port=5432 dbname=tpch1gb user=wmalpica password=blazingIsBetter")
ph.createDatabase("host=127.0.0.1 port=5432 user=wmalpica password=blazingIsBetter", "tpch1gb")

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
print "Done Importing"
ph.describeDatabaseVerbose()
