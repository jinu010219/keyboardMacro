import pyautogui as py
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import time
import keyboard
import string
import pyperclip
import pygetwindow as gw



root = Tk()
root.title("Fine Macro for just everyone")
root.geometry("540x320+280+180")
root.resizable(False,False)

"""
photoStart = PhotoImage(file=".\\images\\start.png")
#photoPause = PhotoImage(file="C:\\Users\\jinuchoi\\Desktop\\finemacro\\images\\pause.png")
photoStop = PhotoImage(file=".\\images\\stop.png")
"""
btnframe_root = Frame(root)
currentframe = Frame(root)
currentlistframe= Frame(currentframe)
btnframe_root2 =Frame(currentframe)
labelframe_bottom = Frame(currentframe)
bottomframe = Frame(labelframe_bottom)

btnframe_root.pack(side=LEFT)
currentframe.pack(side=RIGHT)
btnframe_root2.grid(row=1, column=0)
currentlistframe.grid(row=0, column = 0)
labelframe_bottom.grid(row=2, column = 0)

position = py.position()
global btncdt
btncdt = 1

class Act():
    global xvalue
    global yvalue
    global wait
    
    xvalue = None
    yvalue = None
    def 저장(self):
        global xvalue
        global yvalue
        xvalue,yvalue = py.position()
    def 클릭(self):
        py.leftClick()
    def 드래그(self,xmove,ymove):
        py.moveTo(x=xmove,y=ymove,duration=0.5)
    def 오류(self, dragerror):
        tk.messagebox.showerror("오류가 났습니다" ,f"{dragerror}이(가) 설정되지 않았습니다")
    
    def 시간지연(self,freezetime):
        ft = freezetime
        time.sleep(float(ft))
    def 키보드(self,keyvalue):
        pyperclip.copy(keyvalue)
        py.hotkey("ctrl", "v")
        
    actlist = []
act = Act()

currentlist = Listbox(currentlistframe, width= 40 , height = 10)
pointentry = Entry(bottomframe, width = 10)

def waitTime(freezetime):
        currentlist.insert(END,f"{freezetime}초 대기")
        act.actlist.append([act.시간지연.__name__,None,None,freezetime,None])   
        
def putKey(keyvalue):
        currentlist.insert(END,f"{keyvalue}입력")
        act.actlist.append([act.키보드.__name__,None,None,None,keyvalue])
        print(keyvalue)

def click():
    currentlist.insert(END, act.클릭.__name__)
    act.actlist.append([act.클릭.__name__,None,None,None,None])

def drag():
    if xvalue == None or yvalue == None :
        dragerror = "커서위치"
        act.오류(dragerror)
    else:
        currentlist.insert(END,f"{xvalue},{yvalue} 로 드래그")
        act.actlist.append([act.드래그.__name__,xvalue,yvalue,None,None])
def key():
    keyWindow = tk.Toplevel(root)
    keyWindow.title("FineMacro")
    keyWindow.geometry("300x260+300+200")
    keyWindow.wm_attributes("-topmost", 1)
    keyLabel = Label(keyWindow, text='키보드 입력내용을 설정하세요')
    keyText = Text(keyWindow, width=35, height=10 )
    global btncdt
    btncdt = btncdt * 0
    print(btncdt)
    def setKey():
        keyvalue = keyText.get(1.0,END).rstrip()
        putKey(keyvalue)
        global btncdt
        btncdt = btncdt + 1
        print(btncdt)
        keyWindow.destroy()
    keyConfirm = Button(keyWindow,width=4, height=1 ,text="확인", command=setKey )
    keyLabel.pack(side=TOP , pady=10)
    keyText.pack(side=TOP, pady =5)
    keyConfirm.pack(side=TOP, pady=10)

    #여기까지 진행함
    
def save():
    act.저장()
    pointentry.delete(0,END)
    pointentry.insert(0,{yvalue, xvalue})

def wait():
    waitWindow = tk.Toplevel(root)
    waitWindow.title("FineMacro")
    waitWindow.geometry("200x260+300+200")
    waitWindow.resizable(False,False)
    waitWindow.wm_attributes("-topmost", 1)
    global btncdt
    btncdt = btncdt * 0
    waitframe = Frame(waitWindow)
    waitLable = Label(waitWindow, text='대기시간을 설정하세요')
    waitEntry = Entry(waitframe, width=10)
    choLable = Label(waitframe, text='초')
    def setFreezetime():
        global btncdt
        freezetime = waitEntry.get().strip()
        waitTime(freezetime)
        btncdt = btncdt + 1
        waitWindow.destroy()

    waitConfirm = Button(waitWindow, width=4, height=1 , text="확인", command= setFreezetime)
    waitLable.pack(side=TOP, pady=10)
    waitframe.pack(side=TOP, pady=5)
    waitEntry.pack(side=LEFT , pady=5)
    choLable.pack(side=RIGHT)
    waitConfirm.pack(side=TOP, pady=10)

