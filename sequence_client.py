import roslibpy

class SequenceClient:
    def __init__(self, ros, ns):
        self._ros = ros
        self._ns = ns

        self._upload_service = roslibpy.Service(self._ros, f"{self._ns}/upload", "commander_msgs/Upload")
        self._start_service = roslibpy.Service(self._ros, f"{self._ns}/start", "commander_msgs/RunSequence")
        self._stop_service = roslibpy.Service(self._ros, f"{self._ns}/stop", "std_srvs/Trigger")
        self._pause_service = roslibpy.Service(self._ros, f"{self._ns}/pause", "std_srvs/Trigger")
        self._step_service = roslibpy.Service(self._ros, f"{self._ns}/step", "std_srvs/Trigger")
        self._debug_service = roslibpy.Service(self._ros, f"{self._ns}/debug", "std_srvs/Trigger")

    def upload(self, blockly_xml):
        request = roslibpy.ServiceRequest({"blockly": blockly_xml})
        result = self._upload_service.call(request)
        if not result['success']:
            raise Exception(f"Unable to upload blockly: {result['message']}")

    def start(self):
        request = roslibpy.ServiceRequest()
        result = self._start_service.call(request)
        if not result['success']:
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
