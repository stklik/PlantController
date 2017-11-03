# PlantController

This repo uses [Chirp-rpi](https://github.com/ageir/chirp-rpi) and [Yoctopuce YoctoLib](https://github.com/yoctopuce/yoctolib_python) to create a controller that regularly reads the Yoctopuce and Chirp sensors.

The values are sent to Adafruit-IO using its [python client](https://github.com/adafruit/io-client-python).

This is a very simple client that only forwards data to Adafruit-IO. There is no possibility to directly speak to the controller.


## Todo
- [ ] write a server with a nice API so we can talk directly
- [ ] create a way to interact with the relay (through Adafruit and local)
- [ ] actually make this a real thing


---

Things to consider when running on a new RPi:
* I2C needs to be enabled (in `raspi-config`)
* don't forget to calibrate the Chirps
* `smbus` is needed - consider this when using virtualenv (installed via `apt-get python-smbus`)
* enable yoctopuce to use usb. For this create a file (e.g. `99-yoctopuce-all.rules`) within `/etc/udev/rules.d`. File-content:
```
# udev rules to allow write access to all users for Yoctopuce USB devices
SUBSYSTEM=="usb", ATTR{idVendor}=="24e0", MODE="0666"
```
(credit to [stackmagic](https://github.com/stackmagic)'s [collectd-yoctopuce](https://github.com/stackmagic/collectd-yoctopuce) for providing me with a
* don't forget to change the Adafruit API key in `config.yaml`
