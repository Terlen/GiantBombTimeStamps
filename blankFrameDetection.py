from ffmpy import FFmpeg
import subprocess
import sys
ff = FFmpeg(
    inputs = {"c:\\users\\aidan\\Videos\\Bombcast\\mc_bc_680_040621_9473_700.mp4":None},
    #global_options = {'-loglevel warning -nostats'},
    outputs = {'':'-vf blackdetect=d=2:pix_th=0.1 -f null pipe:2'}
)
ff.cmd
#'ffmpeg -i c:\\users\\aidan\\Videos\\Bombcast\\mc_bc_680_040621_9473_700.mp4 -r 1 -s 640x360 -f image2 thumbs/test-%d.jpg'
'ffmpeg -loglevel 0 -nostats -i c:\\users\\aidan\\Videos\\Bombcast\\mc_bc_680_040621_9473_700.mp4 -vf blackdetect=d=2:pix_th=0.1 -f null pipe:2'
outtext = ff.run(stderr=subprocess.PIPE)
print("REAL OUTPUT",outtext)