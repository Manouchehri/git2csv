#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os 
import sys

n = len(sys.argv)
 
if len(sys.argv) > 1:
    mydir = os.getcwd() 
    mydir_tmp = sys.argv[1]
    mydir_new = os.chdir(mydir_tmp) 
    mydir = os.getcwd() 
else:
    mydir = os.getcwd() 
    mydir_tmp = "C:\\Users\\Whitt\\hallewhittaker"
    mydir_new = os.chdir(mydir_tmp) 
    mydir = os.getcwd()


#Fourth Task, fix bug (problem is with bytes)
#UnicodeDecodeError: 'utf-8' codec can't decode byte 0x9c in position 9: invalid start byte with utf-8
#UnicodeDecodeError: 'utf-32-le' codec can't decode bytes in position 0-3: code point not in range(0x110000)



import datetime
import subprocess

z= subprocess.run('git ls-tree --full-tree --name-only -r HEAD', stdout= subprocess.PIPE)
stan_out = z.stdout

finalArray = []
filearray = stan_out.split(b'\n')

for i in filearray:
    x= i.decode("utf-8")
    finalArray.append(x)
finalArray.remove("")

for i in range(len(finalArray)):
    r= subprocess.run('git --no-pager blame --line-porcelain {}'.format(finalArray[i]),stdout= subprocess.PIPE)
    standard_out = r.stdout
    arrayofDictionaries = []
    linearray = standard_out.split(b'\n') 

    count = 0
    tempdictionary = {}
    for individL in linearray:
        individL = individL.decode("utf-8")
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
                arrayofDictionaries.append(tempdictionary)
                tempdictionary = {} 
                count = 0 
    print("Final Array:" + str(arrayofDictionaries))




# First task: get this working in a terminal. =P Hint: you already have python installed, but it likely isn't in your computer's "PATH".
# python3 Git2CSV.py (current argument, empty string give default value)

# python_script = sys.argv[0]
# python_argument = sys.argv[1]

#Manual Directory Paths
# mydir_tmp = "C:\\Users\\Whitt\\hallewhittaker\\FormatFuzzer" #runs formatfuzzer
# mydir_tmp = "C:\\Users\\Whitt\\hallewhittaker" #runs Git2CSV

#Commands to specify folder
# py Git2CSV.py C:\Users\Whitt\hallewhittaker 
# py Git2CSV.py C:\Users\Whitt\hallewhittaker\FormatFuzzer 
