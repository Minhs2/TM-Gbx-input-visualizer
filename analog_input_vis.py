import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import sys

import numpy as np
from inputs import get_inputs_gbx


def analogVideo(gbxFileName, color_hex, resDpi, scaleFactor, hPos, vPos):
    global accel
    global brake
    global steerR
    global steerL

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

    # Transparent gray background shapes
    # Specifications (scaleFactor = 1): 560 wide, 280 tall, 10 space in between shapes

    CENTER_H = 1920 * hPos
    CENTER_V = 1080 * vPos

    accelBG = patches.Rectangle((CENTER_H - (64 * scaleFactor), CENTER_V + (5 * scaleFactor)), (128 * scaleFactor), (135 * scaleFactor), facecolor='#e2e2e2', alpha = 0.588)
    brakeBG = patches.Rectangle((CENTER_H - (64 * scaleFactor), CENTER_V - (140 * scaleFactor)), (128 * scaleFactor), (135 * scaleFactor), facecolor='#e2e2e2', alpha = 0.588)
    leftBG = patches.Polygon([[CENTER_H - (74 * scaleFactor), CENTER_V + (140 * scaleFactor)],
                            [CENTER_H - (74 * scaleFactor), CENTER_V - (140 * scaleFactor)],
                            [CENTER_H - (280 * scaleFactor), CENTER_V]],
                            closed=True, facecolor='#e2e2e2', alpha = 0.588)
    rightBG = patches.Polygon([[CENTER_H + (74 * scaleFactor), CENTER_V + (140 * scaleFactor)],
                            [CENTER_H + (74 * scaleFactor), CENTER_V - (140 * scaleFactor)],
                            [CENTER_H + (280 * scaleFactor), CENTER_V]],
                            closed=True, facecolor='#e2e2e2', alpha = 0.588)
    ax.add_patch(accelBG)
    ax.add_patch(brakeBG)
    ax.add_patch(leftBG)
    ax.add_patch(rightBG)

    # Active rectangles
    accel = patches.Rectangle((CENTER_H - (64 * scaleFactor), CENTER_V + (5 * scaleFactor)), (128 * scaleFactor), (135 * scaleFactor), facecolor='#00ff00')
    brake = patches.Rectangle((CENTER_H - (64 * scaleFactor), CENTER_V - (140 * scaleFactor)), (128 * scaleFactor), (135 * scaleFactor), facecolor='#ff0000')

    ax.add_patch(accel)
    ax.add_patch(brake)

    accel.set_visible(False)
    brake.set_visible(False)


    def calcPartTriangle(steerVal):
        # Take in steer val and spit out a 4x2 array for the right polygon
        # Steering values range from -65536 to 65536
        MAX_STEER_VAL = 65536
        MIN_STEER_VAL = -65536

        if steerVal == 0:
            return [[0,0]]
        elif steerVal > 0:
            xValue = CENTER_H + (74 * scaleFactor) + (206 * scaleFactor * (steerVal / MAX_STEER_VAL))
            yTop = CENTER_V + (140 * scaleFactor) - (140 * scaleFactor * (steerVal / MAX_STEER_VAL))
            yBottom = CENTER_V - (140 * scaleFactor) + (140 * scaleFactor * (steerVal / MAX_STEER_VAL))
            return[[CENTER_H + (74 * scaleFactor), CENTER_V + (140 * scaleFactor)],
                   [CENTER_H + (74 * scaleFactor), CENTER_V - (140 * scaleFactor)],
                   [xValue, yBottom], [xValue, yTop]]
        else:
            xValue = CENTER_H - (74 * scaleFactor) - (206 * scaleFactor * (steerVal / MIN_STEER_VAL))
            yTop = CENTER_V + (140 * scaleFactor) - (140 * scaleFactor * (steerVal / MIN_STEER_VAL))
            yBottom = CENTER_V - (140 * scaleFactor) + (140 * scaleFactor * (steerVal / MIN_STEER_VAL))
            return[[CENTER_H - (74 * scaleFactor), CENTER_V + (140 * scaleFactor)],
                   [CENTER_H - (74 * scaleFactor), CENTER_V - (140 * scaleFactor)],
                   [xValue, yBottom], [xValue, yTop]]

    steerR = patches.Polygon(calcPartTriangle(inputs["ms_steerR"][0]), closed=True, facecolor='#ffac30')
    steerL = patches.Polygon(calcPartTriangle(inputs["ms_steerL"][0]), closed=True, facecolor='#ffac30')
    ax.add_patch(steerR)
    ax.add_patch(steerL)

    def animate(i):
        '''global progressBar
        from UI_input_generator import progressBar'''
        # On every frame: remove all patches from plot, then readd the ones that need to be shown

        global accel
        global brake
        global steerR
        global steerL


        accel.set_visible(False)
        brake.set_visible(False)

        # Update progress
        # progressBar["value"] = ((i+1)/maxVal)*100

        steerR.remove()
        steerL.remove()
        steerR = patches.Polygon(calcPartTriangle(inputs['ms_steerR'][i]), closed=True, facecolor='#ffac30')
        steerL = patches.Polygon(calcPartTriangle(-inputs['ms_steerL'][i]), closed=True, facecolor='#ffac30')
        ax.add_patch(steerR)
        ax.add_patch(steerL)

        if inputs['ms_accel'][i] > 0:
            accel.set_visible(True)

        if inputs['ms_brake'][i] > 0:
            brake.set_visible(True)

        return ax.patches

    # Export file to video, set dpi to 600 for 1080p
    if os.name == 'nt': # windows
        plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg/ffmpeg.exe'
    elif os.name == 'posix': # linux/mac, assuming ffmpeg is installed and in path
        plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg'
    # else throw error

    anim = animation.FuncAnimation(vidCanvas, animate, blit=True, interval=10, save_count=maxVal)
    plt.axis('off')
    os.makedirs("Inputs Video", exist_ok=True)

    vidWriter = animation.FFMpegWriter(fps=100, bitrate = 100000)

    anim.save(os.path.join('Inputs Video', os.path.splitext(os.path.basename(gbxFileName))[0] + ".mp4"), writer = vidWriter, dpi = resDpi)
