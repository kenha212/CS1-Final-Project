
import arrow
import json
from datetime import datetime, timedelta,date
import pandas as pd
from pandas import DataFrame as dt, Int64Dtype, Int8Dtype 




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
def writeFile(originalfilename, newfilename):
    fileResult = open(originalfilename, 'r')

    newFileResult = open(newfilename, 'w')

    for line in fileResult:
        dctline = json.loads(line)
        picName = dctline['picName']
        if '30' in picName: 
            newFileResult.write(line + '\n')
    
    newFileResult.close()
    fileResult.close()

def txt_emo_check_mayberight(fileName):
    trans_vid1 = json.loads(readFile1(fileName))
    liwc_dict = json.loads(readFile1('liwc_dictionary_final.json'))

    
    text = []   

    for i in range(len(trans_vid1['vtt'])):
        
        if '\n' in str(trans_vid1['vtt'][i]['text']): #In case of /n exist in the text file, the text does not duplicate" 
            x = str(trans_vid1['vtt'][i]['text'])
            head,mid,tail = x.partition('\n')
            text.append(head)
        else:
            text.append(trans_vid1['vtt'][i]['text']) #Appened to form a list of all of the text inside the transcript file"

    emotion_vid1 ={'Topics': ['Words','Percent'],} #Dictionary for the dataframe

    topic_list = []
    topic_wrd  = []  
    
    for topics in liwc_dict['topics']:
        topic_list.append(str(topics)) #Name of the catergories of words
        topic_wrd.append(liwc_dict['dict'][topics])  #List of list of words of each catergory

    words_num = [] 
    
    for m in range(len(text)):
            
            word_lst = (text[m]).split()
            
            words_num.append(len(word_lst))

    total_vid_words = sum(words_num) #Total sum of words in the transcript file
    
    for i in range(len(topic_wrd)): 
        emo_check = []
        for m in range(len(text)):
            word_lst = (text[m]).split()         
            for word in topic_wrd[i]:  #If a word is in a topic, appened the position of that word in a line

                if word in word_lst: 

                    emo_check.append(m+1)
                
        
        percent = (len(emo_check)/total_vid_words)*100 #Percentage of a topic in total of words 
        emotion_vid1[topic_list[i]] =[str(len(emo_check)),' '+ str(percent)]
    





    return emotion_vid1

#trans_vid1 = txt_emo_check_mayberight('transcript_vid1.json')
#trans_vid1_df=pd.DataFrame(data = trans_vid1).T
#trans_vid1_df.to_csv('vid1.csv')
#
#
#
#trans_vid2 = txt_emo_check_mayberight('transcript_vid2.json')
#trans_vid2_df=pd.DataFrame(data = trans_vid2).T
#trans_vid2_df.to_csv('vid2.csv')
    
        


