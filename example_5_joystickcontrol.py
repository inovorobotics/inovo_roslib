#!/usr/bin/env python3

import roslibpy
import time
from robot_client import RobotClient
import pygame ## A library used to read joystick inputs

### Note: This was tested using the Logitech F310 gamepad ###

try:
  client = roslibpy.Ros(host='localhost', port=9090) # Change host to the IP of the robot
  client.run()
except:
  print("Cannot connect to the robot, check your IP addess and network connection")
  exit()

# Sanity check to see if we are connected
print('Verifying the ROS target is connected?', client.is_connected)    # HW - If its not connected then we should terminate the progam here #AA - That's taken care of in the try loop above, this is only a sanity check that is adapted from previous examples

rc = RobotClient(client)


coords ={'x': 0.0,
         'y': 0.0,
         'z': 0.0}


def getJoy(axis, joystick): # axis is in reference to the joystick motion
    demand = joystick.get_axis(axis)
    if demand < 0.005 and demand > -0.005: demand = 0 # Applying dead band to avoid drift when joystick is released

    return demand*0.1
try:

    pygame.init()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    maxC = 0
    kill = False
    while not kill:
        for event in pygame.event.get():
            time.sleep(0)
        #get events from the queue

        coords['x'] = getJoy(0, joystick)
        coords['y'] = getJoy(1, joystick)
        coords['z'] = getJoy(3, joystick)

        if joystick.get_button(1): # read B to kill the program
                kill = True
        if joystick.get_button(5): # read RB
            rc.linear_jog_pub(client, coords)
        if joystick.get_button(4): # read LB
            rc.ang_jog_pub(client, coords)
        if not (joystick.get_button(5) or joystick.get_button(4)): # if neither RB or LB are pressed set to zero to avoid drift
            coords['x'] = 0
            coords['y'] = 0
            coords['z'] = 0
            rc.linear_jog_pub(client, coords)
            rc.ang_jog_pub(client, coords)

        pygame.time.Clock().tick(60) # setting the frame rate (FPS/Hz)


    print("Program Killed") # Printed after exiting the loop by B press
    pygame.quit()


except Exception as  e:
    print('Failed to upload to ftp: '+ str(e))
time.sleep(0.5) 


# Clean up the connection to the robot
client.terminate()
