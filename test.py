import os, sys
from datetime import datetime

file = open('testfile.txt','w')

file.write(str(datetime.now()))

file.close()
