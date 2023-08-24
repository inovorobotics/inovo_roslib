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
create a ROSLibPy insance setting the host name or IP in the constructor
```
client = roslibpy.Ros(host='localhost', port=9090)
client.run()
```

next you can check the connection with the is_connected function
```
# Sanity check to see if we are connected
print('Is ROS connected?', client.is_connected)
```
and create an instance of the SequenceClient
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
returns the run time status as an integer, 0 = idle, 1 = running, 2 = paused, 3 = paused on error

**is_running()**
returns true if the sequencer is running, otherwise returns false

**is_idle()**
return true if the sequencer is idle, otherwise returns false

**wait_until_idle()**
blocks until the sequencer is idle, then returns. this functions implments a 100ms sleep between each status check.

**start_sequence()**
if stopped runs the sequence from the start block

**stop_sequence()**
stops the sequence

**pause_sequence()**
pauses the sequence at the current location

**continue_sequence()**
continues the sequence from where it has been paused

**step_sequence()**
runs the next block at the current location

**call_function(*<function_name>*)**
runs the specified function currently loaded in the blockly sequence 

**load_project_XML(*<path_to_file>*)**
This loads a project file in .isq format and returns the sequence and workspace parts as xml strings that can then be used to call upload_seq and upload_ws (see below)

**upload_seq(*<xml_string>*)**
allows you to upload a blockly sequence in XML format to the sequencer, this will overwrite any existing sequence.

**upload_ws(*<xml_string>*)**
allows you to upload a blockly sequence in XML format to the workspace, this will overwrite any existing workspace config.

**getVar(*<var_name>*)**
returns the current value of a user variable from the running sequence. If the variable is not in scope or the sequence is not running throws an exception

**setVar(*<var_name>*,*<value>*)**
sets the value of a user variable in the running sequence. If the variable is not in scope or the sequence is not running throws an exception

## Robot_Client functions
Please refer to the "robot_client_manual.md" for this library's functions

## Example_1_sequence.py - running the sequencer remoetly. calling functions on demand and reading variables in real time
This example connects to the robot, runs the main sequence and then calls two functions in the sequence. 
Import example_1_sequence.isq into the robot using the standard browser interface (menu>import)
Update the IP address on line 10 to point at your robot.
Make sure the robot can move to the waypoints in the example sequence safely, without collision or risk to people.
Run the example_1.py file, it will prompt you to press enter before it runs the main sequence. 
While the robot moves the python code will pole the statue of the sequencer and read a user variable called ‘n’ printing the value to the debug console. When the sequence finishes execution the python code will then prompt you to press enter again before calling the up down function. It will wait until this function completes and the sequencer returns to the idle state before prompting you to press enter again before calling the left right sequence.

## Example_2_upload_sequence.py – uploads a sequence as XML data and runs it
This example connects to the robot, uploads a sequence and runs it. You can capture a sequence by exporting the currently loaded sequence from the main browser interface, select export from the file menu.

## Example_3_robot_control.py
This example connects to the robot, then checks for the safety stop and estop statuses, and asks the user to unlock the buttons if they are pressed down.
After that, it turns the arm's power on and activates it, grabs some of the robot's information, e.g., the TCP coordinates, and turns off the arm again.

## Example_4_auto_resume.py
This example connects to the arm and keeps looping until it is killed by sending a termination or interruption signal (e.g., using CTRL + C to interrupt). While running a sequence it continuously checks if the arm has paused on an error, either due to a collision or due to either of the safety or the emergency buttons being pressed. If it detects that either of them are pressed, it asks the user to release the button, re-enables the arm, and continues the sequence from the position it was paused at.

## Example_5_joystickcontrol.py 
**Pre-requisites**
Other than our own library (robot_client.py) and roslibpy, using the joystick requires the use of the PyGame library.
Note: This was tested using the Logitech F310 gamepad

**The Program**
The getJoy function takes the axis and the joystick instance as parameters.
This function grabs the offset of the joystick stick at the specified direction defined for the joystick make, e.g. for the left stick up and down would be axis 1.
An if condition is added to the function to make up for joystick drift.
The demand is multiplied by 0.1 to make the movement slower and smoother for safety.

The joystick is initialised using the PyGame library following normal procedure.
A kill variable is created to be used to exit the while loop.
The loop captures all the joystick inputs on the stick being moved on the 0, 1 and 3 axes and records it in a dictionary.
It reads buttons pressed continuously to waiting for button 1, 5, or 4 to be pressed. In this example these buttons correspond to the B, RB, and LB buttons on the Logitech F310.
Pressing B kills the program.
Pressing RB calls the linear jog function from our library, moving the arm linearly.
Pressing LB calls the angular jog function causing a rotation of the arm.
If neither buttons are pressed the program sends a zero message to avoid drifting.

Exiting the while loop the program terminates the joystick control and client connection.