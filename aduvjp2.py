from email.policy import default
from itertools import count
import time
from typing import DefaultDict
import arrow
import json
from matplotlib.font_manager import json_load
import pandas as pd
from pandas import DataFrame as dt, Int64Dtype, Int8Dtype 
import numpy as np
import ast 
from collections import OrderedDict, defaultdict
import operator
import statistics

from operator import itemgetter

def getList(dict): ##Get list of keys of a dictionary
    return dict.keys()

def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value


def readFile1(filename):
    fileResult = open(filename,'r')
    textResult = fileResult.read() 
    fileResult.close() 
    return textResult
def readFile2(filename): #For the visual 
    lstline = []
    fileResult = open(filename,'r')
    for line in fileResult: 
        dctLine = json.loads(line)
        lstline.append(dctLine)

    return lstline
def writeFile(originalfilename, newfilename): #Frame arrangement like 1 2 3 4 5 by a randomly arranged data
    fileResult = open(originalfilename, 'r')

    newFileResult = open(newfilename, 'w')

    pic_list = []
    line_list = []  
    for line in fileResult:
        dctline = json.loads(line)
        line_list.append(line)
        picName = dctline['picName']
        pic_list.append(picName)
    
    
    for i in range(875):   
        
        for k in range(len(line_list)):
           
            if f'"picName":"SFNcWHPHoss__video-frame{i}.jpg"' in line_list[k]: 
                newFileResult.write(line_list[k]+ '\n')

            elif f'"picName":"skEOJA94RIg__video-frame{i}.jpg"' in line_list[k]: 
                newFileResult.write(line_list[k]+ '\n')
        
    
    newFileResult.close()
    fileResult.close()


#writeFile('visual_vid1.json','vs_v1_set.json')
#writeFile('visual_vid2.json','vs_v2_set.json')

def aggerate(set_fileName, annotate_file_Name): 
    vs_v1 = json.loads(readFile1(set_fileName))
    


    data = pd.read_csv(annotate_file_Name)
    start = [] 
    end = [] 
    time_list = [] #I store the time_list as start - end pair
    for s in data.start:
        start.append(s) 

    for e in data.end:
        end.append(e) 

    for r in range(len(start)):
        time_list.append(start[r])
        time_list.append(end[r])

    count = 0 #scene counting
    scences = {'Scenes': ['Classify','Color','Scene','Places']} 
    
    for i in range(len(time_list)):
        if i %2 == 0 and i < len(time_list)-1 and time_list[i] < max(time_list):
            
            pla_dict = DefaultDict(list)
            sce_dict = DefaultDict(list)
            clr_dict = DefaultDict(list)
            cla_dict = DefaultDict(list)    #Make those assignment becomes a dictionary which the value is a list of other dictionaries
            
            count +=1
            if time_list[i] == time_list[i+1]:
                ml_c     = vs_v1[time_list[i]]['imgfeatures']['classify']
                ml_clr   = vs_v1[time_list[i]]['imgfeatures']['true_color']
                ml_sce   = vs_v1[time_list[i]]['imgfeatures']['scene']['scene']
                ml_place = vs_v1[time_list[i]]['imgfeatures']['places']['categories']
            
             

                for key, value in ml_c.items():
                    cla_dict[key].append(value)

                for key, value in ml_clr.items():
                    clr_dict[key].append(value)
                
                for key, value in ml_sce.items():
                    sce_dict[key].append(value)

                for key, value in ml_place.items():
                    pla_dict[key].append(value)
                
                
                

            else:


                for k in range(time_list[i],time_list[i+1],1):
                    ml_c     = vs_v1[k]['imgfeatures']['classify']
                    ml_clr   = vs_v1[k]['imgfeatures']['true_color']
                    ml_sce   = vs_v1[k]['imgfeatures']['scene']['scene']
                    ml_place = vs_v1[k]['imgfeatures']['places']['categories']

                 

                    
                    for key, value in ml_c.items():
                        cla_dict[key].append(value)

                    for key, value in ml_clr.items():
                        clr_dict[key].append(value)

                    for key, value in ml_sce.items():
                        sce_dict[key].append(value)

                    for key, value in ml_place.items():
                        pla_dict[key].append(value)
            
            
            
            cla_average = {obj: sum(obj_ratings) / len(obj_ratings) for obj, obj_ratings in cla_dict.items()} #Calculate the sum
            
            sce_average = {sce: sum(sce_ratings) / len(sce_ratings) for sce, sce_ratings in sce_dict.items()}
            
            clr_average = {clr: sum(clr_ratings) / len(clr_ratings) for clr, clr_ratings in clr_dict.items()}
            
            pla_average = {pla: sum(pla_ratings) / len(pla_ratings) for pla, pla_ratings in pla_dict.items()}

            max_value_cla  = list(dict(sorted(cla_average.items(), key = itemgetter(1), reverse = True)[:3]).keys()) #Select the top 3 keys with the highest mean value
            max_value_clr  = list(dict(sorted(clr_average.items(), key = itemgetter(1), reverse = True)[:3]).keys())
            max_value_sce  = list(dict(sorted(sce_average.items(), key = itemgetter(1), reverse = True)[:3]).keys())
            max_value_pla  = list(dict(sorted(pla_average.items(), key = itemgetter(1), reverse = True)[:3]).keys())

            
            
            lst = [max_value_cla,max_value_clr,max_value_sce,max_value_pla]
            append_value(scences,f'{count}',lst)
    
    return scences

