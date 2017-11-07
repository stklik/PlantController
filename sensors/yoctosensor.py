import logging

from sensors.sensor import Sensor
from yoctopuce.yocto_api import *
from yoctopuce.yocto_lightsensor import YLightSensor
from yoctopuce.yocto_humidity import YHumidity
from yoctopuce.yocto_temperature import YTemperature
from yoctopuce.yocto_pressure import YPressure
from yoctopuce.yocto_rangefinder import YRangeFinder
from yoctopuce.yocto_relay import YRelay

class YoctoSensor(Sensor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Setup the API to use local USB devices
        errmsg = YRefParam()
        if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
            print("YoctoAPI.RegisterHub init error" + errmsg.value)
        self.channel = kwargs.get("channel", "")
        self.init_sensor()
        if not self.sensor.isOnline():
            logging.error('Device %s (Sensor-id: %s) not connected', self.name, self.sensor_id)
        else:
            logging.info('Device %s (Sensor-id: %s) connected', self.name, self.sensor_id)

    def ready(self):
        return self.sensor.isOnline()

    def measure(self):
        if not self.ready():
            logging.debug('Device %s not connected' % self.sensor_id)
            return None
        else:
            return self.sensor.get_currentValue()
    
    def sleep(self, interval):
        YAPI.Sleep(interval * 1000)

class YoctoHumidity(YoctoSensor):
    def init_sensor(self):
        self.sensor = YHumidity.FindHumidity(self.sensor_id + self.channel)

class YoctoPressure(YoctoSensor):
    def init_sensor(self):
        self.sensor = YPressure.FindPressure(self.sensor_id + self.channel)

class YoctoTemperature(YoctoSensor):
    def init_sensor(self):
        self.sensor = YTemperature.FindTemperature(self.sensor_id + self.channel)

class YoctoLight(YoctoSensor):
    def init_sensor(self):
        self.sensor = YLightSensor.FindLightSensor(self.sensor_id + self.channel)

class YoctoRangeFinder(YoctoSensor):
    def init_sensor(self):
        self.sensor = YRangeFinder.FindRangeFinder(self.sensor_id +  self.channel)

class YoctoRelay(YoctoSensor):
    def init_sensor(self):
        self.sensor = YRelay.FindRelay(self.sensor_id + self.channel)

    def measure(self):
        if not self.ready():
            logging.debug('Relay %s%s not connected', self.sensor_id, self.channel)
            return None
        else:
            logging.debug("Relay %s%s reading data", self.sensor_id, self.channel)
            return self.sensor.get_state()

    def write(self, value):
        logging.debug("Writing %s to sensor %s%s", value, self.sensor_id, self.channel)
        if self.ready():
            if value in [0, False, "false", "False", "FALSE", "OFF", "Off", "off", "0"]:
                self.sensor.set_state(YRelay.OUTPUT_OFF)
            else:
                self.sensor.set_state(YRelay.OUTPUT_ON)

    def send_data(self, value=None):
        if type(value) == bool:
            value = 1 if value else 0
        super().send_data(value)
