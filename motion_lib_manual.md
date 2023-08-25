### SIMPLE MOTION ###

**init_move(no_of_goals)**
Initialises simple movement. Pass the number of goals/waypoints wanted for the arm to move to

**set_motion_coordinates(waypoint_number, x, y, z)**
Sets the coordinates for goal "waypoint_number" to x, y, and z coordinates inserted.

**set_motion_orientation(waypoint_number, x, y, z, w)**
Sets the orientation for goal "waypoint_number" to x, y, z and w coordinates inserted.


**set_max_velocity(waypoint_number, linear, angular)**
Sets the velocity for goal "waypoint_number" to linear and angular speed values inserted.

**set_max_joint_velocity_acceleration(waypoint_number, velocity, acceleration)**
Sets the maximum joint velocity and acceleration for goal "waypoint_number".


**start_motion(client, timeout)**
Passing the client to the function starts the motion of the goals set. Passing the timeout assigns a maximum time taken for the motion to plan and execute before timing out and ending the program.


### TRAJECTORY ###

**init_trajectory(joints, goals)**
Sets the number of joints in the arm and the number of goals to be achieved at the end of this sequence

**set_joint_goal(goal, angle, value)**
Set the goal number for a specific joint angle to a certain value

**set_joint_velocity(goal, angle, value)**
Set the valocity at which the angle is to approach a specific goal

**set_time_from_start(goal, value)**
Set value for each value of time to finish motion for the goal's motion

**start_trajectory(client, timeout)**
Start the trajectory motion after setting all the goals. Passing the timeout assigns a maximum time taken for the motion to plan and execute before timing out and ending the program.
