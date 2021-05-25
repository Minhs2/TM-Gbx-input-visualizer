import os
from tkinter import colorchooser
import sys
import threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from generate_input_file import generateTxt
from analog_input_vis import analogVideo
from kb_input_vis import digitalVideo
from video_merger import inputReplayMerge

def run():
    
    global color_hex
    # Run generate_input_file pipe into directory path, 
    baseFileName = os.path.splitext(os.path.basename(gbxFileName))[0]
    os.makedirs("Raw Inputs", exist_ok=True)

    sys.stdout = open(os.path.join('Raw Inputs', baseFileName + '.txt'), "w")
    generateTxt(gbxFileName)
    sys.stdout.close()

    if txtOnlyBool.get() == 0:

        if digitalBool.get() == 0:
            analogVideo(os.path.join('Raw Inputs', baseFileName + '.txt'), color_hex)

        else:
            digitalVideo(os.path.join('Raw Inputs', baseFileName + '.txt'), color_hex)


        if videoMergeBool.get() == 0:
            inputReplayMerge(os.path.join('Inputs Video', baseFileName + '.mp4'), replayFileName)


def gbxAsk():
    global gbxFileName
    gbxFileName = fd.askopenfilename(title='Select a .Gbx replay file (case sensitive):',filetypes=[("Gbx files", "*.Gbx")])
    gbxVar.set(os.path.basename(gbxFileName))

def replayAsk():
    global replayFileName
    replayFileName = fd.askopenfilename(title='Select a video replay file:')
    replayVar.set(os.path.basename(replayFileName))

def bg_color():
    global color_hex   

    # Store selected color
    color_hex = colorchooser.askcolor(title ="Choose background color")[1]

    if color_hex == None:
        color_hex = '#000000'
    
    colorDisplayCanv.itemconfig(colorDisplay, fill=color_hex)


window = Tk()

window.title("TrackMania Replay Input Viewer")
window.geometry('700x400')

gbxFileName = "No .Gbx file specified"

color_hex = '#000000'

gbxVar = StringVar()
gbxVar.set("No .Gbx file specified")

gbxFileDisplay = Label(window, textvariable=gbxVar)
gbxFileDisplay.grid(column=0, row=0,padx = 7, pady= (20,0))

gbxFileBtn = Button(window, text="Open .Gbx file", bg="white", fg="black", command=gbxAsk)
gbxFileBtn.grid(column=1, row=0, padx=10, pady= (20,0))

replayFileName = "No video file specified"

replayVar = StringVar()
replayVar.set("No video file specified")

replayVideoDisplay = Label(window, textvariable=replayVar)
replayVideoDisplay.grid(column=0, row=1,padx = 7, pady= (20,0))

replayVideoBtn = Button(window, text="Open video file", bg="white", fg="black", command=replayAsk)
replayVideoBtn.grid(column=1, row=1, padx=10, pady= (20,0))

inputTypeLabelVar = StringVar()
inputTypeLabelVar.set("Select input type:")
inputTypeLabel = Label(window, textvariable=inputTypeLabelVar)
inputTypeLabel.grid(column=0, row=3,padx = 7, pady= (20,0), sticky=W)

digitalBool = IntVar()
Radiobutton(window, text="Controller, Wheel, or Joystick", variable = digitalBool,value = 0 ).grid(column=0, row=4,sticky=W)
Radiobutton(window, text="Keyboard", variable = digitalBool, value = 1).grid(column=0, row=5,sticky=W)

txtOnlyBool = IntVar()
Checkbutton(window, text="Generate inputs .txt file only (no video)", onvalue=1, offvalue=0, variable = txtOnlyBool).grid(column=0, row=6,pady= (10,0),sticky=W)

videoMergeBool = IntVar()
Checkbutton(window, text="Merge input visualization onto video file (background must be black)", onvalue=0, offvalue=1, variable = videoMergeBool).grid(column=0, row=7,pady= (5,0),sticky=W)

bGColorBtn = Button(window, text = "Select video background color", command = bg_color)
bGColorBtn.grid(column=0, row=8, padx = 10, sticky=E+W)

colorDisplayCanv = Canvas(window, width = 26, height = 26)
colorDisplayCanv.grid(column=1, row=8, pady=10,sticky=W)
colorDisplay = colorDisplayCanv.create_rectangle(0, 0, 26, 26, fill=color_hex)

executeBtn = Button(window, text="Process replay (may take a while for video(s))", bg="white", fg="black", command=run, activebackground='#00ff00')
executeBtn.grid(column=0, row=9, sticky=E+W, padx = 10, pady =(10,0) )

# WiP progressBar code that doesn't work because GUI is unthreaded
'''progressBar = ttk.Progressbar(window ,orient ="horizontal",length = 250, mode ="determinate")
progressBar.grid(column=0, row=6, sticky=W, padx = 5, pady =(10,0) )
progressBar["maximum"] = 100
progressBar["value"] = 0'''

def destroyer():
    window.quit()
    window.destroy()
    sys.exit()

if __name__ == '__main__':

    threading.Thread(window.mainloop())
    window.protocol("WM_DELETE_WINDOW", destroyer)