#!/usr/bin/env python3

import rospy
import std_msgs
from rx_pci_single_ros.msg import ml2437a_msg

import sys
import time
import threading
from NASCORX_System.device import ML2437A

if __name__ == '__main__':
    # initialize parameters
    # ---------------------
    nname = 'ml2437a'
    tname = 'ml2437a'
    rospy.init_node(nname)
    host = rospy.get_param('~host')
    port = rospy.get_param('~port')
    rate = rospy.get_param('~rate')

    # setup devices
    # -------------
    try:
        pm = ML2437A.ml2437a(host, port)
    except OSError as e:
        rospy.logerr("{e.strerror}. host={host}".format(**locals()))
        sys.exit()

    # setup ros
    # ---------
    pub = rospy.Publisher(tname, ml2437a_msg, queue_size=1)

    # start loop
    # ----------
    while not rospy.is_shutdown():
        msg = ml2437a_msg()
        msg.timestamp = time.time()
        msg.dBm = pm.measure()

        pub.publish(msg)

        # time.sleep(rate)
        continue
