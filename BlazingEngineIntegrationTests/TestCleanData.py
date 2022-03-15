# coding=utf-8
import sys
sys.path.append('Classes')
from CleanData import CleanData

path = "blazinDB_data/"

tableFileList = ["M_BUSINESS_PARTNER.csv"]
tableCleanFileList = ["M_BUSINESS_PARTNER_output.csv"]

cleaning_data = CleanData()
cleaning_data.Clean(tableFileList, tableCleanFileList, path, 1, 2)