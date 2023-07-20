from __future__ import print_function
import roslibpy



GRAVITY = 9.8

class RobotClient:

    SAFETY_CIRCUIT_OPEN = 0
    SAFETY_CIRCUIT_CLOSED = 1

    def __init__(self, ros, ns):
        self._ros = ros
        self._ns = ns


        # SUBSCRIBING TO TCP SPEED ON ROS
        self.tcp_speed_client = roslibpy.Topic(self._ros, '/default_move_group/tcp_speed', 'commander_msgs/SpeedStamped')
        self.tcp_speed_client.subscribe (self.tcp_speed)
        self.Speed = {'Lin': 0, # Dictionary of Speeds
                      'Ang': 0} 



        # SUBSCRIBING TO TCP POSE ON ROS
        self.tcp_pose_client = roslibpy.Topic(self._ros, '/default_move_group/tcp_pose', 'geometry_msgs/PoseStamped')
        self.tcp_pose_client.subscribe (self.tcp_pose)
        self.Pose = {'Coords' : {'x': 0, 'y': 0, 'z': 0}, # Dictionary of Poses
                     'Ori' : {'x': 0, 'y': 0, 'z': 0, 'w': 0}}


        # SUBSCRIBING TO JOINT STATES
        self.joint_states_client = roslibpy.Topic(self._ros, '/robot/joint_states', 'sensor_msgs/JointState')
        self.joint_states_client.subscribe(self.joint_states)
        self.State = {'pos': [], # A dictionary of array states
                      'vel':[],
                      'eff':[]}

        self.power_state_client = roslibpy.Topic(self._ros, '/psu/status', 'psu_msgs/Status')
        self.power_state_client.subscribe(self.power_state)
        self.power = False

        self.arm_ready_client = roslibpy.Topic(self._ros, '/robot/robot_state', 'arm_msgs/RobotState')
        self.arm_ready_client.subscribe(self.arm_ready)
        self.arm = {'driver_active': False,
                    'power':False}

        self.estop_state_client = roslibpy.Topic(self._ros, '/psu/estop/state', 'psu_msgs/SafetyCircuitState')
        self.estop_state_client.subscribe(self.estop_state)
        self.estop = {'active': False,
                      'circuit': False}

        self.safe_stop_state_client = roslibpy.Topic(self._ros, '/psu/safe_stop/state', 'psu_msgs/SafetyCircuitState')
        self.safe_stop_state_client.subscribe(self.safety_stop_state)
        self.safe_stop = {'active': False,
                      'circuit': False}


        #### Services ####

        self.safe_stop_reset_service = roslibpy.Service(self._ros, '/psu/safe_stop/reset', 'std_srvs/Trigger')
        
        self.estop_reset_service = roslibpy.Service(self._ros, '/psu/estop/reset', 'std_srvs/Trigger')

        self.power_on_service = roslibpy.Service(self._ros, '/psu/enable', 'std_srvs/Trigger')

        self.power_off_service = roslibpy.Service(self._ros, '/psu/disable', 'std_srvs/Trigger')

        self.arm_on_service = roslibpy.Service(self._ros, '/robot/enable', 'std_srvs/Trigger')

        self.arm_off_service = roslibpy.Service(self._ros, '/robot/disable', 'std_srvs/Trigger')

#### TOPIC FUNCTIONS ####

    def tcp_speed(self, message):
        self.Speed['Lin'] = message['speed']['linear']
        self.Speed['Ang'] = message['speed']['angular']

    def get_tcp_linear_speed(self):  
        return self.Speed['Lin']

    def get_tcp_angular_speed(self):   
        return self.Speed['Ang']


    def tcp_pose(self, message):
        # Setting the coordinates
        self.Pose['Coords']['x'] = message['pose']['position']['x'] 
        self.Pose['Coords']['y'] = message['pose']['position']['y']
        self.Pose['Coords']['z'] = message['pose']['position']['z']
    
        # Setting the orientations
        self.Pose['Ori']['x'] = message['pose']['orientation']['x']
        self.Pose['Ori']['y'] = message['pose']['orientation']['y']
        self.Pose['Ori']['z'] = message['pose']['orientation']['z']
        self.Pose['Ori']['w'] = message['pose']['orientation']['w']

    def get_tcp_coordinates(self): # get_tcpCoordinates()
        return self.Pose['Coords']

    def get_tcp_orientation(self): # get_Orient()
        return self.Pose['Ori']


    def joint_states(self, message):
        jointNum = len(message['position']) # Number of joints from the ROS dictionary

        # Giving the arrays the correct size according to the number of joints
        self.State['pos'] = [0] * jointNum
        self.State['vel'] = [0] * jointNum
        self.State['eff'] = [0] * jointNum

        # for each joint number, set the corresponding joint stat
        for x in range(jointNum):
            self.State['pos'][x] = message['position'][x]
            self.State['vel'][x] = message['velocity'][x]
            self.State['eff'][x] = message['effort'][x]

    
    def get_joint_angles(self): # get_joint_angles()[angle_num] or get_JointAngles() to get an array of them
        return self.State['pos']
    
    def get_joint_velocity(self): 
        return self.State['vel']
    
    def get_joint_effort(self): 
        return self.State['eff']


    ## POWER AND ARM STATUS TOPICS
    def power_state(self, message):
        if message['state'] == "BUS_ON":
            self.power = True
        else:
            self.power = False

    def get_power_state(self):
        return self.power

    def arm_ready(self, message): 
        if message['driver_state'] == 'Active':
            self.arm['driver_active'] = True
        else:
            self.arm['state'] = False
        self.arm['powered'] = message['drives_powered']

    def get_arm_power(self):
        return self.arm['powered']

    def get_arm_active(self):
        return self.arm['driver_active']

    def estop_state(self, message):
        self.estop['active'] = message['active']
        self.estop['circuit'] = message['circuit_complete']

    def get_estop_state(self):
        return self.estop 

    def safety_stop_state(self, message):
        self.safe_stop['active'] = message['active']
        self.safe_stop['circuit'] = message['circuit_complete']

    def get_safety_stop_state(self):
        return self.safe_stop

    ##### SERVICES #####

    def safe_stop_reset(self): ## MAKE SURE IT IS PHYSICALLY INACTIVE
        request = roslibpy.ServiceRequest()
        result = self.safe_stop_reset_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to reset safety stop: {result['message']}")

    def estop_reset(self):
        request = roslibpy.ServiceRequest()
        result = self.estop_reset_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to reset emergency stop: {result['message']}")

    def arm_power_on(self):
        request = roslibpy.ServiceRequest()
        result = self.power_on_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to turn on power: {result['message']}")

    def arm_power_off(self):
        request = roslibpy.ServiceRequest()
        result = self.power_off_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to turn off power: {result['message']}")

    def robot_arm_enable(self):
        request = roslibpy.ServiceRequest()
        result = self.arm_on_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to enable the arm: {result['message']}")

    def robot_arm_disable(self):
        request = roslibpy.ServiceRequest()
        result = self.arm_off_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to disable the arm: {result['message']}")

    def set_power(self, bool):
        if bool == True:
            self.arm_power_on()
        elif bool == False:
            self.arm_power_off()
        else:
            raise Exception(f"Unable to set state")

    def set_arm(self, bool):
        if bool == True:
            self.robot_arm_enable()
        elif bool == False:
            self.robot_arm_disable()
        else:
            raise Exception(f"Unable to set state")

