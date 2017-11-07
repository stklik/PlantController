import logging
from sensors.sensor import Sensor

try:
    from lib.chirp.chirp import Chirp
except ModuleNotFoundError:
    logging.error("Error when importing Chirp. Check whether you're on the RPi")

class ChirpSensor(Sensor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.measurements = kwargs["measurements"]
        try:
            self.sensor = Chirp(
                address=kwargs["sensor_id"],
                read_moist=True,
                read_temp=True,
                read_light=False,
                min_moist=kwargs.get("min_moist", False),
                max_moist=kwargs.get("max_moist", False),
                temp_scale='celsius',
                temp_offset=0
                )
        except NameError:
            logging.error("Couldn't init Chirp %s - class Chirp is not available.", self.sensor_id)
            self.sensor = None

    def ready(self):
        return self.sensor != None

    def measure(self):
        if not self.sensor:
            logging.warn('Device %s not connected' % self.sensor_id)
            return None
        else:
            self.sensor.trigger()
            return {
                "chirp-moist" : self.sensor.moist,
                "chirp-moist-percent": self.sensor.moist_percent,
                "chirp-temperature" : self.sensor.temp
            }

    def send_data(self, value=None):
        for name, config in self.measurements.items():
            feedname = self.feedname + "-" + name
            val = value[config]
            if self.client:
                logging.debug("Sending sensordata (%s) to feed %s : Value = %s", self.sensor_id, feedname, val)
                self.client.send(feedname, val)
            else:
                logging.debug("No client configured - sensor %s read value %s", feedname, val)
