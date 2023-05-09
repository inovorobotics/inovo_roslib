#!/usr/bin/env python3

import roslibpy
from sequence_client import SequenceClient
import time, os

# TODO replace the IP address here with the IP address of your robot
client = roslibpy.Ros(host='192.168.8.126', port=9090)
client.run()

# Sanity check to see if we are connected
print('Is ROS connected?', client.is_connected)

# The sequence client wraps up our sequence-related service calls
sc = SequenceClient(client, "/sequence")

# load project from file and Upload to the robot
sample_file = os.path.join(os.path.dirname(__file__), 'example_1_sequence.isq')
xml_seq, xml_ws = sc.load_project_XML(sample_file)
sc.upload_ws(xml_ws)
sc.upload_seq(xml_seq)

# Run the sequence from the start block
print("press enter to run sequence from start - WARNING the robot will move!")
input()
sc.start()

## Wait for the sequence to finish running
sc.wait_until_idle()

# Clean up the connection to the robot
client.terminate()
