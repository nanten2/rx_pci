#!/usr/bin/env python3
import sys
import time
sys.path.append('/home/amigos/ros/src/rx_pci_single_ros/scripts')
import sisbb_controller as ctrl
import rospy
from rx_pci_single_ros import logger_high_flag_msg

tname = 'save_controller'
pub = rospy.Publisher(tname, logger_high_flag_msg, queue_size=1)

msg = logger_high_flag_msg()
msg.timestamp = str(time.time())
time.sleep(0.1)
print(msg)
pub.publish(msg)

initial_voltage = 0.
final_voltage = 7.
step = 0.1
interval = 2
roop = int((final_voltage - initial_voltage) / step)

for i in range(roop+1):
    ctrl.sisbb_set_voltage(ch=0, voltage=i*step, 0.1)
    time.sleep(interval)

ctrl.sisbb_set_voltage(ch=0, voltage=0, interval)

msg = logger_high_flag_msg()
msg.timestamp = ''
print(msg)
pub.publish(msg)
