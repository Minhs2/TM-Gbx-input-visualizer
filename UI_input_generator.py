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
    #os.makedirs("Raw Inputs", exist_ok=True)

    #sys.stdout = open(os.path.join('Raw Inputs', baseFileName + '.txt'), "w")
    #generateTxt(gbxFileName)
    #sys.stdout.close()

    if txtOnlyBool.get() == 0:

        resDpi = int(dpi_dict[resolutionVar.get()])

        if digitalBool.get() == 0:
            analogVideo(gbxFileName, color_hex, resDpi, float(visScaleVar.get()), hPosSlider.get(), vPosSlider.get())

        else:
            digitalVideo(gbxFileName, color_hex, resDpi, float(visScaleVar.get()), hPosSlider.get(), vPosSlider.get())


        if videoMergeBool.get() == 0:
            inputReplayMerge(os.path.join('Inputs Video', baseFileName + '.mp4'), replayFileName, audioBool.get(), starTrimVar.get())


def gbxAsk():
    global gbxFileName
    gbxFileName = fd.askopenfilename(title='Select a .Gbx replay file (case sensitive):',filetypes=[("Gbx files", "*.Gbx")])
    if gbxFileName == "":
        gbxFileName = "No .Gbx file specified"
    else:
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

def processEnder():
    window.quit()
    window.destroy()
    sys.exit()


window = Tk()
window.protocol("WM_DELETE_WINDOW", processEnder)

window.title("TrackMania Replay Input Viewer")
window.geometry('700x450')

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

starTrimLabelVar = StringVar()
starTrimLabelVar.set("Start trim (seconds):")
starTrimLabel = Label(window, textvariable=starTrimLabelVar)
starTrimLabel.grid(column=0, row=3,padx = 7, pady= (10,0), sticky=W)

starTrimVar = StringVar()
starTrimVar.set("0.000")
startTrimEntry = Entry(window, textvariable = starTrimVar)
startTrimEntry.grid(column=0, row=3,padx = 120, pady= (10,0), sticky=W)

inputTypeLabelVar = StringVar()
inputTypeLabelVar.set("Select input type:")
inputTypeLabel = Label(window, textvariable=inputTypeLabelVar)
inputTypeLabel.grid(column=0, row=4,padx = 7, pady= (20,0), sticky=W)

digitalBool = IntVar()
Radiobutton(window, text="Controller, Wheel, or Joystick", variable = digitalBool,value = 0 ).grid(column=0, row=5,sticky=W)
Radiobutton(window, text="Keyboard", variable = digitalBool, value = 1).grid(column=0, row=6,sticky=W)

txtOnlyBool = IntVar()
Checkbutton(window, text="Generate inputs .txt file only (no video)", onvalue=1, offvalue=0, variable = txtOnlyBool).grid(column=0, row=7,pady= (10,0),sticky=W)

vPosSlider = Scale(window, from_=1, to=0, resolution = 0.05, label="Visualizer center position")
vPosSlider.set(0.75)
vPosSlider.grid(column=1, row=9,sticky=N+S, rowspan=4, padx=(10,0))

hPosSlider = Scale(window, from_=0, to=1, resolution = 0.05, orient=HORIZONTAL, length = 200)
hPosSlider.set(0.5)
hPosSlider.grid(column=1, row=12,padx = (75,0), columnspan = 2, sticky=W+E)



videoMergeBool = IntVar()
Checkbutton(window, text="Merge input visualization onto video file (background must be black)", onvalue=0, offvalue=1, variable = videoMergeBool).grid(column=0, row=8,sticky=W)


audioBool = IntVar()
Checkbutton(window, text="Input video has audio", onvalue=1, offvalue=0, variable = audioBool).grid(column=0, row=9,sticky=W)

bGColorBtn = Button(window, text = "Select video background color", command = bg_color)
bGColorBtn.grid(column=0, row=10, padx = 10, sticky=E+W)

colorDisplayCanv = Canvas(window, width = 26, height = 26)
colorDisplayCanv.grid(column=1, row=10, pady=5,sticky=W)
colorDisplay = colorDisplayCanv.create_rectangle(0, 0, 26, 26, fill=color_hex)

visScaleLabelVar = StringVar()
visScaleLabelVar.set("Visualizer size scale:")
visScaleLabel = Label(window, textvariable=visScaleLabelVar)
visScaleLabel.grid(column=0, row=11,padx = 7, pady= 5, sticky=W)

visScaleVar = StringVar()
visScaleVar.set("1.00")
visScaleEntry = Entry(window, textvariable = visScaleVar)
visScaleEntry.grid(column=0, row=11,padx = 120, pady= 5, sticky=W)

vidResolutionVar = StringVar()
vidResolutionVar.set("Video resolution:")
vidResolutionLabel = Label(window, textvariable=vidResolutionVar)
vidResolutionLabel.grid(column=0, row=12,padx = 7, pady= 5, sticky=W)

resolutions = [
"360p",
"480p",
"720p",
"1080p",
"1440p",
"2160p (4k)",
"4320p (8k)"
]

dpi_dict = {
"360p":"200",
"480p":"267",
"720p":"400",
"1080p":"600",
"1440p":"800",
"2160p (4k)":"1200",
"4320p (8k)":"2400"
}

resolutionVar = StringVar(window)
resolutionVar.set(resolutions[3])

resolutionSelector = OptionMenu(window, resolutionVar, *resolutions)
resolutionSelector.grid(column=0, row=12, sticky=W, padx = 105, pady =5 )

executeBtn = Button(window, text="Process replay (may take a while for video(s))", bg="white", fg="black", command=run, activebackground='#00ff00')
executeBtn.grid(column=0, row=13, sticky=E+W, padx = 10, pady =5 )


# WiP progressBar code that doesn't work because GUI is unthreaded
'''progressBar = ttk.Progressbar(window ,orient ="horizontal",length = 250, mode ="determinate")
progressBar.grid(column=0, row=6, sticky=W, padx = 5, pady =(10,0) )
progressBar["maximum"] = 100
progressBar["value"] = 0'''


if __name__ == '__main__':

    threading.Thread(window.mainloop())
