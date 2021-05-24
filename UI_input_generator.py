import os
import shutil
import sys
from tkinter import *
from tkinter import filedialog as fd
from generate_input_file import generateTxt
from analog_input_vis import analogVideo
from kb_input_vis import digitalVideo

window = Tk()

window.title("TrackMania Replay Input Viewer")
window.geometry('700x300')

gbxFileName = "No .Gbx file specified"

def run():
    # Run generate_input_file pipe into directory path, 
    baseFileName = os.path.splitext(os.path.basename(gbxFileName))[0]
    os.makedirs("Raw Inputs", exist_ok=True)

    sys.stdout = open(os.path.join('Raw Inputs', baseFileName + '.txt'), "w")
    generateTxt(gbxFileName)
    sys.stdout.close()

    if txtOnlyBool.get() == 0:
        

        if digitalBool.get() == 0:
            analogVideo(os.path.join('Raw Inputs', baseFileName + '.txt'))

        else:
            digitalVideo(os.path.join('Raw Inputs', baseFileName + '.txt'))


    #statusVar.set("Processing Finished!")

def gbxAsk():
    global gbxFileName
    gbxFileName = fd.askopenfilename(title='Select a .Gbx replay file (case sensitive):',filetypes=[("Gbx files", "*.Gbx")])
    gbxVar.set(os.path.basename(gbxFileName))




gbxVar = StringVar()
gbxVar.set("No .Gbx file specified")

gbxFileDisplay = Label(window, textvariable=gbxVar)
gbxFileDisplay.grid(column=0, row=0,padx = 7, pady= (20,0))

gbxFileBtn = Button(window, text="Open .Gbx file", bg="white", fg="black", command=gbxAsk)
gbxFileBtn.grid(column=1, row=0, padx=10, pady= (20,0))

inputTypeLabelVar = StringVar()
inputTypeLabelVar.set("Select input type:")
inputTypeLabel = Label(window, textvariable=inputTypeLabelVar)
inputTypeLabel.grid(column=0, row=1,padx = 7, pady= (20,0), sticky=W)

digitalBool = IntVar()
Radiobutton(window, text="Controller, Wheel, or Joystick", variable = digitalBool,value = 0 ).grid(column=0, row=2,sticky=W)
Radiobutton(window, text="Keyboard", variable = digitalBool, value = 1).grid(column=0, row=3,sticky=W)

txtOnlyBool = IntVar()
Checkbutton(window, text="Generate inputs .txt file only (no video)", onvalue=1, offvalue=0, variable = txtOnlyBool).grid(column=0, row=4,pady= (20,0),sticky=W)

executeBtn = Button(window, text="Process replay (may take a while for video)", bg="white", fg="black", command=run, activebackground='#00ff00')
executeBtn.grid(column=0, row=5, sticky=W, padx = 5, pady =(20,0) )

'''statusVar = StringVar()
statusVar.set("")

statusVarShow = Label(window, textvariable=statusVar)
statusVarShow.grid(column=0, row=6,padx = 7, pady= (20,0), sticky=W)'''

if __name__ == '__main__':
    window.mainloop()