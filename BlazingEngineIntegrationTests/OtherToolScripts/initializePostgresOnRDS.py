import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler


#path = "../DataSets/TPCH50Mb/"
path = "/disk1/tpchData/"
tableFileList = ["new_customer.tbl", "new_lineitem.tbl", "new_nation.tbl", "new_orders.tbl", "new_part.tbl", "new_partsupp.tbl", "new_region.tbl", "new_supplier.tbl"]
tableNameList = ["customer", "lineitem", "nation", "orders", "part", "partsupp", "region", "supplier"]



# Create database on Postgres on maggie
#ph = PostgresHandler("host=169.53.37.156 port=5432 dbname=tpch50mb user=postgres password=terry")

#ph.createDatabase("host=169.53.37.156 port=5432 user=postgres password=terry", "tpch50Mb")

ph = PostgresHandler("host=tpch-100gb.cdmjeav81oyg.us-west-2.rds.amazonaws.com port=5432 dbname=tpch100gb user=postgres password=terry671")

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



ph.dropTables(tableNameList)
ph.importDatabaseTables(tableNameList, path, tableFileList, tableDescriptionList)
print "Done Importing"
ph.describeDatabaseVerbose()
