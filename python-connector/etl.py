#!/usr/bin/python
from blazingdb import BlazingPyConnector
import psycopg2 as pg

# Blazing Connection
#bl = BlazingPyConnector('52.41.136.244','felipe@blazingdb.com','tester','emilse')
#con = bl.connect()

# Get the describe table
conn = pg.connect(host='localhost',dbname='test',user='postgres',password='postgres')
consulta = "select mytables.table_name from INFORMATION_SCHEMA.COLUMNS as i_columns left join information_schema.tables mytables on i_columns.table_name = mytables.table_name where mytables.table_schema = 'public' and mytables.table_type = 'BASE TABLE';"
cursor = conn.cursor()
resultado = cursor.execute(consulta)
status = cursor.statusmessage
try:
    tables = []
    for row in cursor.fetchall():
        tables.append(row[0]) # tables name
except:
    print "No results returned" 
    
# Get table names
tables_names = set(tables)
#print tables_names

# Loop by tables
for table in tables_names:
    #print "table " + table
    consulta = "select column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS as i_columns left join information_schema.tables mytables on i_columns.table_name = mytables.table_name where mytables.table_schema = 'public' and mytables.table_type = 'BASE TABLE' and mytables.table_name = '" + table + "';"
    cursor = conn.cursor()
    resultado = cursor.execute(consulta)
    status = cursor.statusmessage
    #print "count columns " + status
    try:
        columns = []
        for col in cursor.fetchall():
            
            # Convert DataTypes and Save String
            blazing_type = 'datatype'
            if(col[1] == 'integer'):
                blazing_type = 'long'
            if(col[1] == 'character varying'):
                blazing_type = 'string('+str(col[2])+')'
            if(col[1] == 'character'):
                blazing_type = 'string('+str(col[2])+')'
            if(col[1] == 'text'):
                blazing_type = 'string('+str(col[2])+')'
            if(col[1] == 'time with time zone'):
                blazing_type = 'string('+str(col[2])+')'
            if(col[1] == 'time without time zone'):
                blazing_type = 'string('+str(col[2])+')'
            if(col[1] == 'timestamp with time zone'):
                blazing_type = 'string('+str(col[2])+')'
            if(col[1] == 'timestamp without time zone'):
                blazing_type = 'string('+str(col[2])+')'
            if(col[1] == 'money'):
                blazing_type = 'double'
            if(col[1] == 'real'):
                blazing_type = 'double'
            if(col[1] == 'numeric'):
                blazing_type = 'double'
            if(col[1] == 'double precision'):
                blazing_type = 'double'
            if(col[1] == 'date'):
                blazing_type = 'date'
            if(col[1] == '"char"'):
                blazing_type = 'string'
            if(col[1] == 'bigint'):
                blazing_type = 'long'
            if(col[1] == 'smallint'):
                blazing_type = 'long'
            if(col[1] == 'bit'):
                blazing_type = 'long'
            
            # Make the describe table line
            columns.append(col[0] + ' ' + blazing_type)       
        
        # join columns array by table
        columns_desc = ', '.join(columns)
        
        # Create Tables on Blazing
        #result = bl.run('create table ' + table + ' (' + columns_desc + ')',con)
        #print result.status
        #print result.rows
        
        # Get data in chunks by table ans save in csv
        # Get table content
        consulta = "select * from "+table
        cursor = conn.cursor()
        resultado = cursor.execute(consulta)
        num_rows = cursor.statusmessage[7:]
        #print num_rows
        chunk_size = 100000
        path = 'datasets/'
        if(int(num_rows) <= int(chunk_size)):
            file = open(path+table+'.tbl', 'w')
            try:
                for row in cursor.fetchall():
                    file.write('|'.join(str(r) for r in row)+'\n')
            except Exception as e:
                print e
                
            file.close()
            # Load Data Infile Blazing
            result = bl.run('load data infile' + table + ' (' + columns_desc + ')',con)
            #print result.status
        else:
            #chunk
            iterations = int(num_rows) / chunk_size
            #print "iter" + str(iterations)
            for i in range(int(iterations)):
                #print "i" + str(i)
                file = open(path+table+'_'+str(i)+'.tbl', 'w')
                try:
                    for row in cursor.fetchmany(chunk_size):
                        #print row
                        file.write('|'.join(str(r) for r in row)+'\n')
                except Exception as e:
                    print e
                    
                file.close()
                # Load Data Infile Blazing
                result = bl.run("load data infile" + path+table+"_"+str(i)+".tbl" + " into table " + table + " fields terminated by '|' enclosed by '\"' lines terminated by '\n'",con)
                print result.status
        
              
    except Exception as e:
        print e 
        
#print describe_table

conn.close()