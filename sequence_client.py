from __future__ import print_function
import roslibpy
import time

# Run Time States retuned by 
RUNTIME_STATUS_IDLE = 0
RUNTIME_STATUS_RUNNING = 1
RUNTIME_STATUS_PAUSED = 2

GRAVITY = 9.8

class SequenceClient:

    def __init__(self, ros, ns):
        self._ros = ros
        self._ns = ns
        self.runtime_status = 0

        self._upload_service = roslibpy.Service(self._ros, f"{self._ns}/upload", "commander_msgs/Upload")
        self._start_service = roslibpy.Service(self._ros, f"{self._ns}/start", "commander_msgs/RunSequence")
        self._stop_service = roslibpy.Service(self._ros, f"{self._ns}/stop", "std_srvs/Trigger")
        self._pause_service = roslibpy.Service(self._ros, f"{self._ns}/pause", "std_srvs/Trigger")
        self._step_service = roslibpy.Service(self._ros, f"{self._ns}/step", "std_srvs/Trigger")
        self._debug_service = roslibpy.Service(self._ros, f"{self._ns}/debug", "std_srvs/Trigger")
        self._runTimeState_client = roslibpy.Topic(self._ros, '/sequence/runtime_state', '/commander_msgs/RuntimeState')
        self._runTimeState_client.subscribe (self.status_update) 

    def status_update( self, message):
        self.runtime_status = message['state']

    def get_status(self):   # "commander_msgs/RuntimeState"
        return self.runtime_status

    def is_running(self):   # "commander_msgs/RuntimeState"
        return (self.runtime_status == RUNTIME_STATUS_RUNNING)

    def is_idle(self):   # "commander_msgs/RuntimeState"
        return (self.runtime_status == RUNTIME_STATUS_IDLE)

    def wait_until_idle(self):
        while (self.is_running()): 
            time.sleep(0.1)
            
    def upload(self, blockly_xml):
        request = roslibpy.ServiceRequest({"blockly": blockly_xml})
        result = self._upload_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to upload blockly: {result['message']}")

    def start(self):
        request = roslibpy.ServiceRequest()
        result = self._start_service.call(request)
        if result['success']:
            self.runtime_status = RUNTIME_STATUS_RUNNING
        else:
            raise Exception(f"Unable to start the sequence: {result['message']}")

    def call_function(self, function_name):
        request = roslibpy.ServiceRequest({"procedure_name" : function_name})
        result = self._start_service.call(request)
        if result['success']:
            self.runtime_status = RUNTIME_STATUS_RUNNING
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
