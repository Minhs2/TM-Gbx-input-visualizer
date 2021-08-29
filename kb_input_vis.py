import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

from inputs import get_inputs_gbx


def digitalVideo(gbxFileName, color_hex, resDpi, scaleFactor, hPos, vPos):

    global accel
    global brake
    global left
    global right

    # Get inputs from replay
    inputs = get_inputs_gbx(gbxFileName)
    maxVal = int(inputs['racetime']/10)

    # Define Matplotlib figure and axes
    vidCanvas, ax = plt.subplots()

    # Set background (chroma key) color to color_hex
    vidCanvas.set_facecolor(color_hex)

    # Set canvas to 1080p aspect ratio @ 600 dpi export
    vidCanvas.set_size_inches((3.2, 1.8))
    ax.set_xlim(0, 1920)
    ax.set_ylim(0, 1080)

    # Make flush with borders
    vidCanvas.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    # Transparent gray background squares
    # Specifications (scaleFactor = 1): 422 wide, 278 tall, 10 space in between shapes
    CENTER_H = 1920 * hPos
    CENTER_V = 1080 * vPos

    accelBG = patches.Rectangle((CENTER_H - (67 * scaleFactor), CENTER_V + (5 * scaleFactor)), 134 * scaleFactor, 134 * scaleFactor, facecolor='#e2e2e2', alpha = 0.588)
    brakeBG = patches.Rectangle((CENTER_H - (67 * scaleFactor), CENTER_V - (139 * scaleFactor)), 134 * scaleFactor, 134 * scaleFactor, facecolor='#e2e2e2', alpha = 0.588)
    leftBG = patches.Rectangle((CENTER_H - (211 * scaleFactor), CENTER_V - (139 * scaleFactor)), 134 * scaleFactor, 134 * scaleFactor, facecolor='#e2e2e2', alpha = 0.588)
    rightBG = patches.Rectangle((CENTER_H + (77 * scaleFactor), CENTER_V - (139 * scaleFactor)), 134 * scaleFactor, 134 * scaleFactor, facecolor='#e2e2e2', alpha = 0.588)

    ax.add_patch(accelBG)
    ax.add_patch(brakeBG)
    ax.add_patch(leftBG)
    ax.add_patch(rightBG)

    # Active squares
    accel = patches.Rectangle((CENTER_H - (67 * scaleFactor), CENTER_V + (5 * scaleFactor)), 134 * scaleFactor, 134 * scaleFactor, facecolor='#00ff00')
    brake = patches.Rectangle((CENTER_H - (67 * scaleFactor), CENTER_V - (139 * scaleFactor)), 134 * scaleFactor, 134 * scaleFactor, facecolor='#ff0000')
    left = patches.Rectangle((CENTER_H - (211 * scaleFactor), CENTER_V - (139 * scaleFactor)), 134 * scaleFactor, 134 * scaleFactor, facecolor='#ffac30')
    right = patches.Rectangle((CENTER_H + (77 * scaleFactor), CENTER_V - (139 * scaleFactor)), 134 * scaleFactor, 134 * scaleFactor, facecolor='#ffac30')

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

        if inputs['ms_accel'][i] > 0:
            accel.set_visible(True)

        if inputs['ms_brake'][i] > 0:
            brake.set_visible(True)

        if inputs['ms_steerL'][i] > 0:
            left.set_visible(True)

        if inputs['ms_steerR'][i] > 0:
            right.set_visible(True)

        return ax.patches

    # Export file to video, set dpi to 600
    if os.name == 'nt': # windows
        plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg/ffmpeg.exe'
    elif os.name == 'posix': # linux/mac, assuming ffmpeg is installed and in path
        plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg'
    # else throw error

    anim = animation.FuncAnimation(vidCanvas, animate, blit=True, interval=10, save_count=maxVal)
    plt.axis('off')
    os.makedirs("Inputs Video/", exist_ok=True)

    vidWriter = animation.FFMpegWriter(fps=100, bitrate = 100000)
    anim.save(os.path.join('Inputs Video', os.path.splitext(os.path.basename(gbxFileName))[0] + ".mp4"), writer = vidWriter, dpi = resDpi)
