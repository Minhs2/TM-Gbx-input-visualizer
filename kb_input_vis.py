import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

def digitalVideo(inputTxt):

    global accel
    global brake
    global left
    global right

    # Parse txt files into 4 arrays
    accelDat = []
    brakeDat = []
    leftDat = []
    rightDat = []
    maxVal = 0

    # Parse txt files into 4 arrays
    file = open(inputTxt, 'r')
    rawData = file.readlines()

    # Divide each raw data time by 10 for drop extra 0
    # Save to 2d array of value pairs

    for line in rawData:
        last5 = line[-6:]
        dashSplit = line.split('-')

        if(len(dashSplit) == 1):
            dashSplit = line.split()
            spaceSplit = dashSplit
            
        else:
             spaceSplit = dashSplit[1].split()

        if int(spaceSplit[0])/10 > maxVal:
            maxVal = int(spaceSplit[0])/10

        if  last5 == "ss up\n":
            accelDat.append([int(dashSplit[0])/10, int(spaceSplit[0])/10])

        elif last5 == " down\n":    
            brakeDat.append([int(dashSplit[0])/10, int(spaceSplit[0])/10])
        
        elif last5 == " left\n":    
            leftDat.append([int(dashSplit[0])/10, int(spaceSplit[0])/10])

        elif last5 == "right\n":
            rightDat.append([int(dashSplit[0])/10, int(spaceSplit[0])/10])

    file.close()

    # Define Matplotlib figure and axes
    vidCanvas, ax = plt.subplots()

    # Set background (chroma key) color to pink
    vidCanvas.set_facecolor('#000000')

    # Set canvas to 1080p aspect ratio @ 600 dpi export
    vidCanvas.set_size_inches((3.2, 1.8))
    ax.set_xlim(0, 1920)
    ax.set_ylim(0, 1080)

    # Make flush with borders
    vidCanvas.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    # Transparent gray background squares
    accelBG = patches.Rectangle((899, 810), 123, 123, facecolor='#e2e2e2', alpha = 0.588)
    brakeBG = patches.Rectangle((899, 676), 123, 123, facecolor='#e2e2e2', alpha = 0.588)
    leftBG = patches.Rectangle((765, 676), 123, 123, facecolor='#e2e2e2', alpha = 0.588)
    rightBG = patches.Rectangle((1034, 676), 123, 123, facecolor='#e2e2e2', alpha = 0.588)

    ax.add_patch(accelBG)
    ax.add_patch(brakeBG)
    ax.add_patch(leftBG)
    ax.add_patch(rightBG)

    # Active squares
    accel = patches.Rectangle((899, 810), 123, 123, facecolor='#00ff00')
    brake = patches.Rectangle((899, 676), 123, 123, facecolor='#ff0000')
    left = patches.Rectangle((765, 676), 123, 123, facecolor='#ffac30')
    right = patches.Rectangle((1034, 676), 123, 123, facecolor='#ffac30')

    ax.add_patch(accel)
    ax.add_patch(brake)
    ax.add_patch(left)
    ax.add_patch(right)

    accel.set_visible(False)
    brake.set_visible(False)
    left.set_visible(False)
    right.set_visible(False)


    def animate(i):

        # On every frame: remove all patches from plot, then readd the ones that need to be shown

        global accel
        global brake
        global left
        global right
        
        accel.set_visible(False)
        brake.set_visible(False)
        left.set_visible(False)
        right.set_visible(False)

        # Print progress
        # print(((i+1)/maxVal)*100)

        for pair in accelDat:
            if pair[0] <= i <= pair[1]:
                accel.set_visible(True)

        for pair in brakeDat:
            if pair[0] <= i <= pair[1]:
                brake.set_visible(True)

        for pair in leftDat:
            if pair[0] <= i <= pair[1]:
                left.set_visible(True)

        for pair in rightDat:
            if pair[0] <= i <= pair[1]:
                right.set_visible(True)

        return ax.patches

    # Export file to video, set dpi to 600
    anim = animation.FuncAnimation(vidCanvas, animate, blit=True, interval=10, save_count=maxVal)
    plt.axis('off')
    os.makedirs("Inputs Video/", exist_ok=True)

    vidWriter = animation.FFMpegWriter(fps=100)
    anim.save(os.path.join('Inputs Video', os.path.splitext(os.path.basename(inputTxt))[0] + ".mp4"), writer = vidWriter, dpi = 600)