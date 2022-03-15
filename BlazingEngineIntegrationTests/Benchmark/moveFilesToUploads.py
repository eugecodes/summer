import shutil
import os

#shutil.copy('/home/ubuntu/supplieraa', '/disk1/blazing/blazing-uploads/2/supplieraa')
shutil.move('/home/ubuntu/supplierab', '/disk1/blazing/blazing-uploads/2/supplierab')

print "The file has successfully moved!"

os.remove('/disk1/blazing/blazing-uploads/2/supplierab')

print "The file has been removed!"
