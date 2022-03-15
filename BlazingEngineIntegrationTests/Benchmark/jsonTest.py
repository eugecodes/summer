import json
import time
import datetime
import sys
sys.path.append('../Classes')
from TPCH_HELPER import TPCH_HELPER



tpch = TPCH_HELPER()
json_data=open("jsonPractice.json").read()

queryList = json.loads(json_data)
# print queryList

for query in queryList:
    qstr = queryList[query]['sql']
    # print qstr
    current_index = qstr.find("<parse_value>",0)
    while current_index !=-1:
        sql_edit = qstr[(current_index + 13) : qstr.find("</parse_value>", current_index + 1 )]
        # print '<parse_value> found at : ' + str(current_index)
        # print '</parse_value> found at : ' + str(qstr.find("</parse_value>", current_index + 1 ))
        edit_data = sql_edit.split('|')
        # print 'the edit_type is: ' + edit_data[0]

        if edit_data[0] == 'date_range':
            #Get a date w/in a range
            rand_date = str(tpch.random_date(edit_data[1], edit_data[2]))
            qstr = tpch.replace_qstr(qstr, sql_edit, rand_date)

        elif edit_data[0] == 'date_range_plus':
            #Get a date w/ in a range and add days to it
            rand_date = str(tpch.random_date_plus(edit_data[1]))
            qstr = tpch.replace_qstr(qstr, sql_edit, rand_date)

        elif edit_data[0] == 'date_range_jan':
            #Get a date on first of a random year.
            rand_date = tpch.random_date_year(int(edit_data[1]),int(edit_data[2]))
            qstr = tpch.replace_qstr(qstr, sql_edit, str(rand_date))

        elif edit_data[0] == 'num_range':
            #Get an integer w/in a range
            rand_number = str(tpch.random_int(int(edit_data[1]), int(edit_data[2])))
            qstr = tpch.replace_qstr(qstr, sql_edit, rand_number)

        elif edit_data[0] == 'float_range':
            #Get a float w/in a range
            rand_number = str(round(tpch.random_float(float(edit_data[1]), float(edit_data[2])),2))
            qstr = tpch.replace_qstr(qstr, sql_edit, rand_number)

        elif edit_data[0] == 'array_range':
            #Get an element from an array of elements
            rand_element = tpch.random_element(edit_data[1])
            qstr = tpch.replace_qstr(qstr, sql_edit, rand_element)

        current_index = qstr.find("<parse_value>", current_index + 1 ) #Sets the index so we grab next <parse_value>
    
    #print qstr
    output_file = open("queries_log.txt", 'a')
    output_file.write(qstr + '\n')
    output_file.close()
    
    # print queryList[query]['sql']
