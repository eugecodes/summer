# coding=utf-8
import csv
import string
import dateutil.parser

class CleanData:
	""" Class to clean data imported from csv """
	
	def FormatDate(format_type, date):
		if format_type == 0:
		   date.strftime('%m/%d/%Y')
		elif format_type == 1:
		   date.strftime('%m-%d-%Y')
		elif format_type == 2:
		   date.strftime('%d/%m/%Y')
		else:
		   print "Without any specified format type"
		   
		return date


    def isDate(col):
        if(len(col) == 10):
            if(col[2] == '.' and col[5] == '.' and col[0:2].isdigit() and col[3:5].isdigit() and col[6:10] ):
                return True
            else:
                return False
        else:
            return False

	def Clean(self, input, output, path, clean_end = 0, clean_start = 0, character_to_replace = ['""""',',"\n"','""','@@@@','\n"'], character_replacement = ['@@@@','\n','"','""',"\n"]):
		""" input is Path/Input_File.csv | output is Path/Output_File.csv """
		print "Clean Start"
		print output
		
		for i_file in range(len(input)):
			file_i = input[i_file]
			print 'Current File Reading :', file_i
			input_file = open(path + file_i, 'r')
			
			data = input_file.read()
			if clean_start > 0:
				data = data[clean_start:] #1
			if clean_end > 0:
				data = data[:-clean_end] #3
				#print data
			
			for i in range(len(character_to_replace)):
				data = data.replace(character_to_replace[i],character_replacement[i])
				data = data.replace(character_to_replace[i],character_replacement[i])
				#print data
			
            data2 = data.split(',')
            for index_data in range(len(data2))
                #print minidata + ' - ' + isDate(mini_data)
                if isDate(data2[index_data]) == True
                    data2[index_data] = FormatDate(0)
            
            data = ",".join(data2)
            
			for o_file in range(len(output)):
				file_o = output[o_file]
				output_file = open(path + file_o, 'w')
				output_file.write(data)
				output_file.close()

			input_file.close()
		