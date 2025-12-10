# Decides when to show/hide notifications
import battery_monitor

def is_bad_health(MIN: int, MAX: int):
    batt = battery_monitor.checkBatteryHealth()
    status = 0
    is_healthy = True
    if batt.percent < MIN and batt.power_plugged == False:
        status = -1
        is_healthy = False
    if batt.percent > MAX and batt.power_plugged == True:
        status = 1
        is_healthy = False
    #Status meanings
    # 0 means healthy 
    # 1 means battery higher than set max value
    # -1 means battery lower than set min value
    return [is_healthy,status]