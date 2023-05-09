#!/usr/bin/env python3

import roslibpy
import time
from sequence_client import SequenceClient


# TODO replace the IP address here with the IP address of your robot
try:
  client = roslibpy.Ros(host='192.168.8.126', port=9090)
  client.run()
except:
  print("can't connect to the robot, check your IP addess and netowrk connection")
  exit()

# Sanity check to see if we are connected
print('Verifying the ROS target is connected?', client.is_connected)

# The sequence client wraps up our sequence-related service calls
sc = SequenceClient(client, "/sequence")

# Run the sequence from the start block

print("press enter to run sequence from start - WARNING the robot will move!")
input()

sc.start()
time.sleep(1) # 1s for the seq to start

while(sc.is_running()):
  try:
    print("n=" + sc.getVar("n"))
  except:
    print("var 'n' was not found, is it in scope?")
  time.sleep(0.5) # wait 1/2s 

print("press enter to run updown function")
input()

sc.call_function("updown")
sc.wait_until_idle()

print("press enter to run leftright function")
input()

sc.call_function("leftright")
sc.wait_until_idle()

# Clean up the connection to the robot
client.terminate()