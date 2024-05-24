#!/usr/bin/env python3

import roslibpy
import roslibpy.actionlib

# TODO replace the IP address here with the IP address of your robot
client = roslibpy.Ros(host='localhost', port=9090)
client.run()

print('Is ROS connected?', client.is_connected)

# Create a new action client - this is an object used to send motion goals to the robot
action_client = roslibpy.actionlib.ActionClient(client,
                                                '/default_move_group/move',
                                                'commander_msgs/MotionAction')

# Build up a goal - all positional units are in meters, and all orientations are in quaternion format
# This goal contains two motions specified by cartesian targets
goal = roslibpy.actionlib.Goal(action_client, roslibpy.Message({
    'motion_sequence': [{
        'pose': {
            'position': {
                'x': 0.4,
                'y': 0.4,
                'z': 0.4
            },
            'orientation': {
                'x': 1.0,
                'y': 0.0,
                'z': 0.0,
                'w': 0.0
            }
        },
        'frame_id': 'world',
        'max_velocity': {
            'linear': 0.5,
            'angular': 1.5
        },
        'max_joint_velocity': 0.5,
        'max_joint_acceleration': 0.5
    },
    {
        'pose': {
            'position': {
                'x': -0.4,
                'y': 0.4,
                'z': 0.4
            },
            'orientation': {
                'x': 1.0,
                'y': 0.0,
                'z': 0.0,
                'w': 5.0
            }
        },
        'frame_id': 'world',
        'max_velocity': {
            'linear': 0.5,
            'angular': 1.5
        },
        'max_joint_velocity': 0.5,
        'max_joint_acceleration': 0.5
    }]
}))

# This set's up a callback so we get some feedback while the goal is running
goal.on('feedback', lambda f: print(f))

# Start the goal - this is where the robot will start moving!
goal.send()

# Wait for the goal to finish - only wait for 10 seconds
result = goal.wait(10)

# Clean up the action client
action_client.dispose()

# Print the "result" from the action server
print('Result: {}'.format(result))

# Clean up the connection to the robot
client.terminate()
