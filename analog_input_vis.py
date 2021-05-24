import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

def analogVideo(inputTxt):

    global accel
    global brake
    global steer
    global targetSteer

    # Parse txt files into 4 arrays
    accelDat = []
    brakeDat = []
    steerDat = []
    maxVal = 0

    # Parse txt files into 4 arrays
    file = open(inputTxt, 'r')
    rawData = file.readlines()

    # Divide each raw data time by 10 for drop extra 0
    # Save to 2d array of value pairs

    for line in rawData:

        analogSplit = line.split(' steer ')

        # Analog input processor
        if len(analogSplit) == 2:
            if int(analogSplit[0])/10 > maxVal:
                maxVal = int(analogSplit[0])/10

            steerDat.append([int(analogSplit[0])/10, int(analogSplit[1][:-1])])   

        # Digital input processor
        else:
            last5 = line[-6:]
            dashSplit = line.split('-')
            spaceSplit = dashSplit[1].split()

            if int(spaceSplit[0])/10 > maxVal:
                maxVal = int(spaceSplit[0])/10

            if  last5 == "ss up\n":
                accelDat.append([int(dashSplit[0])/10, int(spaceSplit[0])/10])

            elif last5 == " down\n":    
                brakeDat.append([int(dashSplit[0])/10, int(spaceSplit[0])/10])


    file.close()

    # Append empty array to not run into inded OOB error
    steerDat.append([float('inf'),0])

    # Define Matplotlib figure and axes
    vidCanvas, ax = plt.subplots()

    # Set background (chroma key) color to black
    vidCanvas.set_facecolor('#000000')

    # Set canvas to 1080p aspect ratio @ 600 dpi export
    vidCanvas.set_size_inches((3.2, 1.8))
    ax.set_xlim(0, 1920)
    ax.set_ylim(0, 1080)

    # Make flush with borders
    vidCanvas.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    # Transparent gray background shapes
    accelBG = patches.Rectangle((874, 807), 127, 137, facecolor='#e2e2e2', alpha = 0.588)
    brakeBG = patches.Rectangle((874, 663), 127, 137, facecolor='#e2e2e2', alpha = 0.588)
    leftBG = patches.Polygon([[867, 944], [867, 663], [657, 804]], closed=True, facecolor='#e2e2e2', alpha = 0.588)
    rightBG = patches.Polygon([[1008, 944], [1008, 663], [1218, 804]], closed=True, facecolor='#e2e2e2', alpha = 0.588)

    ax.add_patch(accelBG)
    ax.add_patch(brakeBG)
    ax.add_patch(leftBG)
    ax.add_patch(rightBG)

    # Active rectangles
    accel = patches.Rectangle((874, 807), 127, 137, facecolor='#00ff00')
    brake = patches.Rectangle((874, 663), 127, 137, facecolor='#ff0000')

    ax.add_patch(accel)
    ax.add_patch(brake)

    accel.set_visible(False)
    brake.set_visible(False)


    def calcPartTriangle(steerVal):
        # Take in steer val and spit out a 4x2 array for the right polygon
        # Steering values range from -65536 to 65536
        if steerVal == 0:
            return [[0,0]]
        elif steerVal > 0:
            xValue = 1008 + (210 * (steerVal/65536))
            yTop = 944 - (140 * (steerVal/65536))
            yBottom = 663 + (141 * (steerVal/65536))
            return[[1008, 944], [1008, 663], [xValue,yBottom], [xValue,yTop]]
        else:
            xValue = 867 - (210 * (steerVal/-65536))
            yTop = 944 - (140 * (steerVal/-65536))
            yBottom = 663 + (141 * (steerVal/-65536))
            return[[867, 944], [867, 663], [xValue,yBottom], [xValue,yTop]]
            
    targetSteer = 0
    
    # Check if the player starts by steering 
    if steerDat[targetSteer][0] == 0:
        steer = patches.Polygon(calcPartTriangle(steerDat[targetSteer][1]), closed=True, facecolor='#ffac30')
    else:
        steer = patches.Polygon([[0,0]], closed=True, facecolor='#ffac30')
    ax.add_patch(steer)

    def animate(i):

        # On every frame: remove all patches from plot, then readd the ones that need to be shown

        global accel
        global brake
        global steer
        global targetSteer
        
        accel.set_visible(False)
        brake.set_visible(False)

        # Print progress
        # print(((i+1)/maxVal)*100)



        if steerDat[targetSteer + 1][0] <= i:

            targetSteer = targetSteer + 1
            steer.remove()
            steer = patches.Polygon(calcPartTriangle(steerDat[targetSteer][1]), closed=True, facecolor='#ffac30')
            ax.add_patch(steer)
        
        for pair in accelDat:
            if pair[0] <= i <= pair[1]:
                accel.set_visible(True)

        for pair in brakeDat:
            if pair[0] <= i <= pair[1]:
                brake.set_visible(True)

        return ax.patches

    # Export file to video, set dpi to 600 for 1080p
    anim = animation.FuncAnimation(vidCanvas, animate, blit=True, interval=10, save_count=maxVal)
    plt.axis('off')
    os.makedirs("Inputs Video", exist_ok=True)

    vidWriter = animation.FFMpegWriter(fps=100)

    anim.save(os.path.join('Inputs Video', os.path.splitext(os.path.basename(inputTxt))[0] + ".mp4"), writer = vidWriter, dpi = 600)
