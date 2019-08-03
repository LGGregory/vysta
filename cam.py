from picamera import PiCamera
from time import sleep
import boto3
import os.path
import subprocess
s3 = boto3.client('s3')
bucket = 'vystastreams'
camera = PiCamera()
camera.resolution = (480,320)
x = 0
camerafile = x
#streamerid='vystastreamer1/'
buffering=""




while True:


    name='/home/pi/streams/'+str(x)
    print("Recording " + name )
#   camera.start_preview()
    camera.start_recording(name + '.h264')
    sleep(1)
    camera.stop_recording()
    print("Recording complete.")
#   camera.stop_preview()

    subprocess.Popen("MP4Box -add " + name + ".h264 " + name +".mp4", shell=True)

    sleep(1)
    print("Uploading " + str(x) + ".mp4")
    s3.upload_file(name + '.mp4', bucket, str(x) + '.mp4')
    print("Upload complete.")
    x=(x+1) % 6