def delete():
    currentlist.delete(END)
    del act.actlist[-1]
def do(x,xmove,ymove,freezetime,keyvalue):
    if x == "클릭": 
        act.클릭()
    if x == "드래그":
        act.드래그(xmove,ymove)
    if x =="시간지연":
        act.시간지연(freezetime)
    if x =="키보드":
        act.키보드(keyvalue)

def startact():
    global breakint
    breakint = 0
    for [x,xmove,ymove,freezetime,keyvalue] in act.actlist:
        do(x,xmove,ymove,freezetime,keyvalue)
        if breakint == 10:
            break
def pauseact():
    global breakint
    breakint = 5
def stopact():
    global breakint
    breakint = 10


btnClick = Button(btnframe_root, width = 18 , height = 1 , text="마우스 클릭:ctrl", command=click )
btnDrag = Button(btnframe_root, width = 18 , height = 1 , text= "저장위치로 이동:alt" , command = drag)
btnKey = Button(btnframe_root, width = 18 , height = 1 , text= "키보드 입력" , command = key)
btnSave = Button(btnframe_root, width = 18 , height = 1 , text="커서위치 저장:CapsLock" , command = save)
btnWait = Button(btnframe_root, width = 18 , height = 1 , text="대기시간 설정" , command = wait)
btnDelete = Button(btnframe_root, width =18,  height = 1 , text="삭제(UNDO)" , command = delete)

btnStart = Button(btnframe_root2, width = 8 , height = 2 ,text="시작", command=startact)
#btnPause = Button(btnframe_root2, width = 50 , height = 50, image=photoPause , command=pauseact)
btnStop = Button(btnframe_root2, width = 8 , height = 2, text="정지", command=stopact )

def gethelp():
    helpWindow = tk.Toplevel(root)
    helpWindow.geometry("300x260+300+200")
    helpLable = Label(helpWindow, text='CJW의 첫 파이썬 작품 \n \n <기타 단축키> \n 우측방향키: 매크로 시작 \n 좌측방향키: 매크로 정지\n <패치예고> \n  -드래그속도 설정추가\n 작동시간 측정기능 추가\n 일시정지기능 추가 \n -UI,기타버그 개선')
    helpLable.pack(side=TOP)


btnhelp = Button(width=12, height=1,text="도움말/패치노트", command=gethelp)
btnhelp.place(x=0,y=0)


sbcurrent = Scrollbar(currentlistframe, orient=VERTICAL)

labelBottom = Label(bottomframe, text='커서위치 :')
labelMaker = Label(labelframe_bottom, text='made by CJW 2021 // for ge sung')
sbcurrent.config(command=currentlist.yview)
currentlist.config(yscrollcommand=sbcurrent.set)

btnClick.grid(row=0, column = 0 , pady= 5)
btnDrag.grid(row=1, column = 0 , pady= 5)
btnSave.grid(row=2, column = 0 , padx =30 , pady= 5)
btnKey.grid(row=3, column = 0 , pady=5)
btnWait.grid(row=4, column = 0, pady=5)
btnDelete.grid(row=5, column = 0 , padx =30 , pady= 5)
btnStop.pack(side=RIGHT,padx =10 , pady= 10)
btnStart.pack(side=RIGHT,padx =10 , pady= 10)
#btnPause.pack(side=RIGHT,padx =10 , pady= 10)
currentlist.pack(side=LEFT)
sbcurrent.pack(side=RIGHT, fill=Y)
bottomframe.grid(row=0, column=0)
labelBottom.pack(side=LEFT)
pointentry.pack(side=LEFT)
labelMaker.grid(row=1, column=0)




def dosave(self):
    save()
def dodrag(self):
    drag()
def doclick(self):
    click()
def doStart(self):
    startact()
def doStop(self):
    stopact()

def fastkey():
    keyboard.on_press_key("Caps_Lock", dosave)
    keyboard.on_press_key("alt", dosave)
    keyboard.on_press_key("alt", dodrag)
    keyboard.on_press_key("ctrl", dosave)
    keyboard.on_press_key("ctrl", doclick)
    keyboard.on_press_key("Right", doStart)
    keyboard.on_press_key("Left", doStop)
fastkey()



root.mainloop()
