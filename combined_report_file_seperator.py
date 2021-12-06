# -*- coding: utf-8 -*-
"""
Spyder Editor
Author: Navid Heydari

a small script to seperate the input large combined report to small CSV format files.
"""
import uuid

#detecting if the line is empty or not. 
def detect_new_line(line):
    return (line == "\n")

	#simply write to a file using appending mode
def write_to_file(file_name, line):
    file = open(file_name,"a")
    file.write(line)
    file.close()

#processing the large file -- the method is handling the large file reading in an efficient way.
with open("./compiled-results-cpuintensivetaskexperiment.csv") as infile:
	file_name = str(uuid.uuid4()) + "-seperated.csv"
	for line in infile:
		if(detect_new_line(line)):
			file_name = str(uuid.uuid4()) + "-seperated.csv"
		else:
			write_to_file(file_name,line) 
        
        
        

    
    








