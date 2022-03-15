
path = "../DataSets/TPCH1Gb/"
tableFileList = ["customer.tbl", "lineitem.tbl", "nation.tbl", "orders.tbl", "part.tbl", "partsupp.tbl", "region.tbl", "supplier.tbl"]



for tableFile in tableFileList:
 
    f = open(path + tableFile,'r')
    filedata = f.read()
    f.close()
 
    newdata = filedata.replace("|\n","\n")

    f = open(path + tableFile,'w')
    f.write(newdata)
    f.close()
            
