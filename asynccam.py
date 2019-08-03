from picamera import PiCamera
from time import sleep
import threading
import asyncio
import aioboto3
import boto3

import os.path
import subprocess
#as3 = async aioboto3.client('s3')

def uploadThread( client, target, name, bucket):
 print("Beginning upload of " + target)
 client.upload_file(name, bucket, target)
 print("Upload of " + name + " comeplete.")

def main(camera, buffersize, s3, bucket):
 x = 1
 y = 0
 name='/home/pi/streams/'+str(0)
 print("Recording" + name)
 lastname=name
 camera.start_recording(name + '.h264')
 sleep(1)
 camera.stop_recording()
 print("Recording " + name +  " complete.")

 while True:
  name='/home/pi/streams/'+str(x)
  print("Recording " + name )
  print("Converting" + lastname)
#  camera.start_preview()
  camera.start_recording(name + '.h264')
  subprocess.Popen("MP4Box -quiet -add " + lastname + ".h264 " + lastname +".mp4", shell=True)
  sleep(1)
  camera.stop_recording()
  print("Recording complete.")
# camera.stop_preview()
  threading.Thread(target=uploadThread, args=(s3,lastname[-1:]+".mp4", lastname+".mp4", bucket)).start()
#    s3.upload_file(lastname + '.mp4', bucket, str(y) + '.mp4')
  y = x
  x=(x+1) % buffersize
  lastname = name

print("Starting")
s3 = boto3.client('s3')
bucket = 'vystastreams'
camera = PiCamera()
camera.resolution = (480,320)
camera.vflip = True
main(camera, 6, s3, bucket)
