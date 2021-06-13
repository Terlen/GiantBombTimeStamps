from ffmpy import FFmpeg
ff = FFmpeg(
    inputs = {"c:\\users\\aidan\\Videos\\Bombcast\\mc_bc_680_040621_9473_700.mp4":None},
    #global_options = {'y','r','1','s','640x360'},
    outputs = {'thumbs/%05d.jpg':'-vf fps=0.2'}
)
ff.cmd
#'ffmpeg -i c:\\users\\aidan\\Videos\\Bombcast\\mc_bc_680_040621_9473_700.mp4 -r 1 -s 640x360 -f image2 thumbs/test-%d.jpg'
'ffmpeg -i c:\\users\\aidan\\Videos\\Bombcast\\mc_bc_680_040621_9473_700.mp4 -vf fps=0.2 thumbs/test-%05d.jpg'
ff.run()
