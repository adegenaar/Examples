import pyvisa   # for SCPI
#import pyusb

class Instrument():
    def __init__(self, delay = 0.001):
        self.id = ""
        self.rm = pyvisa.ResourceManager()
        #rm.list_resources()
        self.connection = None
        self.delay = delay
        #inst.read_termination = '\r\n'
        #inst.write_termination = '\r\n'

    def is_connected(self)->bool:
        return self.connection is not None

    def connect(self, address: str):
        if not self.is_connected():
            self.connection = self.rm.open_resource(address)
        self.connection.query_delay = self.delay
    
    def disconnect(self):
        self.connection.close()

    def send_command(self, command: str):
        if not self.is_connected():
            return ""
        
        results = self.connection.send(command)
        #err = self.connection
        return results

    def idn(self)->str:
        if self.id is None:
            self.id=self.query("*IDN?")

        return self.id

    def reset(self):
        self.send_command("*RST")

    