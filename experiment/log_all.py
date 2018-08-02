#!/usr/bin/env python3
import sys
import time
sys.path.append('/home/amigos/ros/src/rx_pci_single_ros/scripts/')
import sisbb_controller as ctrl
import rospy
from rx_pci_single_ros.msg import logger_high_flag_msg

# node_name = 'save_controller'
# rospy.init_node(node_name)
tname = 'logger_controller'
pub = rospy.Publisher(tname, logger_high_flag_msg, queue_size=1)

msg = logger_high_flag_msg()
msg.timestamp = str(time.time())
time.sleep(0.1)
print(msg)
pub.publish(msg)

input('sawattene!!')

msg = logger_high_flag_msg()
msg.timestamp = ''
print(msg)
pub.publish(msg)
