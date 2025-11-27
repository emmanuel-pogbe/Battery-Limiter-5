# Copyright (c) 2009, Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.


#Understanding battery parameters

"""Show battery information.

$ python3 scripts/battery.py
charge:     74%
left:       2:11:31
status:     discharging
plugged in: no
"""

import sys
import psutil

def secs2hours(secs):
    mm, ss = divmod(secs, 60)
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


if __name__ == '__main__':
    getBatteryStatus()