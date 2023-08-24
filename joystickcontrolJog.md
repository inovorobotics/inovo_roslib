**Pre-requisites**
Other than our own library ((LIBRARY NAME)) and roslibpy, using the joystick requires the use of the PyGame library.
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