import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from Fromfolder import getname
from mutagen import File
from Uploading_Correction import package
from PlaySong import playbgm,click
from Working import corefn
import sys
import time
import os
import eyed3
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


repeat = None

debugsong = False

font1 = "Courier New"

path1 = r"C:\Program Files (x86)\TpsFiles"

def settings():
    handle = open(path1 + r"\debugsettings.txt",'r')
    doc = []
    for line in handle:
        doc.append(line.rstrip('\n'))
    for i in range(0,len(doc)-1):
        if 'Play Music:' in doc[i]:
            val = bool(int(doc[i+1]))
            debugsong = val
        else:
            pass
    return debugsong
try:
    debugsong = settings()
except Exception as e:
    print("WARNING!! Settings TAMPERED...")
    print(f'\nError Here:{e}')
    randsleep()
    os.system('cls')



class App:
    def __init__(self, root=None):
        self.root = root
        self.frame = tk.Frame(self.root,bg = 'gray21')
        self.frame.pack()
        tk.Label(self.frame, text='\nMAIN MENU\n',font=(font1, 23),bg = 'grey21',fg = 'tan1').pack(padx = 5,pady = 5)

        tk.Button(self.frame, text='UPLOAD CORRECTION',font=(font1, 16),command=self.make_page_upload,bg = 'burlywood1',fg = 'grey21').pack(padx = 5,pady = 5)
        tk.Button(self.frame, text='WEEKLY REPORT',font=(font1, 16),command=self.make_page_report,bg = 'burlywood2',fg = 'grey21').pack(padx = 5,pady = 5)
        tk.Button(self.frame, text='QUIT',font=(font1, 16),command=self.quitapp,fg = 'grey16',bg = 'sienna2').pack(padx = 5,pady = 20)
        
        self.page_report = Page_Report(master=self.root, app=self)
        self.page_upload = Page_Upload(master=self.root, app=self)

    def main_page(self):
        self.frame.pack()

    def make_page_upload(self):
        click()
        self.frame.pack_forget()
        self.page_upload.start_page()
        
    def make_page_report(self):
        click()
        self.frame.pack_forget()
        self.page_report.start_page()

    def quitapp(self):
        click()
        self.root.destroy()


class Page_Report:
    def __init__(self, master=None, app=None):
        global repeat
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master,bg = 'grey21')

        tk.Label(self.frame, text='\nENTER THE FOLDER NAME\n',font=(font1, 16),fg = 'tan1',bg = 'grey21').pack()
    
        fpath = None
        
        def report():
            click()
            global repeat
            inp = inputtxt.get(1.0, "end-1c")
            val = getname(inp)
            if val!=-1:
                repeat = 0
                sendval['state'] = 'disabled'
                back['state'] = 'disabled'
                lbl.config(text = "\nGREAT! FOLDER FOUND!\n",font=(font1, 14),fg='OliveDrab1',bg = 'grey21')
                lbl.update()
                try:
                    corefn(val)
                except Exception as e:
                    print(e)
                    back['state'] = 'active'
                    sendval['state'] = 'active'
                    lbl.config(text = "\nUH OH, WE RAN INTO AN ERROR :( ... TRY IT AGAIN\n",font=("Arial", 16),fg='deep pink')
                else:
                    back['state'] = 'active'
                    sendval['state'] = 'active'
                    lbl.config(text = "\nWEEKLY REPORT GENERATED!\n",font=(font1, 14),fg='SteelBlue1',bg = 'grey21')
            else:
                lbl.config(text = "\nOOPS! COULD NOT FIND FOLDER\n",font=(font1, 14),fg='firebrick1',bg = 'grey21')
                repeat = 1
        
        inputtxt = tk.Text(self.frame,height = 1,width = 10,font=(font1, 16))
        inputtxt.pack()

        lbl = tk.Label(self.frame, text = "",font=(font1, 16),bg = 'grey21')
        lbl.pack()

        sendval = tk.Button(self.frame,text = "CREATE REPORT",font=(font1, 16), command = report,bg = 'burlywood1',fg = 'grey21')
        sendval.pack()

        lbl = tk.Label(self.frame, text = "",font=(font1, 16),bg = 'grey21')
        lbl.pack()

        back = tk.Button(self.frame, text='GO BACK',font=(font1, 16), command=self.go_back,bg = 'burlywood1',fg = 'grey21')
        back.pack()

    def start_page(self):
        self.frame.pack()

    def go_back(self):
        click()
        self.frame.pack_forget()
        self.app.main_page()

