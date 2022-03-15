# coding=utf-8
import csv
import string
import dateutil.parser
from random import randint
import random
import radar

import sys
sys.path.append('Classes')
#from BlazingDB import connect
from LocalBlazingHandler import LocalBlazingHandler
import BlazingDB

bh = BlazingDB.connect("52.41.136.244", 8890, "6", "emilse")
bp = LocalBlazingHandler("52.41.136.244", 8890, "6", "emilse")

#bh.execute("create table dab (a string(50), b date, c long, d double)")
#bh.execute('insert into dab (a,b,c,d) values ("hola", "20161502", 14, 15.5)')
bh.execute("select a,b,c,d from dab")
bp.runQuery("select a,b,c,d from dab",verbose=True)