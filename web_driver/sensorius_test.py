import random
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


webdriver_wait = None
use_animation = True
sensors = {'sensor_1': {'type': 'sht711', 'iface': 'i2c', 'bnum': '2', 'addr': 78},
           'sensor_2': {'type': 'bma280', 'iface': 'spi', 'bnum': '1', 'cs_num': '6'},
           'sensor_3': {'type': 'tmp82', 'iface': 'i2c', 'bnum': '0', 'addr': 81},
           'sensor_4': {'type': 'custom-1', 'iface': 'uart', 'bnum': '8', 'baud_rate': '38400'}}
config_title = {'sht711': 'SHT711 Config',
                'tmp82': 'TMP82 Config',
                'bma280': 'BMA280 Config',
                'custom-1': 'Custom-1 Config'
                }
iface_title = {'i2c': 'I2C Configuration',
                'spi': 'SPI Configuration',
                'uart': 'UART Configuration'}


def pause(wait=use_animation, time_out=1.0):
    """ Helps to see (visually) what happens when manipulating browser UI. """
    if wait:
        time.sleep(time_out)


def wait_on_redirect(title_name=None):
    global webdriver_wait
    if title_name is not None:
        webdriver_wait.until(EC.title_is(title_name))


def select_sensor(web_drv=None, sdata=None):
    """ Entry page requires a sensor-type to be selected from drop-down menu. """
    sensor_type = sdata['type']
    select = Select(web_drv.find_element_by_name('name'))
    # select by visible text:
    # select.select_by_visible_text('BMA280')
    # select by value:
    select.select_by_value(sensor_type)
    pause()
    web_drv.find_element_by_name('sensor-config').click()


def config_sensor(web_drv=None, sname=None, sdata=None):
    """ Config-page requires a) an alias to be given, and b) an interface to be selected. """
    dev_type = sdata['type']
    config_page_title = config_title[dev_type]
    print("Waiting for page titled '%s' to load ..." % config_page_title)
    wait_on_redirect(config_page_title)
    # Set alias:
    web_drv.find_element_by_name('alias').send_keys(sname)
    pause()
    # Set interface:
    iface = sdata['iface']
    select = Select(web_drv.find_element_by_name('type_name'))
    # select by value:
    select.select_by_value(iface)
    pause()
    # web_drv.find_element_by_class_name('submit').click()
    web_drv.find_element_by_name('iface-config').click()


def config_iface(web_drv=None, sdata=None):
    """
    Interface configuration requires minimum one value to be set:
    1) I2C : bus-address
    2) SPI: CS-number
    3) UART: COM/TTY-port number
    """
    iface_type = sdata['iface']
    iface_page_title = iface_title[iface_type]
    print("Waiting for page titled '%s' to load ..." % iface_page_title)
    wait_on_redirect(iface_page_title)
    #
    if iface_type == 'i2c':
        i2c_address = sdata['addr']
        web_drv.find_element_by_name('i2c_addr').send_keys(i2c_address)
        pause()
    elif iface_type == 'spi':
        cs_num = sdata['cs_num']
        select = Select(web_drv.find_element_by_name('cs_num'))
        select.select_by_value(cs_num)
        pause()
    elif iface_type == 'uart':
        brate = sdata['baud_rate']
        select = Select(web_drv.find_element_by_name('baud_rate'))
        select.select_by_value(brate)
        pause()
    else:
        print("ERROR: cannot interpret interface-type '%s'!!" % iface_type)
    # web_drv.find_element_by_class_name('submit').click()
    web_drv.find_element_by_name('add-sensor').click()



# *************** TEST-LOOP **************************
if __name__ == "__main__":
    print("Starting test ...")

    d = webdriver.Chrome()
    webdriver_wait = WebDriverWait(d, 10)  # Wait up to 10sec for page load to complete.
    d.get('http://localhost:5000/')

    for sensor_name, sensor_data in sensors.items():
        #
        select_sensor(d, sensor_data)
        config_sensor(d, sensor_name, sensor_data)
        config_iface(d, sensor_data)
        #
        wait_on_redirect('Sensor Creator Page')
        pause(3.0)

    pause(time_out=10.0)
    d.close()

    print("Test finished!")
