#!/usr/bin/env python3
""" 
execute this script after the separet script.
"""

import os
import sys
import csv
import numpy as np


sys.path.append('./test')

file_suffix_to_process = "-exploded.csv"
folderName = '' 
#this collection is a consolidated data at the end and all the final data records are in there
containers_consolidated__data_rows = []
containers_consolidated__data_header = ['containerID','mean_runTime','median_runTime','perc10_runTime','perc25_runTime','perc50_runTime','perc75_runTime','stdv_runTime','avg_runTime','min_runtime','max_runtime','CV']
cold_instance_is_excluded = False
prefix_container_name = "Category containerID with"

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

def calculate_countIf_GREATER_THAN_OR_EQUAL_Field(nums,field):
    return np.count_nonzero(nums >= field)

def calculate_percentile(nums,percentile):
    # return "percentile" + str(percentile) + ":," + str(np.percentile(nums,percentile,axis=0))
    return np.percentile(nums,percentile,axis=0)

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
      


def calculate_buckets(containers_consolidated__data_header,containers_consolidated__data_rows,field_to_calculate_based_on):
    
    #getting mean_runtime -- field_to_calculate_based_on = "mean_runtime"
    target_calc_field_index = containers_consolidated__data_header.index(field_to_calculate_based_on)
    temp_data = []
    for row in containers_consolidated__data_rows:
        temp_data.append(float(row[target_calc_field_index]))
    
    max = calculate_max(temp_data)
    min = calculate_min(temp_data)
    avg = calculate_avg(temp_data)
    percentage_Max_min_or_marginal_line_for_buckets = 0
    if min != 0:
        percentage_Max_min_or_marginal_line_for_buckets = max/min
    
    print("avg," + str(avg))
    print("min," + str(min))
    print("max," + str(max))
    print("percentage margin," + str(percentage_Max_min_or_marginal_line_for_buckets))
    
    print("percentage,percentageVal,range_start,range_end,diff")
    percXX = calculate_percentile(temp_data, 0)
    print("perc"+str(0) + ","+ str(percXX))
    for i in range(10):
        #start from rang 0 to 100
        j = i+1
        percXXX = calculate_percentile(temp_data, (j*10))

        countOfItemsGraterOrEqThanPercXX = calculate_countIf_GREATER_THAN_OR_EQUAL_Field(temp_data, percXX)
        countOfItemsGraterOrEqThanPercXXX = calculate_countIf_GREATER_THAN_OR_EQUAL_Field(temp_data, percXXX)
        diff = countOfItemsGraterOrEqThanPercXX - countOfItemsGraterOrEqThanPercXXX
        print("perc"+str(j*10) + ","+ str(percXXX) + "," + str(countOfItemsGraterOrEqThanPercXX) + "," + str((countOfItemsGraterOrEqThanPercXXX)) + "," + str(diff))
        #prepare for the next round
        percXX = percXXX

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
                    print("COLD INSTANCE ONLY ["+first_line+"]")
                    #skip if newContainer == 0, but capture the rest
                    continue
            #gathering all the data from each container file
            raw_data_per_container.append(int(row[runtime_index]))
           
               
        # handling the empty list inside each one of these methods. (if the container has no other lines = instance experiments rather than COLD ) == just used once and done.
        if not raw_data_per_container:
            # if Empty don't include that to our analysis.
            return
        
        #handling noises
        if len(raw_data_per_container) < 5:
            return
        
        # TODO adding new methods
        processed_data_per_container.append(first_line)
        processed_data_per_container.append(str(calculate_mean(raw_data_per_container)))
        processed_data_per_container.append(str(calculate_median(raw_data_per_container))) 
        processed_data_per_container.append(str(calculate_percentile(raw_data_per_container,10)))
        processed_data_per_container.append(str(calculate_percentile(raw_data_per_container,25)))
        processed_data_per_container.append(str(calculate_percentile(raw_data_per_container,50)))
        processed_data_per_container.append(str(calculate_percentile(raw_data_per_container,75)))
        processed_data_per_container.append(str(calculate_stdv(raw_data_per_container)))
        processed_data_per_container.append(str(calculate_avg(raw_data_per_container)))
        processed_data_per_container.append(str(calculate_min(raw_data_per_container)))
        processed_data_per_container.append(str(calculate_max(raw_data_per_container)))
        processed_data_per_container.append(str(calculate_CV(raw_data_per_container)))
        return processed_data_per_container
    
    

if (len(sys.argv) != 4):
    print("Usage:\n./calcStatisticalAnalysis.py <Path to the seperated csv files.> <cold_instance_is_excluded=False/True> <field to calculate consolidation result based on e.g. mean_runTime or CV>")
    
elif (len(sys.argv) == 4):
    folder_name = sys.argv[1]
    cold_instance_is_excluded = False #sys.argv[2]
    field_to_calculate_based_on = sys.argv[3]
    #a collection to gather data for all the write
    print("finding the seperated files under dir: [" + folder_name + "] -- cold_instance_is_excluded="+str(cold_instance_is_excluded) + " fieldToProcessFinalConsolidationBasedOn=" + field_to_calculate_based_on)
    for file in os.listdir(folder_name):
        if file.endswith(file_suffix_to_process):
            relative_file_path = folder_name + file.__str__()
            # print("matching file name with postfix -- file: [" + relative_file_path + "]")
            #processing and collecting the result.
            d = extract_fields_from_container_csv_file(relative_file_path)
            if d is not None:
                # r=','.join([str(element) for element in d])
                containers_consolidated__data_rows.append(d)                       
    # extract_fields_from_container_csv_file("./history/combined_1day/test/0a24a673-7696-41e0-a0f8-d2bcc649e63e-exploded.csv")                       
    csv_writer(containers_consolidated__data_header,containers_consolidated__data_rows,"GT5_exclude_"+str(cold_instance_is_excluded)+"_COLD_instances_dataAnalysis_statistical_analysis_per_Container.csv")
    
    #field_to_calculate_based_on = "mean_runTime"
    
    #calculate_buckets(containers_consolidated__data_header,containers_consolidated__data_rows,field_to_calculate_based_on)
    





