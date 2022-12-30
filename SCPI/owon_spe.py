from instrument import Instrument

class OWON_SPE(Instrument):
    """
        * IDN Return Format
        OWON,<model>,<serial number>,FV:X.XX.XX
        <model>：the model number of the instrument.
        <serial number>：the serial number of the instrument.
        FV:X.XX.XX：the software version of the instrument.        

        https://www.owon.com.hk/download.asp?category=Power%20Supply&series=P4000,SP,SPE%20Series&model=&SortTag=User%20Manual
        https://www.owon.com.hk/download.asp?category=Power%20Supply&series=P4000,SP,SPE%20Series&model=&SortTag=Application
        https://www.owon.com.hk/download.asp?category=Power%20Supply&series=P4000,SP,SPE%20Series&model=&SortTag=Software
        https://www.owon.com.hk/download.asp?category=Power%20Supply&series=P4000,SP,SPE%20Series&model=&SortTag=Latest%20Firmware
    """
    def __init__(self):
        super(OWON_SPE, self).__init__()

    def measure_voltage(self)->float:
        return self.send_command("MEAS:VOLT?")

    def measure_current(self)->float:
        return self.send_command("MEAS:CURR?")

    def measure_power(self)->float:
        return self.send_command("MEAS:POW?")

    #todo implement this correctly
    def measure(self)->tuple(float,float,float):
        return self.send_command("MEAS:ALL?")

    def is_on(self) -> bool:
        return self.output


    @property
    def output(self)->bool:
        if self.is_connected():
            return bool(self.send_command(f"OUTP?"))

        return False
    

    @output.setter
    def output(self, value:bool):
        self.send_command(f"OUTP {value}")
        

    @property
    def current(self)->float:
        if self.is_connected():
            return float(self.send_command(f"CURR?"))

        return 0.0
    
    @current.setter
    def current(self, value:float):
        if self.is_connected():
            self.send_command(f"CURR {value}")


    @property
    def voltage(self)->float:
        if self.is_connected():
            return float(self.send_command(f"VOLT?"))

        return 0.0
    

    @voltage.setter
    def voltage(self, value:float)->float:
        if not self.is_connected():
            return 0.0

        return self.send_command(f"VOLT {value}")

    @property
    def limit_current(self)->float:
        if self.is_connected():
            return float(self.send_command(f"CURR:LIM?"))
        return 0.0
    
    @limit_current.setter
    def limit_current(self, value:float):
        if self.is_connected():
            return self.send_command(f"CURR:LIM {value}") 


    @property
    def limit_voltage(self)->float:
        if self.is_connected():
            return float(self.send_command(f"VOLT:LIM?"))
        return 0.0
    

    @limit_voltage.setter
    def limit_voltage(self, value:float):
        if self.is_connected():
            return self.send_command(f"VOLT:LIM {value}")

    def local(self)->bool:
        self.send_command("SYST:LOCAL") 

    def local(self)->bool:
        self.send_command("SYST:REMOTE") 