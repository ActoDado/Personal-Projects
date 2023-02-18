from Prepping_Dicts import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from random import uniform
from PlaySong import playbgm


username = "enter here"
password = "enter here"
link = "https://topperseducation.sg/index.php"

#logging in

#uploading correction inside

#FINDING BY XPATH
#RIGHT CLICK, INSPECT, COPY, COPY XPATH,
#THEN USE FIND ELEMENT BY XPATH. EASY


#DEFAULT GLOBAL SETTINGS
mn,mx = 0.5,2.5
debugmarkall = False
debuglate = True
debugsong = False

path1 = r"C:\Program Files (x86)\TpsFiles"

def randsleep():
    #TO LOOK NATURAL
    val = uniform(mn,mx)
    return val

def settings():
    handle = open(path1 + r"\debugsettings.txt",'r')
    doc = []
    for line in handle:
        doc.append(line.rstrip('\n'))
    for i in range(0,len(doc)-1):
        if 'Rand Value(s):' in doc[i]:
            mn = float(doc[i+1].lstrip('Min:'))
            mx = float(doc[i+2].lstrip('Max:'))
        elif 'Mark All Completed:' in doc[i]:
            val = bool(int(doc[i+1]))
            debugmarkall = val
        elif 'Late Submission:' in doc[i]:
            val = bool(int(doc[i+1]))
            debuglate = val
        elif 'Play Music:' in doc[i]:
            val = bool(int(doc[i+1]))
            debugsong = val
        else:
            pass
    return (mn,mx,debugmarkall,debuglate,debugsong)

try:
    sets = settings()
    mn,mx = sets[0],sets[1]
    debugmarkall,debuglate = sets[2],sets[3]
    debugsong = sets[4]
    
except Exception as e:
    print("WARNING!! Settings TAMPERED...")
    print(f'Error Here:{e}')
    randsleep()
    os.system('cls')

def checkifalldone(driver):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content,'lxml')
    toptable = soup.find("table", attrs={"id": "order-listing"})
    topdata = toptable.tbody.find_all("tr")  
    # Get all the headings of Lists
    pdict = {'id':'Not Done','fi':'Done'}
    alldict = {}
    for elem in topdata:
        i = 0
        s = str(elem.button)
        #print(f's here in elem is {s}')
        x = s.split('data-ws')
        #print(f'x here in elem is {x}')
        try:
            p = x[1][1:3]
        except:
            continue
        FinalState = pdict[p]
        d1 = {0:FinalState}
        for td in elem:
            #print(i,td.text,'\n')
            if i==3:
                d1[2] = td.text
            i+=1
        alldict[d1[2]] = d1[0]
    lst = list(filter(lambda x:x[1] == 'Not Done' ,alldict.items()))
    if lst:
        return False
    else:
        return True

def tostudent(driver,PendingStudents,studentswithcomments,debuglate):
    valuedict = {'Absent Present Class': "2",'Completed':"3",'Partially Completed':"4",
                 'Not Submitted':"8",'Incomplete':"6",'Few Left':"5",'Absent Last Class':"1",'Select Status':"0"}
    def redones(student):
        try:
            #HERE CHECKS IF STUD UPLOADED A FILE(KEY ERROR), IF HE DID, HE IS NOT A RED ONE
            if student[4]=='Worksheet Uploaded':
                return
            val = valuedict[student[1]]
        except:
            return
            #IF STUD UPLOADED SKIPS
        #print(f'student here is {student}')
        xpath = f'//*[@id="order-listing"]/tbody/tr[{student[2]}]/td[6]/button'
        #button = driver.find_element_by_xpath(xpath)
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,xpath)))
        actions = ActionChains(driver)
        actions.move_to_element(button).click().perform()
        #button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
        #driver.implicitly_wait(20)
        element = driver.switch_to.active_element
        time.sleep(0.2)
        #print(element)
        elem = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'submission-status')))
        select = Select(elem)
        time.sleep(randsleep())
        #driver.implicitly_wait(20)
        if debuglate is True and val!="1":
            #INSTEAD OF NS, SENDS LATE SUBMISSION
            select.select_by_value("3")
            driver.find_element_by_name("worksheet-comment").send_keys("LATE SUBMISSION")
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'submit-upload-file'))).click()
            time.sleep(randsleep())
            #/html/body/div[3]/div/div[4]/div/button
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/div[4]/div/button'))).click()
            return
        #SENDS NS
        select.select_by_value(val)
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'submit-upload-file'))).click()
        time.sleep(randsleep())
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/div[4]/div/button'))).click()
    for student in PendingStudents:
        #print(f'student here in main loop is {student}')
        try:
            #CHECKS TO SEE IF STUDENT EXISTS INSIDE NOTES
            status = list(filter(lambda x:x[0].lower() in student[0].lower(),studentswithcomments))[0]
            student+=status[1:]
            #print(f'full length of students is {len(student)}, and student is {student}')
            xpath = f'//*[@id="order-listing"]/tbody/tr[{student[2]}]/td[6]/button'
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
            #button = driver.find_element_by_xpath(f"//*[@data-ws-id={str(student[1])}]").click()
            val = valuedict[student[5]]
            driver.implicitly_wait(20)
            element = driver.switch_to.active_element
            time.sleep(0.2)
            #print(element)
            elem = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'submission-status')))
            select = Select(elem)
            time.sleep(randsleep())
            select.select_by_value(val)
            if len(student)==7:
                driver.find_element_by_name("worksheet-comment").send_keys(student[6])
            #button = driver.find_element_by_xpath('//*[@id="submit-upload-file"]').click()
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'submit-upload-file'))).click()
            time.sleep(randsleep())
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/div[4]/div/button'))).click()
            #button = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/button').click()
            #driver.implicitly_wait(20)
        except:
            #print(f'{student} is a redone')
            redones(student)
            continue
    return

