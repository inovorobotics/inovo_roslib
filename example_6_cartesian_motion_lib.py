#!/usr/bin/env python3

import roslibpy
import time


from motion_lib import MotionLib

try:
  client = roslibpy.Ros(host='192.168.8.74', port=9090)
  client.run()
except:
  print("can't connect to the robot, check your IP addess and netowrk connection")
  exit()

# Sanity check to see if we are connected
print('Verifying the ROS target is connected?', client.is_connected)


ml = MotionLib(client)

time.sleep(1) # 1s for the seq to start

try:

  ml.init_move(2) # Initialises simple movement with number of goals

  ml.set_motion_coordinates(0, -0.25, 0.5, 0.1) # Sets the coordinate positions
  ml.set_motion_coordinates(1, 0.65, 0.5, 0.1) # goal number (starting from 0), x, y, z

  ml.set_motion_orientation(0, 0.768795862315926, 0.6384872667721858, 0.01671760406794834, 0.0317404154024891) # Sets the orientation points
  ml.set_motion_orientation(1, 0.7414345473977823, 0.6403921926394932, -0.1496872910512758, 0.1332905339067958) # goal number (starting from 0), x, y, z, w

  ml.set_max_velocity(0, 0.5, 1.5) # Sets max linear and angular velocity
  ml.set_max_velocity(1, 0.5, 1.5) # goal number, linear, angular

  ml.set_max_joint_velocity_accelartion(0, 1.0, 1.0) # Sets maximum joint velocity and acceleration
  ml.set_max_joint_velocity_accelartion(1, 1.0, 1.0) # goal number (starting from 0), velocity, acceleration

  result =  ml.start_motion(client, 30)

  print(result)

except Exception as e:
    print("Error: Could not complete task-- " + str(e))
    time.sleep(0.5) # wait 1/2s 


# Clean up the connection to the robot
client.terminate()
