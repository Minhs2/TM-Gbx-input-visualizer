import subprocess
import os

def inputReplayMerge(inputVideo, replayVideo, audioBool, startTrim):
    os.makedirs("Final Videos/", exist_ok=True)
    outputPath = os.path.join('Final Videos', os.path.splitext(os.path.basename(inputVideo))[0]+ '.mp4')
    if audioBool == 1:
        subprocess.call('ffmpeg/ffmpeg.exe -y -ss ' + startTrim + ' -i "'+ replayVideo + '" -i "' + inputVideo + 
                        '" -filter_complex "[1:v]colorkey=0x000000:0.1:0.47[ckout];[0:v][ckout]overlay[out];[0:a]aresample=44100" -map "[out]" "' 
                        + outputPath + '"')
    else:
        subprocess.call('ffmpeg/ffmpeg.exe -y -ss ' + startTrim + ' -i "'+ replayVideo + '" -i "' + inputVideo + 
                        '" -filter_complex "[1:v]colorkey=0x000000:0.1:0.47[ckout];[0:v][ckout]overlay[out]" -map "[out]" "' 
                        + outputPath + '"')