#! /usr/bin/env python3

import rospy
import std_msgs
from rx_pci_single_ros.msg import lakeshore_218_msg

import sys
import time
import threading
import NASCORX_System.device.L218 as L218

if __name__ == '__main__':
    # initialize parameters
    # ---------------------
    nname = 'lakeshore_218'
    tname = 'lakeshore_218'
    rospy.init_node(nname)
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
    pub = rospy.Publisher(tname, lakeshore_218_msg, queue_size=1)

    # start loop
    # ----------
    while not rospy.is_shutdown():
        ret = temp.measure()

        msg = lakeshore_218_msg()
        msg.timestamp = time.time()
        msg.ch1_K = ret[0]

        pub.publish(msg)

        # time.sleep(rate)
        continue
