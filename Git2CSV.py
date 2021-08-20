#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import json
import os 
import sys
import csv
import datetime
import subprocess

n = len(sys.argv)

if n > 1:
    mydir = os.getcwd() 
    mydir_tmp = sys.argv[1]
    mydir_new = os.chdir(mydir_tmp) 
    mydir = os.getcwd() 
else:
    mydir = os.getcwd() 
    mydir_tmp = "C:\\Users\\Whitt\\hallewhittaker" 
    mydir_new = os.chdir(mydir_tmp) 
    mydir = os.getcwd()

z= subprocess.run('git ls-tree --full-tree --name-only -r HEAD', stdout= subprocess.PIPE)
stan_out = z.stdout

finalArray = []
filearray = stan_out.split(b'\n')

for i in filearray:
    x= i.decode("utf-8")
    finalArray.append(x)
finalArray.remove("")

arrayofDictionaries = []
for i in range(len(finalArray)):
    r= subprocess.run('git --no-pager blame --line-porcelain {}'.format(finalArray[i]),stdout= subprocess.PIPE)
    standard_out = r.stdout
    linearray = standard_out.split(b'\n') 

    # print("Current length of dictionary: " + str(len(arrayofDictionaries)))
    # print("We're currently analyzing the file: " + finalArray[i])

    count = 0
    tempdictionary = {}
    for individL in linearray:
        individL = individL.decode("ISO-8859-1")
        splitline = individL.split(" ") 

        temp_key_name = splitline[0]
        first_word_removed = splitline.copy()
        first_word_removed[0] = " "
        first_word_removed = " ".join(first_word_removed).lstrip()

        if count == 0:
            tempdictionary["hash"] = temp_key_name
            commitNumbers = first_word_removed.split(" ") 

            for i in range(0, len(commitNumbers)):
                try:
                    commitNumbers[i] = int(commitNumbers[i])
                except:
                    None

            if len(commitNumbers) == 3:
                tempdictionary["CommitLinesN"] = {'originalLine': commitNumbers[0], 'finalLine': commitNumbers[1], 'groupLine' : commitNumbers[2]}
            elif len(commitNumbers) == 2:
                tempdictionary["CommitLinesN"] = {'originalLine': commitNumbers[0], 'finalLine': commitNumbers[1] } 
        
        elif count >= 1 and count <= 12:
            if count == 3:
                int_time_author= int(first_word_removed)
                date_author_time = datetime.datetime.fromtimestamp(int_time_author)   
                tempdictionary["author-time"] = date_author_time 
                
            elif count == 4:
                authortz = datetime.datetime.strptime(first_word_removed,'%z').tzinfo
                new_atz = datetime.timezone.tzname( authortz, None )
                tempdictionary["author-tz"] = new_atz
                tempdictionary["author-time"].replace(tzinfo=authortz)
        
            elif count == 7:
                int_time_commiter= int(first_word_removed)
                date_commiter_time = datetime.datetime.fromtimestamp(int_time_commiter)
                tempdictionary["commiter-time"] = date_commiter_time
    
            elif count == 8:
                commitertz = datetime.datetime.strptime(first_word_removed,'%z').tzinfo
                new_ctz = datetime.timezone.tzname( commitertz, None )
                tempdictionary["commiter-tz"] = new_ctz
                tempdictionary["commiter-time"].replace(tzinfo=commitertz)
            
            elif individL[0:1] == '\t':
                slice_string = individL[1:]
                tempdictionary["commit_content"] = slice_string.lstrip()

            else:
                tempdictionary[temp_key_name] = first_word_removed

        count += 1 
        for key,value in dict(tempdictionary).items():
            if key == "commit_content":
                # print(tempdictionary)
                arrayofDictionaries.append(tempdictionary.copy()) # TODO: check if copy is actually needed, it won't hurt, but it'll slow things down and take extra memory.
                # print(len(arrayofDictionaries))
                tempdictionary = {} 
                count = 0
        #break
    #print("Final Array:" + str(arrayofDictionaries))

print("Final length of dictionary: " + str(len(arrayofDictionaries)))

def myconverter(k):
    if isinstance(k, datetime.datetime):
        return k.__repr__()
jsonstring= json.dumps(arrayofDictionaries, default = myconverter)

fieldnames = ['hash','CommitLinesN', 'author','author-mail','author-time','author-tz','committer','committer-mail', 'commiter-time','commiter-tz','summary', 'previous', 'boundary', 'filename','commit_content']
rows = arrayofDictionaries


try:
    filetype = sys.argv[2].split(".") # What if I have the filename of "this.is.a.file.json"? =P 
except:
    None

if n > 2 and filetype[1] == "csv": 
    filename_csv= sys.argv[2]
    with open('C:\\Users\\Whitt\\hallewhittaker\\{}'.format(filename_csv), "w+", encoding='ISO-8859-1', newline='') as sys.stdout:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
else: 
    filename_csv = 'TestCSV.csv'
    with open(filename_csv, 'w+', encoding='ISO-8859-1', newline='') as f: 
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if n > 2 and filetype[1] == "json":
    filename_json= sys.argv[2]
    sys.stdout = open('C:\\Users\\Whitt\\hallewhittaker\\{}'.format(filename_json), "w+", encoding='ISO-8859-1', newline='') 
    sys.stdout.write(jsonstring) # it is only priniting final array, it is overwriting the rest. I have tried using a,w, w+ and opening the file outside of the array, and attempted to use a for loop for writing to file. No luck 
    sys.stdout.close() # the problem could also be realted to jsonstring, as when i print this i get the finalarray in array of dict as well
else:
    filename_json= "data.json"
    jsonFile = open(filename_json, "w+")
    jsonFile.write(jsonstring)
    jsonFile.close()


#Task 1
#Where all output? only like 12 lines, why?

#Task 2
#Fix random text in actual output

#Task 3
#Fix commit lines to 1,1,1


#Manual Directory Paths
# mydir_tmp = "C:\\Users\\Whitt\\hallewhittaker\\FormatFuzzer" #runs formatfuzzer
# mydir_tmp = "C:\\Users\\Whitt\\hallewhittaker" #runs Git2CSV

#Commands to specify folder
# py Git2CSV.py C:\Users\Whitt\hallewhittaker 
# py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer 

#Further Commands to Specify Output
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer data.json   (use me)
#py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer TestCSV.csv (use me)







#Previous Code:
#  filename_csv = sys.argv[2]
#     with open(filename_csv, 'w+', encoding='ISO-8859-1', newline='') as f: # woot woot, this looks good!
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(rows)

# if len(sys.argv) > 2:
#     filename_json= json_output #sys.argv[2]
#     jsonFile = open(filename_json, "w+")
#     jsonFile.write(jsonstring)
# else:
#     filename_json= "data.json"
#     jsonFile = open(filename_json, "w+")
#     jsonFile.write(jsonstring)
# jsonFile.close()
  
# fieldnames = ['hash','CommitLinesN', 'author','author-mail','author-time','author-tz','committer','committer-mail', 'commiter-time','commiter-tz','summary', 'previous', 'boundary', 'filename','commit_content']
# rows = arrayofDictionaries

# if len(sys.argv) > 2:
#     filename_csv = csv_output #sys.argv[2]
#     with open(filename_csv, 'w+', encoding='ISO-8859-1', newline='') as f: # woot woot, this looks good!
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(rows)
# else:
#     filename_csv = 'TestCSV.csv'
#     with open(filename_csv, 'w+', encoding='ISO-8859-1', newline='') as f: 
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(rows)
