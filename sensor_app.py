"""
@file sensor_app.py

@brief Sensor-config web-app using Flask.
"""

import os
import uuid

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request


app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))

sensor_dev_name = None
sensors = []


class Sensor(object):

    def __init__(self, alias=None, name=None, type_name=None):
        self.name = name
        self.type_name = type_name
        self.alias = alias
        uuid_val = uuid.uuid4()
        self.id = str(uuid_val.hex)     # Store UUIDs as plain (hex-)string --> get (BIG)INT-value as 'int(self.id, 16)'
        # Debug:
        print("Created sensor: id=%s, alias=%s, type=%s, device=%s" % (self.id, self.alias, self.type_name, self.name))

    def __repr__(self):
        return '<ID %r><Name %r><Alias %r><Type %r>' % (self.id, self.name, self.alias, self.type_name)


@app.route('/config', methods=["GET", "POST"])
def config():
    global sensor_dev_name
    #
    page_map = {"sht711": "sht711_config.html",
                "bma280": "bma280_config.html",
                "custom-1": "custom1_config.html"}
    #
    print("'Config()' called with device='%s' selected ..." % sensor_dev_name)
    if sensor_dev_name is None:
        print("ERROR: no sensor-device selected!")
        return
    if request.form:
        try:
            sensor = Sensor(alias=request.form.get("alias"), name=request.form.get("name"),
                            type_name=request.form.get("type_name"))
            #
            sensors.append(sensor)
            #
            return redirect("/")
        except Exception as e:
            print("Failed to create sensor!")
            print(e)
    return render_template(page_map[sensor_dev_name])    # Change to other HTML input page if needed ...


@app.route('/', methods=["GET", "POST"])
def home():
    global sensor_dev_name
    #
    if request.form:
        try:
            sensor_dev_name = request.form.get("name")
            print("Sensor device %s selected - now configuring ..." % sensor_dev_name)
            return redirect("/config")
        except Exception as e:
            print("Failed to add sensor!")
            print(e)
    return render_template("add_sensor.html")    # Change to other HTML input page if needed ...


if __name__ == '__main__':
    app.run(debug=True, port=5000)
