#!/usr/bin/env python3
""" 
execute this script after the separet script. this will execute and add the lable to the csv file based on runtime quartile. 
this field will be used as a controller field to validate if the buckets can be defined in an easy and simple way.

"""
import sys
import csv
import numpy as np
import pandas as pd

sys.path.append('./test')

def calculate_percentile(nums,percentile):
    # return "percentile" + str(percentile) + ":," + str(np.percentile(nums,percentile,axis=0))
    return np.percentile(nums,percentile,axis=0)


#handling newline as python documentation to avoid universal newline
def csv_writer(header, data, filename):
  with open (filename, 'w',newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)
    for row in data:
      csv_writer.writerow(row)
      

if (len(sys.argv) != 2):
    print("Usage:\n./<thisScriptName>.py <csv_file_name_to_add_label_based_on_quartile.>")
    
elif (len(sys.argv) == 2):
    file_name = sys.argv[1]
    #a collection to gather data for all the write
    print("reading file: [" + file_name + "] ..." )
    
    df = pd.read_csv(file_name)
    print(df.head())
    print(df.shape)
    
    runtime_col_data = df['runtime'].tolist()
    
    _25_quartile_bucket = 396#calculate_percentile((runtime_col_data),25)
    _50_quartile_bucket = 413# calculate_percentile((runtime_col_data),50)
    _75_quartile_bucket = 449#calculate_percentile((runtime_col_data),75)
    
    print("25%={} 50%={} 75%={}".format(_25_quartile_bucket,_50_quartile_bucket,_75_quartile_bucket))
    labels = []
    for index, row in df.iterrows():
        row_runtime = row['runtime']
        if(row_runtime <= _25_quartile_bucket):
            labels.append('VERY_FAST')
            continue
        elif(row_runtime <= _50_quartile_bucket):
            labels.append('FAST')
            continue
        elif(row_runtime <= _75_quartile_bucket):
            labels.append('SLOW')
            continue
        else:
            labels.append('VERY_SLOW')
        
        #print(df.head())
        #print(df.shape)
    
    df['container_label'] = labels
    print(df.head())
    df.to_csv("./predict_data_added_label.csv",index=False, header=True)
    print("finished processing")
                