def scence_list(annotate_fileName): #Take data from the human-annotated file
    data = pd.read_csv(annotate_fileName)
    
    ytber = [] 
    food = [] 
    place= [] 

    for y in data.youtuber_existing:
        if y == 1:
            ytber.append(1)
        if y!=0:
            ytber.append(0)
    
    for f in data.food_focus_existing:
        if f ==1:
            food.append(1)
        if f==0:
            food.append(0)
    for p in data.place:
        if p == 1:
            place.append(1)
        if p==0:
            place.append(0)
           
    scene_duration = [] 
    start = [] 
    end = [] 
    time_list = [] 
    
    for s in data.start:
        start.append(s) 

    for e in data.end:
        end.append(e) 
    
    for d in data.duration: 
        scene_duration.append(d)

    for i in range(len(start)):
        time_list.append(start[i])
        time_list.append(end[i])
    
    scence_time = {'Scenes':'Seconds'} 
    count = 0
    for i in range(len(time_list)):
        if i %2 == 0 and i < len(time_list)-1:
            count +=1
            for k in range(time_list[i],time_list[i+1]+1,1):
                append_value(scence_time,f'{count}',k)
    
    

    scence_time['Mean time'] = f"{round(statistics.mean(scene_duration))} seconds"  #Calculate the mean time of youtuber, human, eating places scenes. 
    
    scene_num = len(start)
    scence_time['Food Focus Scenes'] = f"{100*(sum(food)/scene_num)} percent"
    scence_time['Youtuber Focus Scenes'] = f"{100*(sum(ytber)/scene_num)} percent"
    scence_time['Place Existing Scene'] = f"{100*(sum(place)/scene_num)} percent" 
    

    
    return scence_time






#v1_vs = aggerate('vs_v1_set.json','vid1_annotate.csv')            
#v1_df =  pd.DataFrame.from_dict(data = v1_vs,orient='index')
#v1_df.transpose()
#v1_df.to_csv('vsv1_agg.csv')
#
#
#v2_vs = aggerate('vs_v2_set.json','vid2_annotate.csv')            
#v2_df =  pd.DataFrame.from_dict(data = v2_vs,orient='index')
#v2_df.transpose()
#v2_df.to_csv('vsv2_agg.csv')
##
#x = scence_list('vid1_annotate.csv')
#x_df = pd.DataFrame.from_dict(data = x, orient='index')
#x_df.transpose()
#x_df.to_csv('time1.csv')
##
#x2 = scence_list('vid2_annotate.csv')
#x2_df = pd.DataFrame.from_dict(data = x2, orient='index')
#x2_df.transpose()
#x2_df.to_csv('time2.csv')








