from tkinter import *
import os
import sys
import traceback
IDLEContrasts = [["white","black"],["black","white"],["purple","yellow"],["yellow","purple"],["green","lime"],["lime","green"],["lime","white"],["green","white"]]
running = False
window = None
codebox = None
parser = None
outputbox = None
debug_blank = "\n\n\n\n\n\n\n\n\n\n\n"
contrast = 0
try:
    from resources.language.Janky import *
    window = Tk()
    window.config(bg="white")
    window.title("Janky v1.0.0 IDLE (v1.0)")
    window.resizable(width=True,height=True)
    window.geometry("950x995")
    window.minsize(950,995)
    running = True
    outputbox = Label(window,anchor="nw",justify="left",padx=5,height=50,width=60,text="",relief="solid",borderwidth=2,bg="white")
except Exception as err:
    window = Tk()
    window.config(bg="white")
    window.title("Janky IDLE (v1.0): Error")
    window.geometry("795x185")
    window.resizable(width=False,height=False)
    errmsg = Label(window,bg="white",text=f"There was an error trying to start Janky (1.0.0) IDLE (v1.0)\n\tError: {err}\n\tFile: {traceback.format_exc()}")
    errmsg.place(x=10,y=10)
    window.mainloop()
def changeContrastUp(event):
    global contrast
    contrast += 1
    if contrast > len(IDLEContrasts) - 1:
        contrast = 0
    t = outputbox["text"]
    outputbox["text"] = ""
    outputbox["bg"] = IDLEContrasts[contrast][0]
    outputbox["fg"] = IDLEContrasts[contrast][1]
    outputbox["text"] = t
def changeContrastDown(event):
    global contrast
    contrast -= 1
    if contrast < 0:
        contrast = len(IDLEContrasts) - 1
    t = outputbox["text"]
    outputbox["text"] = ""
    outputbox["bg"] = IDLEContrasts[contrast][0]
    outputbox["fg"] = IDLEContrasts[contrast][1]
    outputbox["text"] = t
def updateContrast():
    outputbox["bg"] = IDLEContrasts[contrast][0]
    outputbox["fg"] = IDLEContrasts[contrast][1]
def handle(packets):
    for packet in packets:
        updateContrast()
        command = packet["command"]
        values = packet["values"]
        code = packet["code"]
        errors = packet["errors"]
        for err in errors:
            outputbox["fg"] = "red"
            outputbox["text"] += err + "\n"
        if len(errors) > 0:
            break
        if command == "print":
            strRep = ""
            for v in values:
                strRep += str(v)
            outputbox["text"] += strRep
        elif command == "println":
            strRep = ""
            for v in values:
                strRep += str(v)
            outputbox["text"] += strRep + "\n"
        elif command == "clear":
            outputbox["text"] = ""
        elif command == "printforeach":
            strRep = ""
            for v in values:
                strRep += str(v) + "\n"
            outputbox["text"] += strRep
if running:
    codebox = Text(window,height=50,width=60,borderwidth=2,relief="solid")
    codebox.place(x=10,y=10)
    outputbox.bind("<Button-1>",changeContrastUp)
    outputbox.bind("<Button-3>",changeContrastDown)
    def doHandling():
        updateContrast()
        outputbox["text"] = ""
        outputbox["fg"] = outputbox["bg"] = IDLEContrasts[contrast][1]
        handle(JankyParser().parse(codebox.get("1.0",END)))
    run = Button(window,text="Run",bg="lightgray",width=10,command=doHandling)
    run.place(x=510,y=10)
    outputbox.place(x=510,y=60)
    Label(window,bg="white",height=1,text="Output: ",borderwidth=0).place(x=510,y=40)
    window.mainloop()
