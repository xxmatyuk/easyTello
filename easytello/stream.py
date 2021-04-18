import os
import subprocess
import cv2
import numpy as np

FFMPEG_BIN = '/usr/local/bin/ffmpeg'

def run_ffmpeg(tello_ip):
    ffmpg_cmd = [
        FFMPEG_BIN,
        '-i', 'udp://{}:11111'.format(tello_ip),
        '-f', 'image2pipe',
        '-codec:v', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', '640x480',
        '-b:v', '800k',
        '-r', '20',
        '-bf', '0',
        '-',                        # output to go to stdout
    ]
    return subprocess.Popen(ffmpg_cmd, stdout = subprocess.PIPE, bufsize=10**8)

def run_stream(process):
    while True:
        # read frame-by-frame
        raw_image = process.stdout.read(640*480*3)
        if raw_image == b'':
            raise RuntimeError("Empty pipe")
        
        # transform the bytes read into a numpy array
        frame =  np.frombuffer(raw_image, dtype='uint8')
        frame = frame.reshape((480,640,3)) # height, width, channels
        if frame is not None:
            cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        process.stdout.flush()
    
    cv2.destroyAllWindows()
    process.terminate()
    print(process.poll())
    return process

def stop_stream(process):
    cv2.destroyAllWindows()
    process.terminate()


def start_stream(tello_ip):
    ffmpeg_process = run_ffmpeg(tello_ip)
    run_stream(ffmpeg_process)
