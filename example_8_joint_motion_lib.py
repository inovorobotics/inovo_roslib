#!/usr/bin/env python3

import roslibpy
import time
from motion_lib import MotionLib #MY NEW LIB

try:
  client = roslibpy.Ros(host='192.168.8.74', port=9090) # replace with your robots IP address
  client.run()
except:
  print("Cannot connect to the robot, check your IP addess and network connection")
  exit()

# Sanity check to see if we are connected
print('Verifying the ROS target is connected?', client.is_connected)


ml = MotionLib(client)

time.sleep(1) # 1s for the seq to start

try:


  ml.init_trajectory(6,3) # Number of joints and number of goals

  for x in range(6): # Setting all the joints to the same value 
     ml.set_joint_goal(0, x, 2.0)
     ml.set_joint_goal(1, x, 1.0)
     ml.set_joint_goal(2, x, -1.5)



  ml.set_time_from_start(0, 2)
  ml.set_time_from_start(1, 4)
  ml.set_time_from_start(2, 10)

  ml.start_trajectory(client, 30)

except:
    print("Error: Could not complete task")
time.sleep(0.5) # wait 1/2s 


# Clean up the connection to the robot
client.terminate()
