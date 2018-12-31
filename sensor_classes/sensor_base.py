import uuid


class SensorBase:
    """
    Base sensor class no.1 (external sensors, connected to a bus)
    """
    # bus_property1 = {"i2c": "bus-address", "spi": "ChipSelect-number", "uart": "baud_rate"}

    def __init__(self, type_name=None, bus_no=None, dev_name=None, alias=None):
        #
        self.uuid = uuid.uuid4()     # TODO: assess - should UUID creation happen first when a new sensor is accepted?
        self.type_name = type_name
        self.bus_no = bus_no
        if dev_name:
            self.dev_name = dev_name
        else:
            self.dev_name = "none"
        #
        if alias:
            self.alias = alias
        else:
            self.alias = "none"

    def __repr__(self):
        return '<ID %r><Name %r><Alias %r><Type %r>' % (self.uuid, self.dev_name, self.alias, self.type_name)

    def get_info(self):
        if self.type_name is None:
            print("Unknown sensor type - cannot show info!")
            return
        # INFO:
        bus_type_name = self.type_name.upper()
        print("%s-sensor properties:" % bus_type_name)
        print("---------------------")
        print("%s-interface no: %d" % (bus_type_name, self.bus_no))
        print("%s connected device: %s" % (bus_type_name, self.dev_name))
        print("%s sensor alias: %s" % (bus_type_name, self.alias))
        print("%s sensor UUID: %s" % (bus_type_name, self.uuid))
        print("Bus-specific properties:")