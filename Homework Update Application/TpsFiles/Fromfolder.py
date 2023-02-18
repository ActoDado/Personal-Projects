from pprint import pprint
from os import listdir
from os.path import isfile, join, isdir
import sys
import time
import requests
import datetime

datedict = {}

def settings():
    handle = open("C:\Program Files (x86)\TpsFiles\debugsettings.txt",'r')
    doc = []
    for line in handle:
        doc.append(line.rstrip('\n'))
    for i in range(0,len(doc)-1):
        if 'Folder Path:' in doc[i]:
            path = doc[i+1]
        else:
            pass
    return path

try:
    path1 = settings()
except Exception as e:
    print("WARNING!! Settings TAMPERED...")
    print(f'Error Here:{e}')
    randsleep()
    os.system('cls')

    
def getname(inp):
    global path1
    mypath = path1 + str('\\' + inp)
    #print(mypath)
    while True:
        #x = str(input('Enter the folder name: '))
        if not(len(inp)==3 and inp[0]=='t' and isdir(mypath)):
            return -1
        else:
            break
    #mypath = path + str('\\' + inp)
    return mypath
    
def getdates(mypath):
    def intchecker(name):
        try:
            name = int(name)
            return True
        except:
            return False
    dfolders = [f for f in listdir(mypath) if intchecker(f)]
    dates = []
    for date in dfolders:
        x = datetime.datetime(int('20'+date[-2:]),int(date[-4:-2]),int(date[-6:-4]))
        dt = x.strftime("%B %d, %Y")
        dates.append(dt)
    return dates

def getfolders(mypath):
    def intchecker(name):
        try:
            name = int(name)
            return True
        except:
            return False
    datefolders = [f for f in listdir(mypath) if intchecker(f)]
    return datefolders

def getclasses(folders,mypath):
    classd = {}
    for folder in folders:
        x = datetime.datetime(int('20'+folder[-2:]),int(folder[-4:-2]),int(folder[-6:-4]))
        dt = x.strftime("%B %d, %Y")
        path = mypath+str('\\'+folder)
        classes = [path+str('\\'+f) for f in listdir(path)]
        classd[dt] = classes
    return classd 

        
##pname = getname()
##folders = getfolders(pname)
##classd = getclasses(folders,pname)
