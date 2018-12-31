"""
@file sensor_app.py

@brief Sensor-config web-app using Flask.
"""

import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

# Local imports:
from sensor_classes.sensor_base import SensorBase
from sensor_classes.sensor_types import I2cSensor, SpiSensor, UartSensor, sensor_type_map


# Choose UI:
# FRONT_PAGE = "add_sensor.html"
# FRONT_PAGE = "sensors_page.html"
FRONT_PAGE = "sensors_table_page.html"


app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))

sensor_dev_name = None
sensor_alias = None
sensor_interface = None
sensors = []


@app.route('/interface', methods=["GET", "POST"])
def interface():
    global sensor_dev_name
    global sensor_alias
    global sensor_interface
    global sensors
    #
    interface_map = {"spi": "spi_config.html", "i2c": "i2c_config.html", "uart": "uart_config.html"}
    #
    print("'interface()' called with interface='%s' selected ..." % sensor_interface)
    if sensor_interface is None:
        print("ERROR: no interface selected for sensor!")
        return redirect("/")
    #
    if request.form:
        try:
            bus_num = int(request.form.get("bus_num"))
            print("Creating sensor base with dev=%s, bus no=%d, interface=%s and alias=%s" %
                  (sensor_dev_name, bus_num, sensor_interface, sensor_alias))
            sensor_base = SensorBase(type_name=sensor_interface, bus_no=bus_num,
                                     dev_name=sensor_dev_name, alias=sensor_alias)

            # Need to handle each interface-form specifically:
            if sensor_interface == "i2c":
                i2c_addr = int(request.form.get("i2c_addr"))
                if i2c_addr > 127 or i2c_addr < 1:
                    print("INPUT ERROR: I2C-address must be in range 1-->127! Value: %s" % i2c_addr)
                clk_speed = int(request.form.get("clk_speed"))
                sensor = I2cSensor(sensor_base=sensor_base, i2c_addr=i2c_addr, clk_speed=clk_speed)
            #
            elif sensor_interface == "spi":
                cs_num = int(request.form.get("cs_num"))
                clk_speed = int(request.form.get("clk_speed"))
                sensor = SpiSensor(sensor_base=sensor_base, cs_no=cs_num, clk_speed=clk_speed)
            #
            elif sensor_interface == "uart":
                baud_rate = int(request.form.get("baud_rate"))
                sensor = UartSensor(sensor_base=sensor_base, baud_rate=baud_rate)
            #
            else:
                print("ERROR: incorrect INTERFACE specified: '%s'" % sensor_interface)
                sensor = None
            # INFO:
            if sensor is None:
                print("Sensor Creation ERROR!")
            else:
                sensors.append(sensor)
                print("DEBUG: total of %d sensors stored ..." % len(sensors))
            #
            return redirect("/")
        except Exception as e:
            print("Failed to create sensor!")
            print(e)
            return redirect("/")
    #
    return render_template(interface_map[sensor_interface])    # Change to other HTML input page if needed ...


@app.route('/config', methods=["GET", "POST"])
def config():
    global sensor_dev_name
    global sensor_alias
    global sensor_interface
    #
    page_map = {"sht711": "sht711_config.html",
                "bma280": "bma280_config.html",
                "custom-1": "custom1_config.html",
                "tmp82": "tmp82_config.html"}
    #
    print("'Config()' called with device='%s' selected ..." % sensor_dev_name)
    if sensor_dev_name is None:
        print("ERROR: no sensor-device selected!")
        return
    if request.form:
        try:
            sensor_alias = request.form.get("alias")
            sensor_dev_name = request.form.get("name")
            sensor_interface = request.form.get("type_name")
            print("Chosen interface: ", sensor_interface)
            #
            return redirect("/interface")
        except Exception as e:
            print("Failed to create sensor!")
            print(e)
    return render_template(page_map[sensor_dev_name])    # Change to other HTML input page if needed ...


@app.route('/', methods=["GET", "POST"])
def home():
    global sensor_dev_name
    global sensors
    #
    if request.form:
        try:
            sensor_dev_name = request.form.get("name")
            print("Sensor device %s selected - now configuring ..." % sensor_dev_name)
            return redirect("/config")
        except Exception as e:
            print("Failed to add sensor!")
            print(e)
    return render_template(FRONT_PAGE, sensor_list=sensors)    # Change to other HTML input page if needed ...


if __name__ == '__main__':
    # For test/debug only:
    bs1 = SensorBase(type_name="spi", bus_no=0, dev_name="tmp82", alias="TempSense-1A")
    ts1 = SpiSensor(sensor_base=bs1, cs_no=2, clk_speed=100000)
    sensors.append(ts1)
    bs2 = SensorBase(type_name="i2c", bus_no=1, dev_name="sht711", alias="RHT-Sense-2C")
    ts2 = I2cSensor(sensor_base=bs2, i2c_addr=28, clk_speed=100000)
    sensors.append(ts2)
    bs3 = SensorBase(type_name="uart", bus_no=5, dev_name="custom-1", alias="Custom-IMU-1")
    ts3 = UartSensor(sensor_base=bs3, baud_rate=19200)
    sensors.append(ts3)
    #
    app.run(debug=True, port=5000)
