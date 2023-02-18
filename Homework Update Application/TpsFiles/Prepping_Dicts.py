import urllib.request
import re
from selenium import webdriver
from pprint import pprint
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import sys
import time
import requests
import os
from Fromfolder import *
import xlwt

username = "enter here"
password = "enter here"
link = "https://topperseducation.sg/index.php"



DEBUG = False

def dprint(text):
    if DEBUG is True:
        pprint(text)

#logging in
def login():
    #incognito part
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options = chrome_options)
    #next part
    driver.get(link)
    driver.find_elements_by_class_name("cancel")[0].click()
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("do-login").click()
    return driver


#uploading correction inside
#FINDING BY XPATH
#RIGHT CLICK, INSPECT, COPY, COPY XPATH,
#THEN USE FIND ELEMENT BY XPATH. EASY


#hovering over
def hoveroverws(driver):
    element_to_hover_over = driver.find_element_by_xpath("/html/body/div/nav/div[2]/div/ul/li[4]/a/span")
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()


#collecting all data from upload ws
def collectfromclass(driver,key):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content,'lxml')
    toptable = soup.find("table", attrs={"id": "order-listing"})
    topdata = toptable.tbody.find_all("tr")  
    # Get all the headings of Lists
    alldict = {}
    tr = 1
    for elem in topdata:
        i = 0
        s = str(elem.button)
        #print(s)
        x = s.lstrip('<button class="btn btn-outline-primary btn-upload-file" data-target="#modal-file-upload" data-toggle="modal" data-ws-id=')
        FinalID = x[:5]
        #print(f'data id onwards: {FinalID,type(FinalID)}')
        #print(FinalID)
        try:
            int(FinalID)
        except:
            FinalID = 'Not Submitted'
        d1 = {0:FinalID}
        for td in elem:
            #print(i,td.text,'\n')
            if i==9:
                #THIS IS CORRECTED/CORRECTION PENDING
                for k in td:
                    #print(k.text)
                    d1['corstat'] = k.text
                break
            if i==7:
                for k in td:
                    #print(k.text)
                    d1['wsstat'] = k.text
                    break
            d1[4] = tr
            if i==3:
                val = td.get("style")
                #print(f'style is {val}')
                if val == 'color:red':
                    #print('\nReached here\n')
                    d1[0] = 'Absent Last Class'
                #print(f'style is {td.get("style")}')
                d1[2] = td.text
            i+=1
        tr+=1
        #pprint(d1)
        if alldict.get(key,-1)==-1:
            alldict[key] = [(d1[2],d1[0],d1[4],d1['corstat'],d1['wsstat'])]
        else:
            alldict[key].append((d1[2],d1[0],d1[4],d1['corstat'],d1['wsstat']))
    return alldict
def collectfromup(driver):
##    driver.implicitly_wait(20)
##    link = driver.find_element_by_link_text('Upload Corrected Worksheet')
##    link.click()
##    select = Select(driver.find_element_by_name('order-listing_length'))
##    select.select_by_value('-1')
    html_content = driver.page_source

    soup = BeautifulSoup(html_content,'lxml')

    toptable = soup.find("table", attrs={"id": "order-listing"})
    topdata = toptable.tbody.find_all("tr")  

    # Get all the headings of Lists
    alldict = {}
    for elem in topdata:
        i = 0
        s = str(elem.button)
        l = s.split('id')
        m = l[1].lstrip('="')
        FinalID = m[:5]
        #print(FinalID)
        d1 = {0:FinalID}
        for td in elem:
            #print(i,td.text,'\n')
            if i==11:
                d1[1] = td.text
            if i==3:
                d1[2] = td.text
            if i==5:
                d1[3] = td.text
            i+=1
        if alldict.get(d1[1],-1)==-1:
            alldict[d1[1]] = [(d1[2],d1[3],d1[0])]
        else:
            alldict[d1[1]].append((d1[2],d1[3],d1[0]))
    return alldict

