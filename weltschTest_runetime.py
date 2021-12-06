#!/usr/bin/env python3
""" 
execute this script after the separet script.

"""

import os
import sys
import csv
from scipy import stats
import numpy as np


sys.path.append('./test')

file_suffix_to_process = "-exploded.csv"
folderName = '' 
#this collection is a consolidated data at the end and all the final data records are in there
containers_consolidated__data_rows = []
containers_consolidated__data_header = ['container_name','totalContainerRecordSize','EachContainerSize','statistics','pValue','avg_runtime_perContainer','mean_total_population','subtract meanContainer from total','std_runtime_perContainer','cv_each_container','total_population_cv','df','level','container_raw']
cold_instance_is_excluded = True
prefix_container_name = "Category containerID with"

#assumption of no equal variance = FALSE
def calculate_welc_ttest(a,b):
    return stats.ttest_ind(a,b,equal_var=False)

def calculate_min(nums):
    return np.min(nums)

def calculate_max(nums):
    return np.max(nums)

def calculate_median(nums):
    return np.median(nums)

def calculate_stdv(nums):
    return np.std(nums,axis=0)

def calculate_stdv_to_number(nums):
    return np.std(nums,axis=0)

def calculate_mean(nums):
    return np.mean(nums,axis=0)

def calculate_mean_to_number(nums):
    return np.mean(nums,axis=0)

def calculate_avg(nums):
    return np.average(nums)

def calculate_degree_of_freedome(set1,set2):
    return len(set1) + len(set2) - 2

# ---- adding the CV calculation here 
def calculate_CV(nums):
    stdv_temp = calculate_stdv_to_number(nums)
    mean_temp = calculate_mean_to_number(nums)
    result = 0
    if mean_temp == 0:
        result
    else:
        result= stdv_temp/mean_temp
    return result

        
#handling newline as python documentation to avoid universal newline
def csv_writer(header, data, filename):
  with open (filename, 'w',newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)
    for row in data:
      csv_writer.writerow(row)
      

#this method will extract each CSV file (each container) file data.
def extract_fields_from_container_csv_file(csv_file_name):
    
    with open(csv_file_name, 'r') as csvfile:
        processed_data_per_container = []
        raw_data_per_container = []
        
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        first_line = next(csvreader)[0] 
        #skip the first row which can be the container id,etc.
        if not (first_line.startswith(prefix_container_name)):
            # NOT the file for container -- doesn't have the starter line
            return
        if (first_line.startswith(prefix_container_name)):
            # print(">>>Processing ... " + first_line)
            #extract the header fields from CSV files
            header = next(csvreader)
            # print(str(header)) # CSV HEADER DATA
            # processed_container_row = str(header)
        runtime_index = header.index("runtime")
        new_container_index = header.index("newcontainer")
        
        for row in csvreader:
            # print(row[runtime_index])
            if cold_instance_is_excluded is True:
                if row[new_container_index] == "1": 
                    #print("COLD INSTANCE ONLY ["+first_line+"]")
                    #skip if newContainer == 0, but capture the rest
                    continue
            #gathering all the data from each container file
            raw_data_per_container.append(int(row[runtime_index]))
           
               
        # handling the empty list inside each one of these methods. (if the container has no other lines = instance experiments rather than COLD ) == just used once and done.
        if not raw_data_per_container:
            # if Empty don't include that to our analysis.
            #print("empty collection")
            return None
        
        #handling noises
        if len(raw_data_per_container) < 0:
            return None
        #print(first_line)
        return [first_line,raw_data_per_container]
    
    

if (len(sys.argv) != 2):
    print("Usage:\n./welstchTest_runner.py <Path to the seperated csv files.>")
    
elif (len(sys.argv) == 2):
    folder_name = sys.argv[1]
    #a collection to gather data for all the write
    print("finding the seperated files under dir: [" + folder_name + "] - Processing the Welch T-Test" )
    
    
    #---------- init
    #this is the base container data for calc ttest
    base_container_data = []
    all_containers_data = []
    all_container_names = []
    #no seperation by containers.
    all_containers_data_raw = []
    
    for file in os.listdir(folder_name):
        if file.endswith(file_suffix_to_process):
            relative_file_path = folder_name + file.__str__()
            print("matching file name with postfix -- file: [" + relative_file_path + "]")
            #processing and collecting the result.
            #data_per_container = extract_fields_from_container_csv_file(relative_file_path)
            l = extract_fields_from_container_csv_file(relative_file_path)
            if l is not None:
                if l[1] is not None:
                    data_per_container = l[1]
                    all_containers_data.append(data_per_container)
                    all_containers_data_raw.extend(data_per_container)
                    all_container_names.append(l[0])
    #get the mean of total population
    mean_total_population = calculate_mean(all_containers_data_raw)
    print(str(mean_total_population))
# =============================================================================
#     print(str(len(all_container_names)))
#     axularyList = list(set(all_container_names))
#     print(str(len(axularyList)))
# =============================================================================
    for container_data in all_containers_data:
        if len(container_data) < 15:
            continue
        result_to_save_into_csv = []
        res_ttest = stats.ttest_ind(all_containers_data_raw,container_data,equal_var=False)
        #cleanining container name --  replacing ""Category containerID with ""
        result_to_save_into_csv.append(all_container_names[all_containers_data.index(container_data)].replace("Category containerID with ",""))
        result_to_save_into_csv.append(str(len(all_containers_data_raw)))
        result_to_save_into_csv.append(str(len(container_data)))
        result_to_save_into_csv.append(str(res_ttest.statistic))
        result_to_save_into_csv.append(str(res_ttest.pvalue))
        container_runetime_mean = calculate_mean(container_data)
        result_to_save_into_csv.append(str(container_runetime_mean))
        result_to_save_into_csv.append(str(mean_total_population))
        runTimeDiff_againstTotal = container_runetime_mean - mean_total_population
        result_to_save_into_csv.append(str(runTimeDiff_againstTotal))
        result_to_save_into_csv.append(str(calculate_stdv(container_data)))
        result_to_save_into_csv.append(str(calculate_CV(container_data)))
        result_to_save_into_csv.append(str(calculate_CV(all_containers_data_raw)))
        result_to_save_into_csv.append(str(calculate_degree_of_freedome(container_data,all_containers_data_raw)))
        
        if res_ttest.pvalue < 0.1:
            if mean_total_population < container_runetime_mean:
                result_to_save_into_csv.append('SLOW')
            else:
                result_to_save_into_csv.append('FAST')
        else:
            if mean_total_population < container_runetime_mean:
                result_to_save_into_csv.append('NS - SLOW')
            else:
                result_to_save_into_csv.append('NS - FAST')
                
        result_to_save_into_csv.append(str(container_data))
        containers_consolidated__data_rows.append(result_to_save_into_csv)
        csv_writer(containers_consolidated__data_header,containers_consolidated__data_rows,"Welsh-Test-GT15_exclude_"+str(cold_instance_is_excluded)+"_COLD_instances_per_Container_rawdataaddedAVGadded_skipGT0_1_cvTotalAdded.csv")


        
            


    print("finished processing")
                



