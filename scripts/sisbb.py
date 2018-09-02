#!/usr/bin/env python3

import rospy
import std_msgs
from rx_pci_single_ros.msg import sisbb_pub_msg
from rx_pci_single_ros.msg import sisbb_sub_msg
from rx_pci_single_ros.msg import ml2437a_msg

import sys
import time
import numpy
import threading
import pyinterface.tools as pyinterface

ad = pyinterface.open(3177, 0)
da = pyinterface.open(3408, 0)

nname = 'sisbb'
tname_pub = 'sisbb_pub'
tname_sub = 'sisbb_sub'

# rate = rospy.get_param('~rate')

class sisbb_controller(object):

    def __init__(self):
        self.flag = 1
        self.ch = 1

    def set_param(self, req):
        self.timestamp = req.timestamp
        self.interval = req.interval
        self.ch = req.ch
        self.mv = req.voltage
        self.flag = 0
        return

    def sisbb_set_voltage(self):
        while not rospy.is_shutdown():
            if self.flag == 1:
                time.sleep(0.01)
                continue
            mv = self.mv / 3
            da.output_voltage(1, mv)
            da.output_voltage(2, mv)
            # da.output_da('ch1-ch16', mv)
            self.flag = 1
            time.sleep(0.1)
            continue

    def sisbb_iv_monitor(self):
        pub1 = rospy.Publisher(tname_pub, sisbb_pub_msg, queue_size=1)
        pub2 = rospy.Publisher('ml2437a', ml2437a_msg, queue_size=1)
        time.sleep(0.01)
        msg1 = sisbb_pub_msg()
        msg2 = ml2437a_msg()
        time.sleep(0.1)

        while not rospy.is_shutdown():
            '''
            ret1 = ad.input_ad('ch1') * 10 / 2   # mV
            ret2 = ad.input_ad('ch2') * 1000 / 2 # uA
            ret3 = ad.input_ad('ch3') * 10 / 2   # mV
            ret4 = ad.input_ad('ch4') * 1000 / 2 # uA
            '''
            ret1 = ad.input_voltage(1, 'diff') * 10
            ret2 = ad.input_voltage(2, 'diff') * 1000
            ret3 = ad.input_voltage(3, 'diff') * 10
            ret4 = ad.input_voltage(4, 'diff') * 1000          
            ret10 = ad.input_voltage(26, 'single')

            msg1.timestamp = time.time()
            msg1.ch1_mv = ret1
            msg1.ch1_ua = ret2
            msg1.ch2_mv = ret3
            msg1.ch2_ua = ret4

            msg2.timestamp = time.time()
            p = numpy.polyfit([-5, 5], [-40, 0], 1)
            pm_mv = numpy.polyval(p, ret10)
            msg2.dBm1 = pm_mv
            msg2.dBm2 = pm_mv

            pub1.publish(msg1)
            pub2.publish(msg2)
            # time.sleep(rete)
            time.sleep(0.02)


    def start_thread_ROS(self):
        th = threading.Thread(target=self.sisbb_iv_monitor)
        th.setDaemon(True)
        th.start()
        th2 = threading.Thread(target=self.sisbb_set_voltage)
        th2.setDaemon(True)
        th2.start()

if __name__ == '__main__':
    rospy.init_node(nname)
    bctrl = sisbb_controller()
    bctrl.start_thread_ROS()
    print('[sisbb.py] : START SUBSCRIBER ... ')
    sub = rospy.Subscriber(tname_sub, sisbb_sub_msg, bctrl.set_param)
    rospy.spin()