def getstudents(driver,datetoclass):
    classtostud = {}
    #p is parentwindow
    p = driver.current_window_handle
    classidlist = []
    for row in datetoclass.values():
        classidlist.extend(row)
    for clas in classidlist:
        #print("Parent window title: " + driver.title)
        wsmid = clas[2]
        #print(wsmid)
        button = driver.find_element_by_xpath(f"//*[@data-wsm-id={wsmid}]").click()
        #chwd is child window
        chwd = driver.window_handles
        for w in chwd:
            if(w!=p):
                driver.switch_to.window(w)
                break
        select = Select(driver.find_element_by_name('order-listing_length'))
        select.select_by_value('-1')
        ctos = collectfromclass(driver,clas)
        for k,v in ctos.items():
            classtostud[k] = v
        driver.switch_to.window(p)
        #print("Child window title: " + driver.title)
    dprint(classtostud)
    return classtostud

def refine(filename):
    subjdict = {'math':'Maths','phy':'Physics','chem':'Chemistry','bio':'Biology',
                'math hl aa':'Math-HL-Analysis','math sl aa':'Math-SL-Analysis',
                'math hl ai':'Math-HL-Application','math sl ai':'Math-SL-Application',
                'bio hl':'BIO-HL','bio sl':'BIO-SL','chem hl':'CHEMISTRY-HL',
                'chem sl':'CHEMISTRY-SL','phy hl':'PHYSICS-HL','phy sl':'PHYSICS-SL'}
    #NO ENGLISH, ECONOMICS, SCIENCE
    parts = filename.split(' ',maxsplit=1)
    batch,subject = parts[0],parts[1]
    if batch[:2].upper() in ('CB','CL'):
        if 'j' not in batch:
            if int(batch[2])<7:
                batch = batch[:2].upper()+'-'+batch[2:4]+'-'+batch[4:].upper()
            else:
                batch = batch[:2].upper()+'-'+batch[2]+'-'+batch[3:].upper()
        else:
            if int(batch[2])<7:
                batch = batch[:2].upper()+'-'+batch[2:4]+'-'+batch[4].upper() + '-' + batch[5:].upper()
            else:
                batch = batch[:2].upper()+'-'+batch[2]+'-'+batch[3].upper() + '-' + batch[4:].upper()
    elif batch[:2].upper()=='IB':
        if 'j' not in batch:
            batch = batch[:2].upper()+ '-' +batch[2].upper() + batch[3]+'-'+batch[4:].upper()
        else:
            batch = batch[:2].upper()+ '-' +batch[2].upper() + batch[3]+'-'+batch[4].upper()+'-'+ batch[5:].upper()
    elif batch[:2].upper()=='IG':
        if 'j' not in batch:
            if int(batch[2])<7:
                batch = batch[:2].upper()+'-'+batch[2:4] + batch[4].upper()+ '-'+batch[5:].upper()
            elif int(batch[2])==8:
                batch = batch[:2].upper()+'-'+batch[2] +'-'+batch[3:].upper()
            else:
                batch = batch[:2].upper()+'-'+batch[2] + batch[3].upper()+ '-'+batch[4:].upper()
        else:
            if int(batch[2])<7:
                batch = batch[:2].upper()+'-'+batch[2:4] + '-' +  batch[4].upper()+ '-' + batch[5].upper() + '-' + batch[6:].upper()
            elif int(batch[2])==8:
                batch = batch[:2].upper()+'-'+batch[2] +'-'+ batch[3].upper() + '-' + batch[4:].upper()
            else:
                batch = batch[:2].upper()+'-'+batch[2:4].upper()+ '-' + batch[4].upper() + '-' +batch[5:].upper()
    subject = subjdict[subject]
    return (batch,subject)


def linkfinder(clsuid,links):
    for link in links:
        name = os.path.basename(link)
        name = name.rstrip('.txt')
        #print(name)
        batchsubtup = refine(name)
        #print(batchsubtup)
        if batchsubtup[0]==clsuid[0] and batchsubtup[1]==clsuid[1]:
            return link

def docreader(link):
    #Can add more
    upldic = {'comp':'Completed','pc':'Partially Completed','ns':'Not Submitted','fl':'Few Left',
              'incomp':'Incomplete','alc':'Absent Last Class','abs':'Absent Present Class','-':'Select Status'}
    handle = open(link,'r')
    compones = []
    doc = []
    for line in handle:
        doc.append(line.rstrip('\n'))
    doc = list(filter(lambda x:x!='',doc))
    #pprint(f'link {link} and doc {doc}')
    flag = -1
    for i in range(0,len(doc)-1,2):
        if flag==1:
            flag = -1
            continue
        names = doc[i].split(',')
        names = list(filter(lambda x:x!=' ' and x!='',names))
        if doc[i+1] in upldic:
            for name in names:
                finalname = name.rstrip(',').lstrip(',')
                finalname = finalname.rstrip(' ').lstrip(' ')
                compones.append((finalname,upldic[doc[i+1]]))
        elif doc[i+1]=='c:':
            flag = 1
            for name in names:
                finalname = name.rstrip(',').lstrip(',')
                finalname = finalname.rstrip(' ').lstrip(' ')
                compones.append((finalname,upldic[doc[i+3]],doc[i+2]))
    return compones
             