class Page_Upload:
    def __init__(self, master=None, app=None):
        global repeat
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master,bg = 'grey21')

        tk.Label(self.frame, text='\nENTER THE FOLDER NAME\n',font=(font1, 16),fg = 'tan1',bg = 'grey21').pack()
    
        fpath = None
        
        def passval():
            click()
            global repeat
            inp = inputtxt.get(1.0, "end-1c")
            val = getname(inp)
            if val!=-1:
                repeat = 0
                sendval['state'] = 'disabled'
                back['state'] = 'disabled'
                lbl.config(text = "\nGREAT! FOLDER FOUND!\n",font=(font1, 14),fg='OliveDrab1',bg = 'grey21')
                lbl.update()
                e = None
                try:
                    package(val)
                except Exception as e:
                    print(e)
                    back['state'] = 'active'
                    sendval['state'] = 'active'
                    lbl.config(text = "\nUH OH, WE RAN INTO AN ERROR :( ... TRY IT AGAIN\n",font=("Arial", 14),fg='deep pink',bg = 'grey21')
                else:
                    back['state'] = 'active'
                    sendval['state'] = 'active'
                    lbl.config(text = f"\nWEEK {inp[1:]} UPLOADING DONE!\n",font=(font1, 14),fg='SteelBlue1',bg = 'grey21')
            else:
                lbl.config(text = "\nOOPS! COULD NOT FIND FOLDER\n",font=(font1, 14),fg='firebrick1',bg = 'grey21')
                repeat = 1
        
        inputtxt = tk.Text(self.frame,height = 1,width = 10,font=(font1, 16))
        inputtxt.pack(padx = 5,pady = 5)

        lbl = tk.Label(self.frame, text = "",font=(font1, 16),bg = 'grey21')
        lbl.pack()

        sendval = tk.Button(self.frame,text = "UPLOAD",font=(font1, 16), command = passval,bg = 'burlywood1',fg = 'grey21')
        sendval.pack()

        lbl = tk.Label(self.frame, text = "",font=(font1, 16),bg = 'grey21')
        lbl.pack()

        back = tk.Button(self.frame, text='GO BACK',font=(font1, 16), command=self.go_back,bg = 'burlywood1',fg = 'grey21')
        back.pack()
        
        

    def start_page(self):
        self.frame.pack()
        
    def go_back(self):
        click()
        self.frame.pack_forget()
        self.app.main_page()

def mainfn():
    def update1(ind):
        #print('over here',ind,len(frames),frames[ind])
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        panel1.config(image=frame)
        root.after(20, update1, ind)
    tup = playbgm(debugsong)
    try:
        img = tup[0]
        title,artist = tup[1],tup[2]
    except:
        pass
    finally:
        root = tk.Tk()
        root.title('Tps V3')
        root.iconbitmap(path1 + r"\Tps V3.ico")
        frameCnt = 160
        frames = []
        for i in range(frameCnt):
            #print(f'gif -index {i}')
            frames.append(ImageTk.PhotoImage(file = path1 + f'\Space Frames\Fr ({i+1}).gif'))
        #check(frames)
        root.geometry('800x600')
        panel1 = tk.Label(root)
        panel1.place(x=0, y=0, relwidth=1, relheight=1)
        #panel1.pack(fill='both')
        #root.configure(bg = 'indian red')
        #root.wm_attributes('-transparentcolor', '#ab23ff')
    if debugsong:
        img = img.resize((250,250),Image.ANTIALIAS)
        imag = ImageTk.PhotoImage(img)
        panel = tk.Label(root, image = imag)
        panel.pack(padx = 5,pady = 10)
        song = tk.Label(root, text = f"{title} - {artist}",font=('Free Mono', 10),fg = 'medium blue')
        song.pack(padx = 5,pady = 5)
        root.after(0, update1, 0)
        #root.geometry('800x700')
    else:
        root.geometry('400x300')
        root.configure(bg = 'indian red')
        root.update()
    app = App(root)
    root.mainloop()
    sys.exit()
    exit()

#mainfn()
    
