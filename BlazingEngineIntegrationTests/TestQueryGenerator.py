# coding=utf-8
import sys
sys.path.append('Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet
from QGCC import RandomQueryGenerator

ph = PostgresHandler("host='localhost' dbname='integration_test' user='postgres' password='meloleo'")
bh = LocalBlazingHandler("52.32.212.172", 8890, "6", "testing")
comp = PostgresComparisonTestSet(bh, ph)

tableFileList = ["customer.tbl", "lineitem.tbl", "nation.tbl", "orders.tbl", "part.tbl", "partsupp.tbl", "region.tbl", "supplier.tbl"]
tableNameList = ["customer", "lineitem", "nation", "orders", "part", "partsupp", "region", "supplier"]

columns_customer = ['c_custkey', 'c_name', 'c_address', 'c_nationkey', 'c_phone', 'c_acctbal', 'c_mktsegment', 'c_comment']
type_data_customer = ['long', 'string', 'string', 'long', 'string', 'double', 'string', 'string']

columns_lineitem = ['l_orderkey', 'l_partkey', 'l_suppkey', 'l_linenumber', 'l_quantity', 'l_extendedprice', 'l_discount', 'l_tax', 'l_returnflag', 'l_linestatus', 'l_shipdate', 'l_commitdate', 'l_receiptdate', 'l_shipinstruct', 'l_shipmode', 'l_comment']
type_data_lineitem = ['long', 'long', 'long', 'long', 'double', 'double', 'double', 'double', 'string', 'string', 'date', 'date', 'date', 'string', 'string', 'string']

columns_nation = ['n_nationkey', 'n_name', 'n_regionkey', 'n_comment']
type_data_nation = ['long', 'string', 'long', 'string']

columns_orders = ['o_orderkey', 'o_custkey', 'o_orderstatus', 'o_totalprice', 'o_orderdate', 'o_orderpriority', 'o_clerk', 'o_shippriority', 'o_comment']
type_data_orders = ['long', 'long', 'string', 'double', 'date', 'string', 'string', 'long', 'string']

columns_part = ['p_partkey', 'p_name', 'p_mfgr', 'p_brand', 'p_type', 'p_size', 'p_container', 'p_retailprice', 'p_comment']
type_data_part = ['long', 'string', 'string', 'string', 'string', 'long', 'string', 'double', 'string']

columns_partsupp = ['ps_partkey', 'ps_suppkey', 'ps_availqty', 'ps_supplycost', 'ps_comment']
type_data_partsupp = ['long', 'long', 'long', 'double', 'string']

columns_region = ['r_regionkey', 'r_name', 'r_comment']
type_data_region = ['long', 'string', 'string']

columns_supplier = ['s_suppkey', 's_name', 's_address', 's_nationkey', 's_phone', 's_acctbal', 's_comment']
type_data_supplier = ['long', 'string', 'string', 'long', 'string', 'double', 'string']

tableDescriptionList = [columns_customer, columns_lineitem, columns_nation, columns_orders, columns_part, columns_partsupp, columns_region, columns_supplier]
tableDataTypeList = [type_data_customer, type_data_lineitem, type_data_nation, type_data_orders, type_data_part, type_data_partsupp, type_data_region, type_data_supplier]
limits = [8, 16, 4, 9, 9, 5, 3, 7]
cant_tables = 8

query_generator = RandomQueryGenerator(comp, tableDescriptionList, tableDataTypeList, limits, cant_tables, tableNameList)
query_generator.generateRandom(to_file=True, file="nuevo_log_queries.txt", to_json=False, comparison_test=False, comparison_test_log_file="nuevo_log.txt", debug=True)
