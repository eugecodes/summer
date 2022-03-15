# coding=utf-8
import csv
import string
import dateutil.parser
from random import randint
import random
import radar

import sys
sys.path.append('Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet

""" Configuration Parameters """

ph = PostgresHandler("host='localhost' dbname='integration_test' user='postgres' password='meloleo'")
bh = LocalBlazingHandler("52.41.136.244", 8890, "6", "testing")
comp = PostgresComparisonTestSet(bh, ph)


#output_file = open('queries.txt', 'a')

tableFileList = ["customer.tbl", "lineitem.tbl", "nation.tbl", "orders.tbl", "part.tbl", "partsupp.tbl", "region.tbl", "supplier.tbl"]
tableNameList = ["customer", "lineitem", "nation", "orders", "part", "partsupp", "region", "supplier"]

columns_customer = ['c_custkey', 'c_name', 'c_address', 'c_nationkey', 'c_phone', 'c_acctbal', 'c_mktsegment', 'c_comment']
type_data_customer = ['long', 'string', 'string', 'long', 'string', 'double', 'string', 'string']

columns_lineitem = ['l_orderkey', 'l_partkey', 'l_suppkey', 'l_linenumber', 'l_quantity', 'l_extendedprice', 'l_discount', 'l_tax', 'l_returnflag', 'l_linestatus', 'l_shipdate', 'l_commitdate', 'l_receiptdate', 'l_shipinstruct', 'l_shipmode', 'l_comment']
type_data_lineitem = ['long', 'long', 'long', 'long', 'double', 'double', 'double', 'double', 'string', 'string', 'date', 'date', 'date', 'string', 'string', 'string']

columns_nation = ['n_nationkey', 'n_name', 'n_regionkey', 'n_comment']
type_data_nation = ['long', 'string', 'long', 'string']

columns_orders = ['o_orderkey', 'o_custkey', 'o_orderstatus', 'o_totalprice', 'o_orderdate', 'o_orderpriority', 'o_clerk', 'o_shippriority', 'o_comment']
type_data_orders = ['long', 'long', 'long', 'string', 'double', 'date', 'string', 'string', 'long', 'string']

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

""" END Configuration Parameters """

select = 'select '
where = ' where '
inner_join = ' inner join '
outer_join = ' left outer join '
on = ' on '
in_ = ' in '
all_multiply = ' * '
from_table = ' from '
menos = ' -'
as_something = ' as result '
as_something2 = ' as result2 '
igual = ' = '
between = ' between '
query = ''
and_ = ' and '

for i in range(len(tableNameList)):
    print "\n tabla: " + tableNameList[i]
    print "campos: \n"
    
    for ii in range(len(tableDescriptionList[i])):
        print " -- " + tableDescriptionList[i][ii]
        
        print "Verify field data type"
        print " -_- " + tableDataTypeList[i][ii]
        
        print "Creando indice de lista random para seleccionar otra tabla y hacer join"
        random_tabla = randint(0,(cant_tables-1))
        print "Indice random de tabla " + str(random_tabla)
        print "Cant campos de random tabla " + str(limits[random_tabla])
        
        if tableDataTypeList[i][ii] == 'date':
            print "Date tests"
            query = select + tableDescriptionList[i][ii] + from_table + tableNameList[i] + where + tableDescriptionList[i][ii] + between + str(radar.random_datetime()) + and_ + str(radar.random_datetime()) + ' \n \n'
            #output_file.write(query)
            comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
            
            """ Generando randoms para date """
            
            
        if tableDataTypeList[i][ii] == 'long' or tableDataTypeList[i][ii] == 'double':
            
            random_limit = randint(0,20)
            random_list = list()
            for x in range(0,random_limit):
                random_list.append(randint(-9000,(x*-1)))
            
            #################################################
            print "Query integer / double * negative value"
            #################################################
            print select + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i]
            query = select + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + '\n \n'
            #output_file.write(query)
            comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
            query = select + 'avg(' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + as_something + from_table + tableNameList[i] + where + tableDescriptionList[i][ii] + in_ + '(' + str(random_list).strip('[]') + ')' + '\n \n'
            #output_file.write(query)
            comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
            
            # generar un aleatorio de tabla y verificar que campo sea del mismo tipo que el campo de la otra tabla, entonces ponerlos como clave del join
            campo_random_del_mismo_tipo = 999
            campo_random_del_mismo_tipo2 = 999
            campo_random_distinto_tipo = 999
            # Buscamos los nº de los indices de los campos que sean del mismo tipo al key de la otra tabla
            campos_mismo_type = list()
            campos_distinto_type = list()
            for iii in range(len(tableDataTypeList[random_tabla])):
                if tableDataTypeList[i][ii] == tableDataTypeList[random_tabla][iii]:
                    campos_mismo_type.append(iii)
                else:
                    campos_distinto_type.append(iii)
                    
            if len(campos_mismo_type) != 0:
                campo_random_del_mismo_tipo = random.choice(campos_mismo_type)
                campo_random_del_mismo_tipo2 = random.choice(campos_mismo_type)
                print " Campo random del mismo tipo " + str(campo_random_del_mismo_tipo)

            ##############################################################
            print "Query integer / double * negative value in inner join"
            ##############################################################
            
            if campo_random_del_mismo_tipo != 999:
                print select + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + inner_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + menos + str(randint(0,700)) + ')' 
                print select + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + ', ' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + tableNameList[i] + '.' + tableDescriptionList[i][ii] + as_something2 + from_table + tableNameList[i] + inner_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + menos + str(randint(0,700)) + ')' 
                query = select + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + inner_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + menos + str(randint(0,700)) + ')' + '\n \n'
                #output_file.write(query)
                comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
                query = select + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + ', ' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + tableNameList[i] + '.' + tableDescriptionList[i][ii] + as_something2 + from_table + tableNameList[i] + inner_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + menos + str(randint(0,700)) + ')' + '\n \n'
                #output_file.write(query)
                comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
                query = select + tableNameList[i] + '.' + tableDescriptionList[i][ii] + where + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + str(randint(-9800,-1)) + between + '(' + str(random_list).strip('[]') + ')' + '\n \n'
                #output_file.write(query)
                comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
                
            #################################################################################################
            print "Query integer / double * negative value when the column has null values & left outer join"
            #################################################################################################
            
            #if len(campos_distinto_type) != 0:
            #    campo_random_distinto_tipo = random.choice(campos_distinto_type)
                
            #if campo_random_distinto_tipo != 999:
            #    print select + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + outer_join + tableNameList[random_tabla] + on + "(" + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ")" + igual + "(" + tableDescriptionList[random_tabla][campo_random_distinto_tipo] + all_multiply + menos + str(randint(0,700)) + ")" 

            if campo_random_del_mismo_tipo != 999:
               print select + tableNameList[i] + "." + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + outer_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + menos + str(randint(0,700)) + ')' 
               query = select + tableNameList[i] + "." + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + outer_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + menos + str(randint(0,700)) + ')' + '\n \n'
               #output_file.write(query)
               comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
               
               if campo_random_del_mismo_tipo2 != 999:
                   print select + tableNameList[i] + "." + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + outer_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo2] + all_multiply + menos + str(randint(0,700)) + ')' 
                   query = select + tableNameList[i] + "." + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + outer_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo2] + all_multiply + menos + str(randint(0,700)) + ')' + '\n \n'
                   #output_file.write(query)
                   comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
				
#output_file.close()
comp.report()
comp.logResults("log_emilse.txt", "version", "memo")