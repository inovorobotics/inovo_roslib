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

To get started created a new file, import  roslibpy and sequence_cleint as below then create an instance 
```
import roslibpy
from sequence_client import SequenceClient
```
create a ROSLibPy insance setting the host name or IP in the constructor@
```
client = roslibpy.Ros(host='localhost', port=9090)
```

next you can check the connection with the is_connected function
```
# Sanity check to see if we are connected
print('Is ROS connected?', client.is_connected)
```
and create an instance of the SequenceClint
```
# The sequence client wraps up our sequence-related service calls
sc = SequenceClient(client, "/sequence")
```
at the end of your file add a distructor to close the ROS bridge connection
```
# Clean up the connection to the robot
client.terminate()
```
now you are ready to define your application in between, for example

```
sc.call_function("doPick")
sc.wait_until_idle()
print ("done Pick")

sc.call_function("doPlace")
sc.wait_until_idle()
print ("done Place")
```


## SequenceClient Functions

**get_status()**
returns the run time status as an integer, 0 = idle, 1 = running, 2 = paused

**is_running()**
return true if the sequencer is running, otherwise returns false

**is_idle()**
return trie if the sequencer is idle, otherwise returns false

**wait_until_idle()**
blocks until the sequener is idle, then returns. this functions implments a 100ms sleep between each status check.

**start()**
continues the sequence if pauses, if stopped runs from the start block

**stop()**
stops the sequence

**pause()**
pauses the sequence at the current location

**step()**
runs the next block at the current location

**call_function(*<function_name>*)**
runs the specified function currently loead in the blockly sequence 

**upload(*<xml_string>*)**
allow you to upload a blockly sequence in XML format to the sequencer, this will overwrite any existing sequence.




