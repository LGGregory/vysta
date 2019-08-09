from picamera import PiCamera
from time import sleep
import threading
#import asyncio
#import aioboto3
import boto3

import os.path
import subprocess
#as3 = async aioboto3.client('s3')

def uploadThread( client, target, name, bucket):
# print("Beginning upload of " + target)
 client.upload_file(name, bucket, target)
# print("Upload of " + name + " comeplete.")

delay=2

def main(camera, buffersize, s3, bucket):
 x = 1
 y = 0
 name='/home/pi/streams/'+str(0)
# print("Recording" + name)
 lastname=name
 camera.start_recording(name + '.h264')
 sleep(delay)
 camera.stop_recording()
# print("Recording " + name +  " complete.")

 while True:
  name='/home/pi/streams/'+str(x)
#  print("Recording " + name )
#  print("Converting" + lastname)
#  camera.start_preview()

  # Start recording
  camera.start_recording(name + '.h264')
  # Send uploading to a thread
  threading.Thread(target=uploadThread, args=(s3,"v1/"+lastname[-1:]+".h264", lastname+".h264", bucket)).start()

 # converting on the pi is too slow = mp4 files are too big
 # subprocess.Popen("MP4Box -quiet -add " + lastname + ".h264 " + lastname +".mp4", shell=True)

  #end recording. thread will continue as needed.
  sleep(2)
  camera.stop_recording()
#  print("Recording complete.")
# camera.stop_preview()
  
#    s3.upload_file(lastname + '.mp4', bucket, str(y) + '.mp4')
  y = x
  x=(x+1) % buffersize
  lastname = name

print("Starting")
s3 = boto3.client('s3', aws_access_key_id='AKIAZ4JB4F4YVFJZWYXF',aws_secret_access_key='AZLT8a37FLdb83Svk2fLYCEGfaz7IhdkXhReOzpFQ')
bucket = 'vystastreams'
camera = PiCamera()
camera.resolution = (560,420)
camera.vflip = True
main(camera, 10, s3, bucket)
