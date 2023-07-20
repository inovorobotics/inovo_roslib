#!/usr/bin/env python3

import roslibpy
import time
from sequence_client import SequenceClient
from robot_client import RobotClient
import signal

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, *args):
    self.kill_now = True

# TODO replace the IP address here with the IP address of your robot
try:
  client = roslibpy.Ros(host='localhost', port=9090)
  client.run()
except:
  print("can't connect to the robot, check your IP addess and netowrk connection")
  exit()

# Sanity check to see if we are connected
print('Verifying the ROS target is connected?', client.is_connected)

# The sequence client wraps up our sequence-related service calls
sc = SequenceClient(client, "/sequence")
rc = RobotClient(client, "/default_move_group")

# Run the sequence from the start block




killer = GracefulKiller()

while(not killer.kill_now): # While it is not killed
    if sc.is_paused_on_error(): # Check Paused on Error Status
        if not rc.get_safety_stop_state()['active']: # Check Safety Stop Status
            print("Safety Stop is Active")
            if not rc.get_safety_stop_state()['circuit']:
               print("Safety Stop Button needs to be released")
               time.sleep(0.5)
            else:
               time.sleep(0.5)
               print("Clearing Safety Stop")
               rc.safe_stop_reset()
            time.sleep(1)
        
        if not rc.get_estop_state()['active']: # An EStop would turn off the power to the robot
           print("E-Stop is on. Please reset manually for safety.") # Resetting it manually would be the safest option
        
        if rc.get_safety_stop_state()['active'] and rc.get_estop_state()['active']:
           print("Enabling Arm and resuming process")
           rc.robot_arm_enable()
           time.sleep(2)
           sc.continue_sequence()
           

    time.sleep(1)
      

print("Terminating Connection.")

# Clean up the connection to the robot
client.terminate()

print("ROS connection closed.")
