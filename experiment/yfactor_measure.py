#!/usr/bin/env python3
import sys
import time
sys.path.append('/home/amigos/ros/src/rx_pci_single_ros/scripts')
import rospy
from rx_pci_single_ros import save_logger_high_flag_msg

pub = rospy.Publisher('save_controller', save_logger_high_flag_msg, queue_size=1)

msg = save_logger_high_flag_msg()
msg.timestamp = str(time.time())
time.sleep(0.1)
print(msg)
pub.publish(msg)

initial_voltage = 0.
final_voltage = 7.
step = 0.01
interval = 0.5
roop = int((final_voltage - initial_voltage) / step)

for i in range(roop+1):
    ctrl.nasco_sisbb_set_voltage(ch=0, voltage=i*step, interval)
    time.sleep(interval)

ctrl.nasco_sisbb_set_voltage(ch=0, voltage=0, interval)

msg = save_logger_high_flag_msg()
msg.timestamp = ''
print(msg)
pub.publish(msg)
