"""
A little tool that helps finding and identifying Yocto devices.

Disclaimer: Works for me, maybe it doesn't for you.
"""


import sys
from yoctopuce.yocto_api import *

usage = """Usage:

{0} usage \t\t\t to print this message
{0} devices \t\t\t to list all devices connected via usb
{0} identify <device-identifier> \t to make one device blink for 5 seconds
""".format(sys.argv[0])

def main(*args):
    if args[0] == "usage":
        print(usage)
    elif args[0] == "devices":
        list_devices()
    elif args[0] == "identify":
        identify_device(args[1])
    else:
        raise Exception("Unidentified option '%s'" % args[0])

def list_devices():
    errmsg = YRefParam()
    # Setup the API to use local USB devices
    if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
        raise YoctoException("init error" + str(errmsg))

    print("PRODUCT NAME \t\t", "SERIAL NUMBER \t\t", "LOGICAL NAME \t\t")
    module = YModule.FirstModule()
    while module is not None:
        print(module.get_productName() + "\t\t", module.get_serialNumber() + "\t\t", module.get_logicalName() + "\t\t")
        module = module.nextModule()
    YAPI.FreeAPI()

def identify_device(name):
    errmsg = YRefParam()
    # Setup the API to use local USB devices
    if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
        raise YoctoException("init error" + str(errmsg))

    module = YModule.FindModule(name)
    if not module.isOnline():
        print("Couldn't find device ", name)
    else:
        print("Found ", name, " - blinking for 10 seconds")
        module.set_beacon(YModule.BEACON_ON)
        YAPI.Sleep(10*1000)
        module.set_beacon(YModule.BEACON_OFF)
        print("Stopped blinking. Bye.")

    YAPI.FreeAPI()


class YoctoException(Exception):
    pass

if __name__ == "__main__":
    try:
        main(*sys.argv[1:])
    except YoctoException as e:
        print("There was a problem with your command")
        print(e)
    except Exception as e:
        print("There was a problem with your command")
        print(e)
        print("")
        print(usage)
