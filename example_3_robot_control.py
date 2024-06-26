#!/usr/bin/env python3

import roslibpy
import time
from robot_client import RobotClient 

try:
  client = roslibpy.Ros(host='localhost', port=9090) # Change host to the IP of the robot
  client.run()
except:
  print("can't connect to the robot, check your IP address and network connection")
  exit()

# Sanity check to see if we are connected
print('Verifying the ROS target is connected?', client.is_connected)



rc = RobotClient(client)

time.sleep(1) # To give it time to connect

try:

  while((not rc.get_safety_stop_state()['active']) or (not rc.get_estop_state()['active'])): # Check Safety Stop and reset
     print('Safety stop is active')
     time.sleep(1.0)

     if rc.get_safety_stop_state()['circuit'] == rc.SAFETY_CIRCUIT_OPEN : # If the circuit is open i.e. button is pressed down
        print('Unlock the Safety Stop Button') # Kindly

     else:
        rc.safe_stop_reset()

     if rc.get_estop_state()['circuit'] == rc.SAFETY_CIRCUIT_OPEN : # If the circuit is open i.e. button is pressed down
        print('Unlock the Emergency Stop Button') # Kindly

     else:
        rc.estop_reset()

  if rc.get_arm_power() == False: # If the arm is off turn it on
     rc.arm_power_on()
  while(rc.get_arm_active() == False): # Wait for the arm to be active
     print("Initialising Arm..")
     time.sleep(1)
  
  rc.robot_arm_enable() # Enable the arm

  print('Coordinates of TCP: ', rc.get_tcp_coordinates()) # Dictionary of cartesian coordinates of TCP
  print('Effort: ', rc.get_joint_effort()) # Array of effort in Newton meters
  print('Joint Angles: ', rc.get_joint_angles()) # Array of joint angles in radians

  time.sleep(5)
  rc.robot_arm_disable()
  rc.arm_power_off()


except:
    print("Error: Could not complete task")
time.sleep(0.5) 


# Clean up the connection to the robot
client.terminate()
