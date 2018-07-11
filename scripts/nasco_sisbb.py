#!/usr/bin/env python3

import rospy
# import std_msgs
import std_msgs
from rx_pci_single_ros.msg import nasco_sisbb_pub_msg
from rx_pci_single_ros.msg import nasco_sisbb_sub_msg

import sys
import time
import threading
import pyinterface
ad = pyinterface.open(3177, 0)
da = pyinterface.open(3408, 0)
print(pyinterface)
nodename = 'nasco_sisbb'
topicname_pub = 'nasco_sisbb'
topicname_sub = 'nasco_sisbb_command'

# rate = rospy.get_param('~rate')

class bb_controller(object):

    def __init__(self):
        self.flag = 1
        self.ch = 1
    
    def set_command(self, req):
        self.timestamp = req.timestamp
        self.interval = req.interval
        self.ch = req.ch
        self.mv = req.voltage
        self.flag = 0
        return
    
    def nascosisbb_set_voltage(self):
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
        
        
    def nascosisbb_iv_monitor(self):
        pub = rospy.Publisher(topicname_pub, nasco_sisbb_pub_msg, queue_size=1)
        msg = nasco_sisbb_pub_msg()

        while not rospy.is_shutdown():
            ret4 = ad.input_ad('ch5') * 10 # mV
            ret5 = ad.input_ad('ch6') * 1000 # uA         
            ret6 = ad.input_ad('ch7') * 10 # mV
            ret7 = ad.input_ad('ch8') * 1000 # uA
            
            msg.timestamp = time.time()
            msg.ch1_mv = ret4
            msg.ch1_ua = ret5
            msg.ch2_mv = ret6
            msg.ch2_ua = ret7

            pub.publish(msg)
            # time.sleep(rete)
            time.sleep(0.05)
            

    def start_thread_ROS(self):
        th = threading.Thread(target=self.nascosisbb_iv_monitor)
        th.setDaemon(True)
        th.start()
        th2 = threading.Thread(target=self.nascosisbb_set_voltage)
        th2.setDaemon(True)
        th2.start()

if __name__ == '__main__':
    rospy.init_node(nodename)
    b = bb_controller()
    b.start_thread_ROS()
    print('[nasco_sisbb.py] : START SUBSCRIBER')
    sub = rospy.Subscriber(topicname_sub, nasco_sisbb_sub_msg, b.set_command)
    rospy.spin()
