from __future__ import print_function
import copy

import time
import roslibpy
import roslibpy.actionlib


class MotionLib:

    def __init__(self, ros):
        self._ros = ros

        self.goalStat = {"state": 0} # A dictionary for possible future expansions

        self.goal_num = 0
        self.joint_names = []
        self.goal_info = []
        self.trajectory_goals = []

        self.motion_goal_settings = { # Dictionary in case of simple motion
            'pose':{
                'position':{'x': 0, 
                            'y': 0, 
                            'z': 0},
                'orientation':{'x': 1.0, 
                               'y': 0, 
                               'z': 0, 
                               'w': 0},
                               },
            'frame_id': 'world', # Default frame
            'max_velocity': {'linear': 0.5, ## Default velocities
                              'angular': 1.5},
            'max_joint_velocity': 0.5,
            'max_joint_acceleration': 0.5
        }


        self.trajectory_goal_settings = { # Dictionary in case of trajectory ### WIP ###
            
                'positions':[],
                'velocities': [],
                'time_from_start': {'secs': 3} # Default time
            
        }


    def wait_for_goal(self, goal_timeout):
        quit_time = time.time() + goal_timeout
        while time.time() < quit_time:
            if self.goalStat["state"] == 3:
                return "Success"
            if self.goalStat["state"] == 4:
                return "Unable to solve IK"
        return "Timed out"

    def init_move(self, no_of_goals): # Initialises an array of the dictionary simple motion with the set number of goals  
        self.goal_num = no_of_goals
        for k in range (no_of_goals):
            self.goal_info.append(copy.deepcopy(self.motion_goal_settings))



    def set_motion_coordinates(self, pos, x, y, z): # Sets the coordinates for the goal
        self.goal_info[pos]['pose']['position']['x'] = x
        self.goal_info[pos]['pose']['position']['y'] = y
        self.goal_info[pos]['pose']['position']['z'] = z

    def set_motion_orientation(self, pos, x, y, z, w): # Sets the orientation for the goal
        self.goal_info[pos]['pose']['orientation']['x'] = x
        self.goal_info[pos]['pose']['orientation']['y'] = y
        self.goal_info[pos]['pose']['orientation']['z'] = z
        self.goal_info[pos]['pose']['orientation']['w'] = w


    def set_max_velocity(self, pos, linear, angular): # Sets the maximum linear and angular velociteis
        self.goal_info[pos]['max_velocity']['linear'] = linear
        self.goal_info[pos]['max_velocity']['angular'] = angular

    def set_max_joint_velocity_accelartion(self, pos, velocity, acceleration): # Sets the maximum join velocity and acceleration
        self.goal_info[pos]['max_joint_velocity'] = velocity
        self.goal_info[pos]['max_joint_acceleration'] = acceleration


    def printStatus(self, f):
        self.goalStat["state"] = f["status"]

    def start_motion(self, client, timeout): # Starts the motion by sending the message to the action server, returns a string to resport sucess or timeout

        action_client = roslibpy.actionlib.ActionClient(client,
                                                '/default_move_group/move',
                                                'virtual_robot/MotionAction')


        message_ = {'motion_sequence': self.goal_info} ## Creating a dictionary that looks the same as the simple motion

        goal = roslibpy.actionlib.Goal(action_client, roslibpy.Message(message_))
        goal.on('feedback', lambda f: print(f))
        goal.on("status", lambda f: self.printStatus(f))
        ## Start the goal - this is where the robot will start moving!
        goal.send()

        result = self.wait_for_goal(timeout)    

        # Clean up the action client
        action_client.dispose()
        
        return result

    def print_goal(self):
        print(self.goal_info)

##### TRAJECTORY ANGLE MOTION #####

    def init_trajectory(self, joints, goals):
        self.joint_names = [f'j{x}' for x in range(1, joints+1)] # Set the names of the joints from one to the number of joints
        for k in range(goals):
            setting = copy.deepcopy(self.trajectory_goal_settings)
            setting['positions'] = [0.0]*joints
            setting['velocities'] = [0.0]*joints

            self.trajectory_goals.append(setting) # Make an array of the same type of settings needed for trajectory



    def set_joint_goal(self, goal, joint_num, value): # Set value for each joint for the goal's motion
        self.trajectory_goals[goal]['positions'][joint_num] = value


    def set_joint_velocity(self, goal, joint_num, value): # Set value for each value of joint velocity for the goal's motion
        self.trajectory_goals[goal]['velocities'][joint_num] = value



    def set_time_from_start(self, goal, value): # Set value for each value of time to finish motion for the goal's motion
        self.trajectory_goals[goal]['time_from_start']['secs'] = value



    def start_trajectory(self, client, timeout):
        service = roslibpy.Service(client, '/robot/switch_controller', 'inovo_driver/SwitchControllerGroup')
        request = roslibpy.ServiceRequest({'name': 'trajectory'})
        result = service.call(request)
        #print('Service response: {}'.format(result))

        action_client = roslibpy.actionlib.ActionClient(client, # Setting up the client for the trajectory action
                                                '/robot/joint_trajectory_controller/follow_joint_trajectory',
                                                'control_msgs/FollowJointTrajectoryAction')

        message_ = {'trajectory': { # Compiling the message of different dictionaries and arrays to be sent to the server
                                'joint_names': self.joint_names, 
                                'points': self.trajectory_goals
                                }}

        goal = roslibpy.actionlib.Goal(action_client, roslibpy.Message(message_))

        goal.on('feedback', lambda f: print(f))
        goal.send()
        result = goal.wait(timeout)
        action_client.dispose()
        #print('Result: {}'.format(result))
        return result
