import roslibpy
import roslibpy.actionlib

# TODO replace the IP address here with the IP address of your robot
client = roslibpy.Ros(host='localhost', port=9090)
client.run()

print('Is ROS connected?', client.is_connected)

action_client = roslibpy.actionlib.ActionClient(client,
                                                '/default_move_group/move',
                                                'virtual_robot/MotionAction')

goal = roslibpy.actionlib.Goal(action_client, roslibpy.Message({
    'motion_sequence': [{
        'pose': {
            'position': {
                'x': 0.4,
                'y': 0.4,
                'z': 0.4
            },
            'orientation': {
                'x': 0.0,
                'y': 0.0,
                'z': 0.0,
                'w': 1.0
            }
        },
        'frame_id': 'world',
        'max_velocity': {
            'linear': 0.5,
            'angular': 0.5
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
                'x': 0.0,
                'y': 0.0,
                'z': 0.0,
                'w': 1.0
            }
        },
        'frame_id': 'world',
        'max_velocity': {
            'linear': 0.5,
            'angular': 0.5
        },
        'max_joint_velocity': 0.5,
        'max_joint_acceleration': 0.5
    }]
}))

goal.on('feedback', lambda f: print(f))
goal.send()
result = goal.wait(10)
action_client.dispose()
print('Result: {}'.format(result))

client.terminate()
