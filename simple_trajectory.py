import roslibpy
import roslibpy.actionlib

# TODO replace the IP address here with the IP address of your robot
client = roslibpy.Ros(host='localhost', port=9090)
client.run()

print('Is ROS connected?', client.is_connected)

service = roslibpy.Service(client, '/robot/switch_controller', 'inovo_driver/SwitchControllerGroup')
request = roslibpy.ServiceRequest({'name': 'trajectory'})
result = service.call(request)
print('Service response: {}'.format(result))

action_client = roslibpy.actionlib.ActionClient(client,
                                                '/robot/joint_trajectory_controller/follow_joint_trajectory',
                                                'control_msgs/FollowJointTrajectoryAction')

goal = roslibpy.actionlib.Goal(action_client, roslibpy.Message({
    'trajectory': {
        'joint_names': [f'j{x}' for x in range(1, 7)],
        'points': [{
            'positions': [0.0] * 6,
            'velocities': [0.0] * 6,
            'time_from_start': {'secs': 3}
        },{
            'positions': [1.0] * 6,
            'velocities': [0.0] * 6,
            'time_from_start': {'secs': 6}
        }]
    }}))

goal.on('feedback', lambda f: print(f))
goal.send()
result = goal.wait(10)
action_client.dispose()
print('Result: {}'.format(result))

client.terminate()