def markpagecomp(driver,wsmid):
    #button = driver.find_element_by_xpath(f"//*[@data-wsm-id={wsmid}]").click()
    time.sleep(0.2)
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,f"//*[@data-wsm-id={wsmid}]")))
    actions = ActionChains(driver)
    actions.move_to_element(button).click().perform()
    element = driver.switch_to.active_element
    #print(element)
    time.sleep(randsleep())
    #x = str(input('Enter to continue...'))
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="swal-button swal-button--confirm btn btn-primary"]'))).click()
    #button = element.find_element_by_xpath('//*[@class="swal-button swal-button--confirm btn btn-primary"]').click()
    return driver
    

def upload(datetoclass,classtostudents,datetolink,classtoall,debug,debuglate):
    driver = login()
    hoveroverws(driver)
    driver.implicitly_wait(20)
    link = driver.find_element_by_link_text('Upload Corrected Worksheet')
    link.click()
    select = Select(driver.find_element_by_name('order-listing_length'))
    select.select_by_value('-1')
    p = driver.current_window_handle
    for date in datetoclass:
        classubids = datetoclass[date]
        #pprint(classubids)
        for clsuid in classubids:
            #WE OPEN THE CLASS AND THEN WE ADD FOR EACH STUDENT
            wsmid = clsuid[2]
            #print("Parent window title: " + driver.title)
            #print(wsmid)
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,f"//*[@data-wsm-id={wsmid}]"))).click()
            #button = driver.find_element_by_xpath(f"//*[@data-wsm-id={wsmid}]").click()
            #chwd is child window
            chwd = driver.window_handles
            for w in chwd:
                if(w!=p):
                    driver.switch_to.window(w)
                    break
            studentswithIDS = classtostudents[clsuid]
            #pprint(studentswithIDS)
            select = Select(driver.find_element_by_name('order-listing_length'))
            select.select_by_value('-1')
            try:
                studentswithcomments = classtoall[clsuid]
            except:
                studentswithcomments = None
            #TO REMOVE CORRECTED ONES:
            PendingStudents = list(filter(lambda x:x[3]!='Corrected',studentswithIDS))
            tostudent(driver,PendingStudents,studentswithcomments,debuglate)
            time.sleep(randsleep())
            if debug is True:
                if checkifalldone(driver):
                    #print(f'all done {wsmid}')
                    driver = markpagecomp(driver,wsmid)
            time.sleep(0.2)
            driver.switch_to.window(p)
            time.sleep(0.2)

def package(pname):
    folders = getfolders(pname)
    def piece(folders,pname):
        tup = work(folders,pname)
        datetoclass = tup[0]
        classtostudents = tup[1]
        datetolink = tup[2]
        classtoall = tup[3]
        time.sleep(randsleep())
        upload(datetoclass,classtostudents,datetolink,classtoall,debugmarkall,debuglate)
        return
    done = 0
    while True:
        try:
            piece(folders,pname)
            break
        except Exception as e:
            print(e,done)
            done+=1
            pass
        

#package()
#work()


#FINAL ID, 3 - student class,11 is date,5 - SUBJECT, 7 -ws
#in d1 0 - FinalID, 1 - Date, 2 - studclass,3 - subject

        

