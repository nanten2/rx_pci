#! /usr/bin/env python3

import rospy
import std_msgs
from rx_pci_single_ros.msg import lakeshore_218_msg

import sys
import time
import threading
import NASCORX_System.device.L218 as L218

if __name__=='__main__':
    # initialize parameters
    # ---------------------
    nodename = 'lakeshore_218'
    topicname = 'lakeshore_218'
    rospy.init_node(nodename)
    host = rospy.get_param('~host')
    port = rospy.get_param('~port')
    rate = rospy.get_param('~rate')

    # setup devices
    # -------------
    try:
        temp = L218.l218(host, port)
    except OSError as e:
        rospy.logerr("{e.strerror}. host={host}".format(**locals()))
        sys.exit()

    # setup ros
    # ---------
    pub = rospy.Publisher(topicname, lakeshore_218_msg, queue_size=1)

    # start loop
    # ----------
    while not rospy.is_shutdown():
        ret = temp.measure()

        msg = lakeshore_218_msg()
        msg.timestamp = time.time()
        msg.ch1_value = ret[0]
        msg.ch2_value = ret[1]        
        msg.ch3_value = ret[2]
        msg.ch4_value = ret[3]
        msg.ch5_value = ret[4]
        msg.ch6_value = ret[5]
        msg.ch7_value = ret[6]
        msg.ch8_value = ret[7]
        pub.publish(msg)

        time.sleep(rate)
        continue
