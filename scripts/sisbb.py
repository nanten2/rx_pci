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
import pyinterface

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
            # ch = 'ch{0}'.format(self.ch)
            # print(ch)
            mv = self.mv / 3
            # print(mv)
            # da.output_da_sim(ch, mv)
            da.output_da('ch1-ch16', mv)
            self.flag = 1
            # time.sleep(rate)
            time.sleep(0.1)
            continue

    def sisbb_iv_monitor(self):
        pub1 = rospy.Publisher(tname_pub, sisbb_pub_msg, queue_size=1)
        pub2 = rospy.Publisher('ml2437a', ml2437a_msg, queue_size=1)
        msg1 = nasco_sisbb_pub_msg()
        msg2 = ml2437a_msg()

        while not rospy.is_shutdown():
            ret4 = ad.input_ad('ch5') * 10 # mV
            ret5 = ad.input_ad('ch6') * 1000 # uA
            ret6 = ad.input_ad('ch7') * 10 # mV
            ret7 = ad.input_ad('ch8') * 1000 # uA
            ret10 = ad.input_ad('ch26', 'single') * 2

            msg1.timestamp = time.time()
            msg1.ch1_mv = ret4
            msg1.ch1_ua = ret5
            msg1.ch2_mv = ret6
            msg1.ch2_ua = ret7
            msg2.timestamp = time.time()
            p = numpy.polyfit([-5, 5], [-40, 0], 1)
            pm_mv = numpy.polyval(p, ret10)
            msg2.dBm = pm_mv

            pub1.publish(msg1)
            pub2.publish(msg2)
            # time.sleep(rete)
            # time.sleep(0.02)

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
    print('sisbb.py] : START SUBSCRIBER')
    sub = rospy.Subscriber(tname_sub, sisbb_sub_msg, bctrl.set_param)
    rospy.spin()