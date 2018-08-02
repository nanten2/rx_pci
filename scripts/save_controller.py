#!/usr/bin/env python3

import os
import sys
import time

import rospy
from rx_pci_single_ros.msg import logger_high_flag_msg

nname = 'logger_controller'
tname = 'logger_controller'

rospy.init_node(nname)
pub = rospy.Publisher(tname, save_logger_high_flag_msg, queue_size=1)

msg = logger_high_flag_msg()
msg.timestamp = str(time.time())
time.sleep(0.1)
print(msg)
pub.publish(msg)

time.sleep(3)

msg = logger_high_flag_msg()
msg.timestamp = ''
print(msg)
pub.publish(msg)
