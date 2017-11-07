import time
import logging
from threading import Thread

class Sensor(Thread):

    def __init__(self, name="", sensor_id="", feedname=None, interval=60, client=None, *args, **kwargs):
        Thread.__init__(self)
        self.name = name
        self.client = client
        self.sensor_id = sensor_id
        self.feedname = feedname
        self.interval = interval

    def send_data(self, value=None):
        if self.client:
            logging.debug("Sending sensordata (%s) to feed %s : Value = %s", self.sensor_id, self.feedname, value)
            try:
                self.client.publish(self.feedname, value)
            except:
                logging.error("Error when sending value %s (type: %s) to feed %s", value, type(value), self.feedname, exc_info=True)
        else:
            logging.debug("No client configured - sensor %s read value: %s", self.feedname, value)

    def stop(self):
        logging.info("Stopping %s", self.sensorname)
        self.stopper = True

    def run(self):
        self.stopper = False
        while not self.stopper:
            new_value = self.measure()
            if new_value != None: # only if we have a value
                self.send_data(new_value)

            # sleep
            self.sleep(self.interval)

    def sleep(self, interval):
        """use this intermediate step so we can implement the YOCTO sleep method"""
        time.sleep(interval)
