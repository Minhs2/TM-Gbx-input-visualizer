import subprocess
import os

def inputReplayMerge(inputVideo, replayVideo):
    os.makedirs("Final Videos/", exist_ok=True)
    outputPath = os.path.join('Final Videos', os.path.splitext(os.path.basename(inputVideo))[0]+ '.mp4')
    subprocess.call('ffmpeg/ffmpeg.exe -y -i "'+ replayVideo + '" -i "' + inputVideo + 
                    '" -filter_complex "[1:v]colorkey=0x000000:0.1:0.47[ckout];[0:v][ckout]overlay[out]" -map "[out]" "' 
                    + outputPath + '"')