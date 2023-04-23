
from email.policy import default
import json
from itertools import chain
from typing import DefaultDict
import arrow


#Example 1 
def readFile1(filename):
    fileResult = open(filename,'r')
    textResult = fileResult.read() 
    fileResult.close() 
    return textResult

#def dictFile(x): 
#    dict1 = json.loads(x)
#    return dict1
#
#x = readFile('liwc_dictionary_final.json')
#y = dictFile(x)
#print(y.keys())
#print(y['topics'])
#print(y['dict']['Health'])





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


x = json.loads(readFile1('liwc_dictionary_final.json'))
m = [] 
y = x['dict']['Friend']
for i in x['dict']:
    m.append(len(x['dict'][i]))

dd = DefaultDict(list)
d1= {'a': 1 , 'b':2}
d2= {'a':3, 'b':4}
for d in (d1, d2): # you can list as many input dicts as you want here
    for key, value in d.items():
        dd[key].append(value)

x = arrow.get('00:00:01','HH:mm:ss')
print(x)