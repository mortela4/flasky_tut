"""
@file sensor_types.py
@brief Sensor classes specific to bus-types.
"""


class SensorHelper(object):
    def get_info(self):
        # First - get BASE sensor properties (common to ALL sensors):
        self.base.get_info()
        # Then - get DEVICE-SPECIFIC properties, (possibly) unique to the given sensor type(I2C/SPI/UART):
        for sensor_prop, prop_value in self.__dict__.items():
            if sensor_prop != 'base' and sensor_prop != 'type_name':
                print("Sensor property %s = %s" % (sensor_prop, prop_value))


# Bus-specific sensor classes ...
class I2cSensor(SensorHelper):

    def __init__(self, sensor_base=None, i2c_addr=None, clk_speed=100000):
        print("Creating a I2C sensor ...")
        if sensor_base is None:
            print("ERROR: 'sensor_base' NOT given!")
        else:
            self.base = sensor_base
        self.i2c_addr = i2c_addr
        self.clk_speed = clk_speed   # default unless specified
        # Configure/Initialize sensor if needed:
        self.get_info()


class SpiSensor(SensorHelper):

    def __init__(self, sensor_base=None, cs_no=None, clk_speed=100000):
        print("Creating a SPI sensor ...")
        if sensor_base is None:
            print("ERROR: 'sensor_base' NOT given!")
        else:
            self.base = sensor_base
        self.cs_no = None
        self.spi_mode = 0
        self.data_bits = 8       # default unless specified
        self.clk_speed = 100000  # default unless specified
        self.msb_first = True    # default unless specified
        self.cs_toggle = True    # default unless specified
        self.cycles_before = 0   # default unless specified
        self.cycles_after = 0    # default unless specified
        # Configure/Initialize sensor if needed:
        self.get_info()


class UartSensor(SensorHelper):

    def __init__(self, sensor_base=None, baud_rate=None):
        print("Creating a UART sensor ...")
        if sensor_base is None:
            print("ERROR: 'sensor_base' NOT given!")
        else:
            self.base = sensor_base
        self.baud_rate = baud_rate
        self.data_bits = 8   # default unless specified
        self.parity = False  # default unless specified
        self.stop_bits = 1   # default unless specified
        # Configure/Initialize sensor if needed:
        self.get_info()


sensor_type_map = {"i2c": I2cSensor, "spi": SpiSensor, "uart": UartSensor}
