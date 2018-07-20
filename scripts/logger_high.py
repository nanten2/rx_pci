#!/usr/bin/env python3

import os
import sys
import time
import datetime

import rospy
from rx_pci_single_ros.msg import lakeshore_218_msg
from rx_pci_single_ros.msg import ml2437a_msg
from rx_pci_single_ros.msg import sisbb_pub_msg
from rx_pci_single_ros.msg import logger_high_flag_msg

# --
data_exp_dir = '/home/amigos/data/experiment/'
dir_name = 'logger_high/'
node_name = 'logger_high'
home_dir = os.path.join(data_exp_dir, dir_name)
# --

class logger_high(object):

    def __init__(self):
        self.file_timestamp = 0
        self.flag = 1
        self.timestamp_l218 = 0
        self.timestamp_ml2437a = 0
        self.timestamp_sisbb = 0
        self.ch1_K = 0
        self.dBm = 0
        self.ch1_mv = 0
        self.ch1_ua = 0
        self.ch2_mv = 0
        self.ch2_ua = 0
        self.num = 0
        self.day = ''
        self.name = ''

    def set_flag(self, req):
        self.timestamp = req.timestamp
        if self.timestamp == '': # timestamp
            self.flag = 1
        else:
            self.flag = 0
            # _time = time.time()
            # day = _time.strftime('%Y%m%d_')
            # name = _time.strftime('%H%M%S')
            # _dir_name = day + name
            # os.makedirs(home_dir + 'aaa')
            _ = datetime.datetime.fromtimestamp(float(self.timestamp))
            self.day = _.strftime('%Y%m%d_')
            self.name = _.strftime('%H%M%S')
            os.makedirs(home_dir + self.day + self.name)
            # os.makedirs(home_dir + self.timestamp)

    def callback_l218(self, req):
        if self.flag == 1:
            return
        # filename = home_dir + self.timestamp + '/l218.txt'
        filename = home_dir + self.day + self.name + '/l218.txt'
        # filename = self.saveto + '/l218.txt'
        print(filename)
        self.timestamp_l218 = req.timestamp
        self.ch1_K = req.ch1_K
        msg = '{self.timestamp_l218} {self.ch1_K}\n'.format(**locals())
        print(msg)
        f = open(filename, 'a')
        f.write(msg)
        f.close()
        return

    def callback_ml2437a(self, req):
        if self.flag == 1:
            return
        filename = home_dir + self.day + self.name + '/ml2437a.txt'        
        # filename = home_dir + self.timestamp + '/ml2437a.txt'
        # filename = self.saveto + '/ml2437a.txt'
        self.timestamp_ml2437a = req.timestamp
        self.dBm = req.dBm
        msg = '{self.timestamp_ml2437a} {self.dBm}\n'.format(**locals())
        print(msg)
        print(filename)
        f = open(filename, 'a')
        f.write(msg)
        f.close()
        return
        
    def callback_sisbb(self, req):
        if self.flag == 1:
            return
        filename = home_dir + self.day + self.name + '/sisbb.txt'
        # filename = home_dir + self.timestamp + '/sisbb.txt'
        # filename = self.saveto + '/sisbb.txt'
        self.timestamp_sisbb = req.timestamp
        self.ch1_mv = req.ch1_mv
        self.ch1_ua = req.ch1_ua
        self.ch2_mv = req.ch2_mv
        self.ch2_ua = req.ch2_ua
        msg = '{self.timestamp_sisbb} {self.ch1_mv} {self.ch1_ua} {self.ch2_mv} {self.ch2_ua}\n'.format(**locals())
        print(msg)
        f = open(filename, 'a')
        f.write(msg)
        f.close()
        return

if __name__ == '__main__':
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)
        pass

    st = logger_high()
    rospy.init_node(node_name)
    ut = time.gmtime()
    print('start recording [filename :'+time.strftime("%Y_%m_%d_%H_%M_%S", ut)+'.txt]')
    sub_l218 = rospy.Subscriber('lakeshore_218', lakeshore_218_msg, st.callback_l218, queue_size=1)
    sub_pm = rospy.Subscriber('ml2437a', ml2437a_msg, st.
callback_ml2437a, queue_size=1)
    sub_sisbb = rospy.Subscriber('sisbb_pub', sisbb_pub_msg, st.callback_sisbb, queue_size=1)
    sub_flag = rospy.Subscriber('logger_controller', logger_high_flag_msg, st.set_flag, queue_size=1)
    rospy.spin()
    
