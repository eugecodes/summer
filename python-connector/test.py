from blazingdb import BlazingPyConnector

bl = BlazingPyConnector('52.41.136.244','felipe@blazingdb.com','tester','emilse')
con = bl.connect()
result = bl.run("create table my_new_table (field1 string(20), field2 long, field3 date, field4 double)",con)
print result.status
print result.rows