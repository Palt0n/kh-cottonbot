import os
import psutil


def get_EnvironmentVariable(variable):
    return os.environ.get(variable)

    
import psutil

class ClassPC:
    def __init__(self):
        pass

    def get_battery(self):
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = str(battery.percent)
        if plugged is False:
            plugged = "Not Plugged In"
        else: 
            plugged="Plugged In"
        return percent+'% | '+plugged
    