#!/usr/bin/env python3

import roslibpy
import time
import math
from motion_lib import MotionLib

try:
  client = roslibpy.Ros(host='localhost', port=9090)
  client.run()
except:
  print("Cannot connect to the robot, check your IP addess and network connection")
  exit()

# Sanity check to see if we are connected
print('Verifying the ROS target is connected?', client.is_connected)


ml = MotionLib(client)

time.sleep(1) 

def AddSpiralPoint(index, radius, angle, centre_x, centre_y, z, blend_linear, blend_angular):
   x = centre_x + (radius*math.sin(angle))
   y = centre_y + (radius*math.cos(angle))
   ml.set_motion_coordinates(index, x, y, z)

   ml.set_motion_orientation(index, 0, 1, 0, -0.0032037) 
   ml.set_max_velocity(index, 0.5, 1.0)
   ml.set_max_joint_velocity_acceleration(index, 1.0, 1.0) 
   ml.set_motion_blend(index, blend_linear, blend_angular)

def moveSpiral(turns, pitch, radius, origin_x, origin_y, origin_z, steps_per_turn, blend_linear = 0.0, blend_angular = 0.0):
    slices = steps_per_turn
    n_goals = turns*slices # Number of goals per revolution
    ml.init_move(n_goals) # Initialise all the goals

    angle = 0
    for index in range(n_goals): # For each revolution, set the circle coords
        
        AddSpiralPoint(index, radius, angle, origin_x, origin_y, origin_z, blend_linear, blend_angular)
        angle = (2*(math.pi/steps_per_turn))+angle
        origin_z = origin_z + (pitch/slices) 



    ml.start_motion(client, 30)
    

try:

  moveSpiral(3, 0.1, 0.15, 0.5, 0.5, 0.2, 12, 0.25, 20.0) # Blend values have been selected arbitrarily
  print("Complete!")

except Exception as e:
    print("Error: Could not complete task-- " + str(e))


# Clean up the connection to the robot
client.terminate()
