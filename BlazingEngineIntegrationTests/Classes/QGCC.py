# coding=utf-8
import csv
import string
import dateutil.parser
from random import randint
import random
import radar

import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet

class RandomQueryGenerator:
    'Create random queries for any table'

    def __init__(self, ct, tableDescriptionList, tableDataTypeList, limits, cant_tables, tableNameList):
        self.ct = ct
        self.tableDescriptionList = tableDescriptionList
        self.tableDataTypeList = tableDataTypeList
        self.limits = limits
        self.cant_tables = cant_tables
        self.tableNameList = tableNameList
    
    # Main interaction functions
    def generateRandom(self, **kwargs):
        ' Main function of generation of Queries '
        
        select = 'select '
        where = ' where '
        inner_join = ' inner join '
        outer_join = ' left outer join '
        full_outer_join = ' full outer join '
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
        limit_q = ' limit '
        
        # Main Parameters
        tableNameList = self.tableNameList
        comp = self.ct
        tableDescriptionList = self.tableDescriptionList
        tableDataTypeList = self.tableDataTypeList
        limits = self.limits
        cant_tables = self.cant_tables
        
        # Optional parameters
        to_file = kwargs.get("to_file", False)
        output_file_ = kwargs.get("file", "")
        to_json = kwargs.get("to_json", False)
        comparison_test = kwargs.get("comparison_test", True)
        comparison_test_log_file = kwargs.get("log_file", "")
        debug = kwargs.get("debug", False)
        limit_results = kwargs.get("limit_results", 0)
        negative_test = kwargs.get("test_negatives", True)
        string_test = kwargs.get("test_strings", True)
        date_test = kwargs.get("test_dates", True)
        
        limit_my_query = ""
        
        if(limit_results > 0):
            limit_my_query = limit_q + str(limit_results)
        
        if(to_file == True and len(output_file_) != 0):
            output_file = open(output_file_, 'a')
        
        for i in range(len(tableNameList)):
            if(debug == True):
                print "\n tabla: " + tableNameList[i]
                print "campos: \n"
            
            for ii in range(len(tableDescriptionList[i])):
                if(debug == True):
                    print " -- " + tableDescriptionList[i][ii]
                    
                    print "Verify field data type"
                    print " -_- " + tableDataTypeList[i][ii]
                
                    print "Creando indice de lista random para seleccionar otra tabla y hacer join"
                    
                random_tabla = randint(0,(cant_tables-1))
                
                if(debug == True):
                    print "Indice random de tabla " + str(random_tabla)
                    print "Cant campos de random tabla " + str(limits[random_tabla])
                
                """ STRING TESTS """
                if tableDataTypeList[i][ii] == 'string':
                    
                    if(debug == True):
                        print "String tests"
                    
                    """ Generando randoms para string """
                    campo_random_del_mismo_tipo = 999
                    campo_random_del_mismo_tipo2 = 999
                    campos_mismo_type = list()
                    
                    if(debug == True):
                        print "Lenght tableDataTypeList " + str(len(tableDataTypeList[i]))
                    
                    for iii in range(len(tableDataTypeList[i])):
                        if tableDataTypeList[i][ii] == tableDataTypeList[i][iii]:
                            campos_mismo_type.append(iii)
                            
                    if len(campos_mismo_type) != 0:
                        campo_random_del_mismo_tipo = random.choice(campos_mismo_type)
                        campo_random_del_mismo_tipo2 = random.choice(campos_mismo_type)
                        
                    if(debug == True):
                        print "campo_random_del_mismo_tipo " + str(campo_random_del_mismo_tipo)
                        print "campo_random_del_mismo_tipo2 " + str(campo_random_del_mismo_tipo2)
                        print "table " + tableNameList[i]
                    
                    if campo_random_del_mismo_tipo != 999 and campo_random_del_mismo_tipo2 != 999:
                        query = select + tableDescriptionList[i][ii] + from_table + tableNameList[i] + where + tableDescriptionList[i][ii] + between + tableDescriptionList[i][campo_random_del_mismo_tipo] + and_ + tableDescriptionList[i][campo_random_del_mismo_tipo2] + limit_my_query + ' \n \n'
                        
                        if(string_test == True):
                            if(to_file == True):
                                output_file.write(query)
                            
                            if(comparison_test == True):
                                comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
                        
                """ DATE TESTS """
                if tableDataTypeList[i][ii] == 'date':
                    
                    if(debug == True):
                        print "Date tests"
                        
                    query = select + tableDescriptionList[i][ii] + from_table + tableNameList[i] + where + tableDescriptionList[i][ii] + between + str(radar.random_datetime()) + and_ + str(radar.random_datetime()) + limit_my_query + ' \n \n'
                    
                    if(date_test == True):
                        if(to_file == True):
                            output_file.write(query)
                            
                        if(comparison_test == True):
                            comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
                    
                    """ Generando randoms para date """
                    campo_random_del_mismo_tipo = 999
                    campo_random_del_mismo_tipo2 = 999
                    campo_random_del_mismo_tipo_t_orig = 999
                    campo_random_del_mismo_tipo_t_orig2 = 999
                    campos_mismo_type = list()
                    campos_mismo_type_tabla_orig = list()
                    
                    for iiiy in range(len(tableDataTypeList[i])):
                        if tableDataTypeList[i][ii] == tableDataTypeList[i][iiiy]:
                            campos_mismo_type_tabla_orig.append(iiiy)
                    
                    if len(campos_mismo_type_tabla_orig) != 0:
                        campo_random_del_mismo_tipo_t_orig = random.choice(campos_mismo_type_tabla_orig)
                        campo_random_del_mismo_tipo_t_orig2 = random.choice(campos_mismo_type_tabla_orig)
                        
                    if campo_random_del_mismo_tipo_t_orig != 999 and campo_random_del_mismo_tipo_t_orig2 != 999:
                        
                        query = select + tableDescriptionList[i][ii] + from_table + tableNameList[i] + where + tableDescriptionList[i][ii] + between + tableDescriptionList[i][campo_random_del_mismo_tipo_t_orig] + and_ + tableDescriptionList[i][campo_random_del_mismo_tipo_t_orig2] + limit_my_query + ' \n \n'
                        
                        if(date_test == True):
                            if(to_file == True):
                                output_file.write(query)
                                
                            if(comparison_test == True):
                                comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
                        
                    for iii in range(len(tableDataTypeList[random_tabla])):
                        if tableDataTypeList[i][ii] == tableDataTypeList[random_tabla][iii]:
                            campos_mismo_type.append(iii)
                            
                    if len(campos_mismo_type) != 0:
                        campo_random_del_mismo_tipo = random.choice(campos_mismo_type)
                        campo_random_del_mismo_tipo2 = random.choice(campos_mismo_type)
                    
                        if(debug == True):
                            print " Campo random del mismo tipo " + str(campo_random_del_mismo_tipo)
                    
                    if(debug == True):
                        print "##############################################################"
                        print "Query date between"
                        print "##############################################################"
                    
                    if campo_random_del_mismo_tipo != 999 and campo_random_del_mismo_tipo2 != 999:

                        query = select + tableDescriptionList[i][ii] + from_table + tableNameList[i] + inner_join + tableNameList[random_tabla] + on + tableNameList[i] + '.' + tableDescriptionList[i][ii] + igual + tableNameList[random_tabla] + '.' + tableDescriptionList[i][campo_random_del_mismo_tipo] + where + tableNameList[i] + '.' + tableDescriptionList[i][ii] + between + tableNameList[random_tabla] + '.' + tableDescriptionList[i][campo_random_del_mismo_tipo] + and_ + tableNameList[random_tabla] + '.' + tableDescriptionList[i][campo_random_del_mismo_tipo2] + limit_my_query + ' \n \n'
                        
                        if(date_test == True):
                            if(to_file == True):
                                output_file.write(query)
                                
                            if(comparison_test == True):
                                comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
                    
                        query = select + tableDescriptionList[i][ii] + from_table + tableNameList[i] + outer_join + tableNameList[random_tabla] + on + tableNameList[i] + '.' + tableDescriptionList[i][ii] + igual + tableNameList[random_tabla] + '.' + tableDescriptionList[i][campo_random_del_mismo_tipo] + where + tableNameList[i] + '.' + tableDescriptionList[i][ii] + between + tableNameList[random_tabla] + '.' + tableDescriptionList[i][campo_random_del_mismo_tipo] + and_ + tableNameList[random_tabla] + '.' + tableDescriptionList[i][campo_random_del_mismo_tipo2] + limit_my_query + ' \n \n'
                        
                        if(date_test == True):
                            if(to_file == True):
                                output_file.write(query)
                                
                            if(comparison_test == True):
                                comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)

                """ LONG DOUBLE TESTS """
                if tableDataTypeList[i][ii] == 'long' or tableDataTypeList[i][ii] == 'double':
                    
                    random_limit = randint(0,20)
                    random_list = list()
                    for x in range(0,random_limit):
                        random_list.append(randint(-9000,(x*-1)))

                    if(debug == True):
                        print '#################################################'
                        print "Query integer / double * negative value"
                        print '#################################################'
                        print select + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i]
                        
                    query = select + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + limit_my_query + '\n \n'
                    
                    if(negative_test == True):
                        if(to_file == True):
                            output_file.write(query)
                        
                        if(comparison_test == True):
                            comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
                    
                    if(len(random_list) > 0):
                        query = select + 'avg(' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + as_something + from_table + tableNameList[i] + where + tableDescriptionList[i][ii] + in_ + '(' + str(random_list).strip('[]') + ')' + limit_my_query + '\n \n'
                        
                        if(negative_test == True):
                            if(to_file == True):
                                output_file.write(query)
                            
                            if(comparison_test == True):
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
                        
                        if(debug == True):
                            print " Campo random del mismo tipo " + str(campo_random_del_mismo_tipo)
                            
                    if(debug == True):
                        print "##############################################################"
                        print "Query integer / double * negative value in inner join"
                        print "##############################################################"
                    
                    if campo_random_del_mismo_tipo != 999:
                        if(debug == True):
                            print select + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + inner_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + menos + str(randint(0,700)) + ')' 
                            print select + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + ', ' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + tableNameList[i] + '.' + tableDescriptionList[i][ii] + as_something2 + from_table + tableNameList[i] + inner_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + menos + str(randint(0,700)) + ')' 
                        
                        query = select + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + inner_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + menos + str(randint(0,700)) + ')' + limit_my_query + '\n \n'
                        
                        if(negative_test == True):
                            if(to_file == True):
                                output_file.write(query)
                            
                            if(comparison_test == True):
                                comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
                        
                        query = select + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + ', ' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + tableNameList[i] + '.' + tableDescriptionList[i][ii] + as_something2 + from_table + tableNameList[i] + inner_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + menos + str(randint(0,700)) + ')' + limit_my_query + '\n \n'
                        
                        if(negative_test == True):
                            if(to_file == True):
                                output_file.write(query)
                            
                            if(comparison_test == True):
                                comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
                        
                        query = select + tableNameList[i] + '.' + tableDescriptionList[i][ii] + where + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + str(randint(-9800,-1)) + between + '(' + str(random_list).strip('[]') + ')' + limit_my_query + '\n \n'
                        
                        if(negative_test == True):
                            if(to_file == True):
                                output_file.write(query)
                            
                            if(comparison_test == True):
                                comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
                        
                    if(debug == True):
                        print '#################################################################################################'
                        print "Query integer / double * negative value when the column has null values & left outer join"
                        print '#################################################################################################'
                    
                    #if len(campos_distinto_type) != 0:
                    #    campo_random_distinto_tipo = random.choice(campos_distinto_type)
                        
                    #if campo_random_distinto_tipo != 999:
                    #    print select + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + outer_join + tableNameList[random_tabla] + on + "(" + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ")" + igual + "(" + tableDescriptionList[random_tabla][campo_random_distinto_tipo] + all_multiply + menos + str(randint(0,700)) + ")" 

                    if campo_random_del_mismo_tipo != 999:
                       if(debug == True):
                           print select + tableNameList[i] + "." + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + outer_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + menos + str(randint(0,700)) + ')' 
                       
                       query = select + tableNameList[i] + "." + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + outer_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + menos + str(randint(0,700)) + ')' + limit_my_query + '\n \n'
                       
                       if(negative_test == True):
                           if(to_file == True):
                               output_file.write(query)
                           
                           if(comparison_test == True):
                               comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
                       
                       if campo_random_del_mismo_tipo2 != 999:
                           if(debug == True):
                               print select + tableNameList[i] + "." + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + outer_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo2] + all_multiply + menos + str(randint(0,700)) + ')' 
                           
                           query = select + tableNameList[i] + "." + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + as_something + from_table + tableNameList[i] + outer_join + tableNameList[random_tabla] + on + '(' + tableNameList[i] + '.' + tableDescriptionList[i][ii] + all_multiply + menos + str(randint(0,700)) + ')' + igual + '(' + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo] + all_multiply + tableNameList[random_tabla] + '.' + tableDescriptionList[random_tabla][campo_random_del_mismo_tipo2] + all_multiply + menos + str(randint(0,700)) + ')' + limit_my_query + '\n \n'
                           
                           if(negative_test == True):
                               if(to_file == True):
                                   output_file.write(query)
                               
                               if(comparison_test == True):
                                   comp.runAndValidateQuery(query, showVerboseQuery=True, orderless=True, precision=0.01)
        
        if(to_file == True):
            output_file.close()
            
        if(comparison_test == True):
            comp.report()
            comp.logResults(comparison_test_log_file, "version", "memo")