import time
import logging
from threading import Thread

class Sensor(object):

    def __init__(self, name="", sensor_id="", feedname=None, interval=60, client=None, *args, **kwargs):
        self.name = name
        self.client = client
        self.sensor_id = sensor_id
        self.feedname = feedname
        self.interval = interval

    def send_data(self, value=None):
        if value == None: # early exit
            return
        if self.client:
            logging.debug("Sending sensordata (%s) to feed %s : Value = %s", self.sensor_id, self.feedname, value)
            self.client.send(self.feedname, value)
        else:
            logging.debug("No client configured - sensor %s read value: %s", self.feedname, value)
