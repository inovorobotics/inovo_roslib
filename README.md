# inovo_roslib
Example roslibpy implementations for controlling the robot using the rosbridge JSON interface.

## Introduction
This repository provides examples which use the [rosbridge protocol](https://github.com/RobotWebTools/rosbridge_suite/blob/develop/ROSBRIDGE_PROTOCOL.md) to communicate with the robot. There are multiple client libraries written for languages that support this protocol, notable examples being [roslibjs](https://github.com/RobotWebTools/roslibjs) for javascript and [roslibpy](https://github.com/gramaziokohler/roslibpy) for python. These examples are written against roslibpy.

## Usage

!!! WARNING !!!
The examples in this repository will move the robot to arbitrary positions. Always hold the e-stop when running these scripts so you can stop the robot before it crashes into anything.

Install python dependencies
```
pip3 install -r requirements.txt
```

Replace the IP address in the scripts with the IP address of your robot.

Run the examples with:
```
./<scriptname>
```

## Functions

#get_status
returns the run time status as an integer, 0 = idle, 1 = running, 2 = paused

#is_running
return true if the sequencer is running, otherwise returns false

#is_idle
return trie if the sequencer is idle, otherwise returns false

#wait_until_idle
blocks until the sequener is idle, then returns. this functions implments a 100ms sleep between each status check.

#start
runs the entire sequence

#call_function(<function_name>)
runs the speficed function currently loead in the blockly sequence 


