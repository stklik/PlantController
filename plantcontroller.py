import sys
import yaml
import logging
from Adafruit_IO import Client
from sensors.yoctosensor import *
from sensors.chirpsensor import ChirpSensor

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# shut up urllib (called in Adafruit_IO)
logging.getLogger("urllib3").setLevel(logging.INFO)

type_to_class = {
    "yocto-temperature" : YoctoTemperature,
    "yocto-humidity" : YoctoHumidity,
    "yocto-pressure" : YoctoPressure,
    "yocto-light" : YoctoLight,
    "yocto-distance" : YoctoRangeFinder,
    "yocto-relay" : YoctoRelay
}

def get_config():
    config = None
    with open("config.yaml", "r") as configfile:
        config = yaml.load(configfile)
        return config

def configure_chirp(name, config, namespace="", client=None):
    logging.debug("Registering Chirp %s", name)
    obj = ChirpSensor(
        name=name,
        sensor_id=config["sensor-id"],
        feedname="{}---{}".format(namespace, name),
        interval=config["polling-interval"],
        client=client,
        min_moist=config["calibration"]["min-moist"],
        max_moist=config["calibration"]["max-moist"],
        measurements = config["measurements"]
    )
    obj.start()

def configure_yocto(name, config, namespace="", client=None):
    logging.debug("Registering Yocto %s", name)
    if "measurements" in config:
        for measurement, m_config in config["measurements"].items():
            logging.debug("Registering measurement %s on Yocto %s", measurement, name)
            m_type = m_config["type"]
            m_channel = m_config["channel"]
            klass = type_to_class.get(m_type, None)
            if klass:
                obj = klass(
                    name=name,
                    sensor_id=config["sensor-id"],
                    feedname="{}---{}-{}".format(namespace, name, measurement),
                    interval=config["polling-interval"],
                    channel=m_channel,
                    client=client
                )
                if obj.sensor.isOnline():
                    logging.info("Starting thread for sensor %s on device %s", measurement, name)
                    obj.start()
                else:
                    logging.error("Sensor %s on device %s is not online. Not starting measurements.", measurement, name)
            else:
                logging.warn("Couldn't find correct measurement-class for type: %s", m_type, exc_info=True)
    else:
        logging.warn("No measurements defined on Yocto %s", name)
        print(config)
        sys.exit(0)


def main():
    config = get_config()
    api_key = config["adafruit-io-key"]
    logging.info("Starting an Adafruit client with API-Key %s", api_key)
    client = Client(api_key)
    
    sensor_namespace = config["namespace"]
    
    for dev_name, device_config in config["devices"].items():
        if "active" in  device_config and device_config["active"]:
            dev_type = device_config["type"]
            if dev_type == "chirp":
                try:
                    configure_chirp(dev_name, device_config, sensor_namespace, client)
                except:
                    logging.error("There was an exception when registering chirp device %s", dev_name, exc_info=True)
            elif dev_type.startswith("yocto"):
                try:
                    configure_yocto(dev_name, device_config, sensor_namespace, client)
                except:
                    logging.error("There was an exception when registering generic device %s", dev_name, exc_info=True)
            else:
                logging.error("Unknown device type %s (device: %s)", dev_type, dev_name)
        else:
            logging.info("Skipping device %s because it is not active", dev_name)
            continue
    logging.info("------- Registered all devices -------")

if __name__ == "__main__":
    main()
