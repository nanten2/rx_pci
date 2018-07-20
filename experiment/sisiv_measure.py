#!/usr/bin/env python3
import sys
import time
sys.path.append('/home/amigos/ros/src/rx_pci_single_ros/scripts/')
import sisbb_controller as ctrl
import rospy
from rx_pci_single_ros.msg import logger_high_flag_msg

# node_name = 'save_controller'
# rospy.init_node(node_name)
tname = 'save_controller'
pub = rospy.Publisher(tname, logger_high_flag_msg, queue_size=1)

msg = logger_high_flag_msg()
msg.timestamp = str(time.time())
time.sleep(0.1)
print(msg)
pub.publish(msg)

initial_voltage = 0 # mV
final_voltage = 7 # mV
step = 0.1 # mV
roop = int((final_voltage - initial_voltage) / step)

for i in range(roop+1):
    # ctrl.nasco_sisbb_set_voltage(ch=3, voltage=i*step, interval=0.1)
    # ctrl.nasco_sisbb_set_voltage(ch=3, voltage=i*step, interval=0.1)
    ctrl.sisbb_set_voltage(ch=0, voltage=i*step, interval=0.1)
    time.sleep(3)

ctrl.sisbb_set_voltage(ch=1, voltage=0, interval=0.1)
ctrl.sisbb_set_voltage(ch=2, voltage=0, interval=0.1)
ctrl.sisbb_set_voltage(ch=3, voltage=0, interval=0.1)
ctrl.sisbb_set_voltage(ch=4, voltage=0, interval=0.1)

msg = logger_high_flag_msg()
msg.timestamp = ''
print(msg)
pub.publish(msg)
