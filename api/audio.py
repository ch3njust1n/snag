import os
import subprocess

'''
inputs:
src (str) Source of mp4 file
dst (str) Destination to save audio file to including filename
'''
def mp4_to_wav(src, dst):
	filename = src.split('/')[-1].split('.')[0]
	dst = f'{dst}/{filename}.mp4'
	
	if os.path.isfile(dst): os.remove(dst)

	command = f'ffmpeg -i {src} -ab 160k -ac 2 -ar 44100 -vn {dst}'
	subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)