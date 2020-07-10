# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:47:44 2020

@author: Jim
"""

import csv
import time
from shutil import copyfile

start_time=time.time()

src = "C:/Users/Jim/Documents/Ergasia_2_IR/PAC_topics/"
dst = "C:/Users/Jim/Documents/Ergasia_2_IR/PAC_topics/run_topics/"

with open (src +'AssignmentPhase 2 - Run Topics.txt', 'r') as f:
    run_topics_list = [row[0] for row in csv.reader(f,delimiter='\n')]

for files in run_topics_list:
    from_file = src +"files/" +files +".xml"
    to_file = dst +files +".xml"
    copyfile(from_file, to_file)
        
elapsed_time=time.time()-start_time
print("Finished! Elapsed Time = " +str(round(elapsed_time)) +" sec")