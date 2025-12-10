# Background thread that monitors battery

import psutil
def checkBatteryHealth():
    batt = psutil.sensors_battery()
    return batt #batt.percent, batt.secsleft, batt.power_plugged
    #example output
    # sbattery(percent=84, secsleft=4294967295, power_plugged=False)
    #type: <class 'psutil._common.sbattery'>
if __name__ == "__main__":
    print(checkBatteryHealth())