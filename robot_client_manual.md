**get_tcp_linear_speed()**
Returns a float type value. Gets the TCP linear speed.

**get_tcp_angular_speed()**
Returns a float type value. Gets the TCP angular speed.

**get_tcp_coordinates()**
Returns a dictionary type value. Gets the coordinates of the TCP. Keys: 'x','y','z'. 
Can be used to return a single coordinate. e.g. get_tcp_coordinates()['x']

**get_tcp_orientation()**
Returns a dictionary type value. Gets the orientation of the TCP. Keys: 'x','y','z','w'. 
Can be used to return a single orientation. e.g. get_tcp_orientation()['x']

**get_joint_angles()**
Returns an array type value. Gets the angle of each joint. 
Can be used to get a single joint's info. e.g. get_joint_angles()[0]

**get_joint_velocity()**
Returns an array type value. Gets the velocity of each joint. 
Can be used to get a single joint's info. e.g. get_joint_velocity()[0]

**get_joint_effort()**
Returns an array type value. Gets the effort of each joint. 
Can be used to get a single joint's info. e.g. get_joint_effort()[0]


**get_power_state()**
Returns a boolean of on (True) or off (False) depending on the BUS state

**get_arm_power()**
Returns a boolean of on (True) or off (False) depending on the drives

**get_arm_active()**
Returns a boolean of on (True) or off (False) depending on the driver state


**get_estop_state**
Returns a dictionary with the state of the emergency stop. When active is true it means it is no longer pushed down, and vice versa. When circuit is true it means the circuit is complete.

**get_safety_stop_state**
Returns a dictionary with the state of the safety stop. When active is true it means it is no longer pushed down, and vice versa. When circuit is true it means the circuit is complete.

**get_sequence_state()**
Returns an integer depending on the current state of the sequence.
    SEQUENCE_STATUS_IDLE = 0
    SEQUENCE_STATUS_RUNNING = 1
    SEQUENCE_STATUS_PAUSED = 2
    SEQUENCE_STATUS_PAUSED_ON_ERROR = 3
As defined at the top of the library

**safety_stop_reset()**
Resets the safety stop status. Make sure that the physical switch is active, i.e. not pressed down.

**estop_reset()**
Resets the emergency stop status. Make sure that the physical switch is active, i.e. not pressed down.


**arm_power_on()**
Turns on the power to the arm. Note that it takes a few seconds for the arm to turn on.

**arm_power_off()**
Turns off the power to the arm.

**robot_arm_enable()**
Initialises the robot arm.

**robot_arm_disable()**
Disables the robot arm, keeping the power connected.

**set_power(bool)**
Sets the state of the power to the arm either on (1) or off (0). Note that it takes a few seconds for the arm to turn on.

**set_arm(bool)**
Sets the state of the robot arm either on (1) or off (0). 