def allvaluesfinder(datetoclass,classtostudents,datetolink,xdcdatetoclass):
    classtoall = {}
    for date in xdcdatetoclass:
        #print(f'date is {date}')
        links = datetolink[date]
        #pprint(f'links are {links}')
        for link in links:
            allnames = docreader(link)
            name = os.path.basename(link)
            name = name.rstrip('.txt')
            batchsubtup = refine(name)
            allnames = docreader(link)
            try:
                classsubjids = datetoclass[date]
                clsuid = list(filter(lambda x:x[0]==batchsubtup[0] and x[1]==batchsubtup[1],classsubjids))[0]
                #print(f'clsuid is {clsuid}')
                classtoall[clsuid] = allnames
                #print(f'Reached here')
            except:
                classtoall[batchsubtup+('Already Uploaded',)] = allnames
    #print(f'size is {len(classtoall)}')
    return classtoall
    
def xdocdatetoc(datetolink):
    pdict = {}
    for date in datetolink:
        links = datetolink[date]
        for link in links:
            name = os.path.basename(link)
            name = os.path.basename(link)
            name = name.rstrip('.txt')
            batchsubtup = refine(name)
            if date not in pdict:
                pdict[date] = [batchsubtup]
            else:
                pdict[date].append(batchsubtup)
    return pdict
            
def writetoexcel(foldername,datetolink,datetoclass,classtoall,xdcdatetoclass):
    fname = f'{foldername}.csv'
    if os.path.exists(fname):
        os.remove(fname)
    from xlwt import Workbook
    #color-index red
    style1 = xlwt.easyxf('font: name Times New Roman, color blue, bold on')
    wb = Workbook()
    for date in xdcdatetoclass:
        classes = xdcdatetoclass[date]
        ws = wb.add_sheet(date)
        i,j = 3,3
        while True:
            for clas in classes:
                pass


    #wb.save()

def work(folders,pname):
    driver = login()
    hoveroverws(driver)
    driver.implicitly_wait(20)
    link = driver.find_element_by_link_text('Upload Corrected Worksheet')
    link.click()
    select = Select(driver.find_element_by_name('order-listing_length'))
    select.select_by_value('-1')
    dtc = collectfromup(driver)
    datetolink = getclasses(folders,pname)
    dprint(datetolink)
    datetoclass = {}
    for (key,value) in dtc.items():
        #pprint(f'here {key} and {value}')
        if key in datetolink.keys():
            datetoclass[key] = value
        #pprint(f' here {datetoclass}')
    dprint(f'date to class dictionary {datetoclass}')
    #NOTE: HERE DRIVER IS AT UPLOAD WORKSHEET INDEX
    classtostudents = getstudents(driver,datetoclass)
    dprint(classtostudents)
    #x = str(input("\nPress Enter to continue..."))
    xdcdatetoclass = xdocdatetoc(datetolink)
    dprint(f'excel date to class')
    dprint(xdcdatetoclass)
    classtoall = allvaluesfinder(datetoclass,classtostudents,datetolink,xdcdatetoclass)
    dprint(f'class to all dictionary')
    dprint(classtoall)
    #UPTO HERE ALL DICTIONARIES COLLECTED, NOW TIME TO UPLOAD
    foldername = os.path.basename(pname)
    #writetoexcel(foldername,datetolink,datetoclass,classtoall,xdcdatetoclass)
    driver.quit()
    return((datetoclass,classtostudents,datetolink,classtoall))
    #upload(datetoclass,classtostudents,datetolink,classtoall)


#work()
#login()
#hoveroverws()


#FINAL ID, 3 - student class,11 is date,5 - SUBJECT, 7 -ws, 9 - Corrected/Correction Pending, 7 - ws avail/unavail
#in d1 0 - FinalID, 1 - Date, 2 - studclass,3 - subject

        

