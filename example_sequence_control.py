#!/usr/bin/env python3

import roslibpy
from sequence_client import SequenceClient
import time

# TODO replace the IP address here with the IP address of your robot
client = roslibpy.Ros(host='localhost', port=9090)
client.run()

# Sanity check to see if we are connected
print('Is ROS connected?', client.is_connected)

# The sequence client wraps up our sequence-related service calls
sc = SequenceClient(client, "/sequence")

# Upload blockly to the robot
sc.upload("""
<?xml version="1.0" encoding="utf-8"?>
<xml xmlns="https://developers.google.com/blockly/xml">
    <block id="53ec252b-607b-48f1-9edc-bd973064645e" type="workspace" collapsed="false" disabled="false" x="-43" y="-157">
        <statement name="OBJECTS">
            <block id="f09da19a-9f5a-47bf-878d-01dde1748c37" type="robot_ica" collapsed="false" disabled="false">
                <field name="DEFAULT_TCP"/>
                <field name="NAME"/>
                <field name="NAMESPACE">/robot</field>
            </block>
        </statement>
    </block>
    <block id="3f432e95-a694-4695-a896-072ccdc0f2d8" type="controls_start" collapsed="false" disabled="false" x="-34" y="169">
        <next>
            <block id="726d1425-7d0e-4998-84da-8f323965250e" type="motion_move_to_ext" collapsed="false" disabled="false" x="52" y="529">
                <value name="TARGET">
                    <block id="3c7029b3-e164-4ee8-a735-8ecaa9e0840e" type="robot_pose_form" collapsed="false" disabled="false">
                        <field name="J1">0</field>
                        <field name="J2">1</field>
                        <field name="J3">2</field>
                        <field name="J4">3</field>
                        <field name="J5">4</field>
                        <field name="J6">5</field>
                    </block>
                </value>
                <field name="MOTION_TYPE">JOINT</field>
                <field name="USE_NEAREST_JOINTSPACE_TARGET">FALSE</field>
            </block>
        </next>
    </block>
</xml>
""")

# Run the sequence from the start block
sc.start()

## Wait for a but then stop the sequence again
time.sleep(3)
sc.stop()

# Clean up the connection to the robot
client.terminate()
