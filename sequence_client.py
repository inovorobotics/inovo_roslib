from __future__ import print_function
import roslibpy
import time, re



GRAVITY = 9.8

class SequenceClient:

    # Run Time States retuned by
    RUNTIME_STATUS_IDLE = 0
    RUNTIME_STATUS_RUNNING = 1
    RUNTIME_STATUS_PAUSED = 2

    def __init__(self, ros, ns):
        self._ros = ros
        self._ns = ns
        self.runtime_status = 0

        self._upload_ws_service = roslibpy.Service(self._ros, f"{self._ns}/update_scene", "commander_msgs/Upload")
        self._upload_seq_service = roslibpy.Service(self._ros, f"{self._ns}/upload", "commander_msgs/Upload")

        self._start_service = roslibpy.Service(self._ros, f"{self._ns}/start", "commander_msgs/RunSequence")
        self._stop_service = roslibpy.Service(self._ros, f"{self._ns}/stop", "std_srvs/Trigger")
        self._pause_service = roslibpy.Service(self._ros, f"{self._ns}/pause", "std_srvs/Trigger")
        self._step_service = roslibpy.Service(self._ros, f"{self._ns}/step", "std_srvs/Trigger")
        self._debug_service = roslibpy.Service(self._ros, f"{self._ns}/debug", "std_srvs/Trigger")
        self._runTimeState_client = roslibpy.Topic(self._ros, '/sequence/runtime_state', '/commander_msgs/RuntimeState')
        self._runTimeState_client.subscribe (self.status_update)
        self._setVar_service = roslibpy.Service( self._ros, '/sequence/set_var', 'commander_msgs/SetVariable')
        self._getVar_service = roslibpy.Service( self._ros, '/sequence/get_var', 'commander_msgs/GetVariable')

    def status_update( self, message):
        self.runtime_status = message['state']

    def get_status(self):   # "commander_msgs/RuntimeState"
        return self.runtime_status

    def is_running(self):   # "commander_msgs/RuntimeState"
        return (self.runtime_status == self.RUNTIME_STATUS_RUNNING)

    def is_idle(self):   # "commander_msgs/RuntimeState"
        return (self.runtime_status == self.RUNTIME_STATUS_IDLE)

    def wait_until_idle(self):
        while (self.is_running()): 
            time.sleep(0.1)
            
    def upload_ws(self, blockly_xml):
        request = roslibpy.ServiceRequest({"blockly": blockly_xml})
        result = self._upload_ws_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to upload work space blockly: {result['message']}")

    def upload_seq(self, blockly_xml):
        request = roslibpy.ServiceRequest({"blockly": blockly_xml})
        result = self._upload_seq_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to upload blockly: {result['message']}")


    def load_project_XML(self, file_path):
        """
        Function that takes input as combined XMLs and then seperates in to two string 
        """

        with open(file_path) as f:
            file_content = f.read().rstrip("\n")

        st = [a.start() for a in list(re.finditer('<xml', file_content))]
        end = [a.start() for a in list(re.finditer('</xml>', file_content))]

        seq = file_content[st[1]:end[0]+6]
        ws = file_content[st[2]:end[1]+6]

        return seq, ws

    def start(self):
        request = roslibpy.ServiceRequest()
        result = self._start_service.call(request)
        if result['success']:
            self.runtime_status = self.RUNTIME_STATUS_RUNNING
        else:
            raise Exception(f"Unable to start the sequence: {result['message']}")

    def call_function(self, function_name):
        request = roslibpy.ServiceRequest({"procedure_name" : function_name})
        result = self._start_service.call(request)
        if result['success']:
            self.runtime_status = self.RUNTIME_STATUS_RUNNING
        else:
            raise Exception(f"Unable to start the sequence: {result['message']}")

    def stop(self):
        request = roslibpy.ServiceRequest()
        result = self._stop_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to stop the sequence: {result['message']}")

    def pause(self):
        request = roslibpy.ServiceRequest()
        result = self._pause_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to pause the sequence: {result['message']}")

    def debug(self):
        request = roslibpy.ServiceRequest()
        result = self._debug_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to debug the sequence: {result['message']}")

    def step(self):
        request = roslibpy.ServiceRequest()
        result = self._step_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to step the sequence: {result['message']}")
        
    def setVar(self, var_name, var_val):
        """
        var_name = variable Name in str 
        var_val = float/int
        """
        request = roslibpy.ServiceRequest({
        "name": var_name,
        "value": str(var_val)})
        
        result = self._setVar_service.call(request)

        if not result['success']:
            raise Exception(f"Unable to set varable : {result['message']}")



    def getVar(self, var_name):
        """
        var_name = variable Name in str 
        return value or thorws exception if not found
        """
        request = roslibpy.ServiceRequest({
        "name": var_name})

        result = self._getVar_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to get varable : {result['message']}")
        else :
            return result['value']
        
