#! /usr/bin/env python3
import sys
sys.path.append('/home/amigos/ros/src/rx_pci_single_ros/scripts/')
import stop_logger as log
import nasco_sisbb_controller as ctrl


initial_voltage = 0 # mV
final_voltage = 7 # mV
step = 0.1 # mV
roop = int((final_voltage - initial_voltage) / step)

for i in range(roop+1):
    ctrl.nasco_sisbb_set_voltage(ch=1, voltage=i*step, interval=1)
    ctrl.nasco_sisbb_set_voltage(ch=2, voltage=i*step, interval=1)

log.stop_logger()    

