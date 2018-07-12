#!/usr/bin/env python3

import os
import time
import numpy
import datetime

import rospy
from rx_pci_single_ros.msg import lakeshore_218_msg
from rx_pci_single_ros.msg import ml2437a_msg
from rx_pci_single_ros.msg import nasco_sisbb_pub_msg

# --
data_exp_dir = '/home/amigos/data/experiment/'
node_name = 'save_logger_low'
home_dir = os.path.join(data_exp_dir, node_name)
# --

class save_logger_low(object):
    
    def __init__(self):
        self.timestamp = 0
        self.ch1_K = 0
        self.dBm = 0
        self.ch1_mv = 0
        self.ch1_ua = 0
        self.ch2_mv = 0
        self.ch2_ua = 0
        pass

    def callback_l218(self, req):
        self.timestamp = req.timestamp
        self.ch1_K = req.ch1_K
        return


    def callback_ml2437a(self, req):
        self.dBm = req.dBm
        return


    def callback_sisbb(self, req):
        self.ch1_mv = req.ch1_mv
        self.ch1_ua = req.ch1_ua
        self.ch2_mv = req.ch2_mv
        self.ch2_ua = req.ch2_ua
        self.pm_mv = req.pm_mv
        return

    def write_file(self):
        now = datetime.datetime.utcnow()
        day = now.strftime("%Y%m%d_")
        name = now.strftime("%H%M%S")
        filename =  day + name + ".txt"
        saveto = os.path.join(home_dir, filename)
        print(saveto)
        while not rospy.is_shutdown():
            ctime = time.time()
            f = open(saveto, 'a')
            ch1_K = self.ch1_K
            dBm = self.dBm
            ch1_mv = self.ch1_mv
            ch1_ua = self.ch1_ua
            ch2_mv = self.ch2_mv
            ch2_ua = self.ch2_ua
            msg1 = '{ctime:.1f} {ch1_K:.1f} {dBm:+.1f} {ch1_mv:+.1f} {ch1_ua:+.1f} {ch2_mv:+.1f} {ch2_ua:+.1f}\n'.format(**locals())
            msg2 = '{ctime:.1f} {ch1_K:.1f}K {dBm:+.1f}dBm {ch1_mv:+.1f}mV {ch1_ua:+.1f}uA {ch2_mv:+.1f}mV {ch2_ua:+.1f}uA'.format(**locals())
            print(msg2)
            f.write(msg1)
            f.close()

            time.sleep(5)
            continue
        return
    

if __name__ == '__main__':
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)
        pass

    st = save_logger_low()
    rospy.init_node(node_name)
    ut = time.gmtime()
    print('start recording [filename :'+time.strftime("%Y_%m_%d_%H_%M_%S", ut)+'.txt]')
    sub_l218 = rospy.Subscriber('lakeshore_218', lakeshore_218_msg, st.callback_l218, queue_size=1)
    sub_pm = rospy.Subscriber('ml2437a', ml2437a_msg, st.callback_ml2437a, queue_size=1)
    sub_sisbb = rospy.Subscriber('nasco_sisbb', nasco_sisbb_pub_msg, st.callback_sisbb, queue_size=1)
    st.write_file()
    
