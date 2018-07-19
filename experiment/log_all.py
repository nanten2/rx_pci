#!/usr/bin/env python3
import sys
import time
sys.path.append('/home/amigos/ros/src/rx_pci_single_ros/scripts/')
import nasco_sisbb_controller as ctrl
import rospy
from rx_pci_single_ros.msg import save_logger_high_flag_msg

# node_name = 'save_controller'
# rospy.init_node(node_name)
pub = rospy.Publisher('save_controller', save_logger_high_flag_msg, queue_size=1)

msg = save_logger_high_flag_msg()

time.sleep(0.1)
print(msg)
pub.publish(msg)

input('sawattene!!')

msg = save_logger_high_flag_msg()
msg.timestamp = ''
print(msg)
pub.publish(msg)
