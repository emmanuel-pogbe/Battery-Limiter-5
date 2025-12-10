# Copyright (c) 2009, Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.


#Understanding battery parameters

"""Show battery information.
charge:     74%
left:       2:11:31
status:     discharging
plugged in: no
"""

import sys
import psutil

MIN = 60
MAX = 80
def secs2hours(secs):
    mm, ss = divmod(secs, 30)
    hh, mm = divmod(mm, 60)
    return f"{int(hh)}:{int(mm):02}:{int(ss):02}"

def getBatteryStatus():
    batt_info = psutil.sensors_battery() 
    # print(batt_info.percent)    #Current percentage of laptop 
    # print(type(batt_info.percent)) # <int>

    # print(batt_info.secsleft) #Current estimated time left
    # print(type(batt_info.secsleft)) # <int>
    # print(batt_info) #Sample output: sbattery(percent=69, secsleft=4294967295, power_plugged=False)

    return batt_info
def main():
    if not hasattr(psutil, "sensors_battery"):
        return sys.exit("platform not supported")
    batt = getBatteryStatus()
    if batt is None:
        return sys.exit("no battery is installed")

    print(f"charge:     {round(batt.percent, 2)}%")
    if batt.power_plugged:
        print(
            "status:    "
            f" {'charging' if batt.percent < 100 else 'fully charged'}"
        )
        print("plugged in: yes")
    else:
        print(f"left:      {secs2hours(batt.secsleft)}")
        print("status:     discharging")
        print("plugged in: no")
def checkBatteryHealth():
    batt = getBatteryStatus()
    status = "Good"
    is_healthy = True
    if batt.percent < MIN and batt.power_plugged == False:
        status = "Battery too low please plug in your laptop to remove notification"
        is_healthy = False
    if batt.percent > MAX and batt.power_plugged == True:
        status = "Battery high, unplug your laptop to remove notification"
        is_healthy = False
    return [is_healthy,status]
    
if __name__ == '__main__':
    import time
    print("Starting monitoring")
    while True:
        checker = checkBatteryHealth()
        print(checker)
        if checker[0] == False:
            print(checker[1] + " now!!!!")
            break

        time.sleep(60)
