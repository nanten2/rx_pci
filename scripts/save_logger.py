#!/usr/bin/env python3
import rospy
import time
import os
import sys
from rx_pci_single_ros.msg import ml2437a_msg
from rx_pci_single_ros.msg import lakeshore_218_msg
#from rx_pci_single_ros.msg import preiffer_tpg261_msg
from std_msgs.msg import Bool

# --
data_exp_dir = '/home/amigos/data/experiment'
node_name = 'save_logger'
home_dir = os.path.join(data_exp_dir, node_name)
# --

class save_logger(object):

    def __init__(self):
        self.stop_flag = 0
        pass

    def power_meter(self, req):
        print(req)
        __str = '''[power meter]
        timestamp : {0} 
        dBm : {1}\n'''
        self.f.write(__str.format(req.timestamp, req.dBm))
        pass

    def vaccume_monitor(self, req):
        print(req)
        __str = '''[preiffer_tpg261]
        timestamp : {0} 
        dBm : {1}'''
        self.f.write(__str.format(req.timestamp, req.dBm))
        pass
                                        
    
    def lakeshore(self, req):
        print(req)
        __str = '''[lakeshore218]
        timestamp : {0}
        ch1_K : {1}
        ch2_K : {2}
        ch3_K : {3}
        ch4_K : {4}
        ch5_K : {5}
        ch6_K : {6}
        ch7_K : {7}
        ch8_K : {8}\n'''
        self.f.write(__str.format(req.timestamp, req.ch1_K, req.ch2_K, req.ch3_K, req.ch4_K, req.ch5_K, req.ch6_K, req.ch7_K, req.ch8_K))
        pass

    def callback3(self, req):
        pass

    def stop_logger(self, req):
        self.stop_flag = 1

    def start_write_file(self):
        ut = time.gmtime()
        filename = time.strftime('%Y_%m_%d_%H_%M_%S.txt', ut)
        saveto = os.path.join(home_dir, filename)
        self.f = open(saveto, 'a')
        while not rospy.is_shutdown():
            time.sleep(1)
            if self.stop_flag == 1:
                rospy.signal_shutdown(self.stop_write_file)
            pass
        pass
    
    def stop_write_file(self):
        self.f.close()
        print('end of recording')

    
if __name__ == '__main__':
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)
        pass
    sl = save_logger()
    rospy.init_node(node_name)
    ut = time.gmtime()
    print('start recording')
    sub = rospy.Subscriber('ml2437a', ml2437a_msg, sl.power_meter, queue_size=1)
    #sub1 = rospy.Subscriber('pfeiffer_tpg261', preiffer_tpg261_msg, sl.vaccume_monitor, queue_size=1)
    sub2 = rospy.Subscriber('lakeshore_218', lakeshore_218_msg, sl.lakeshore, queue_size=1)
    sub_stop = rospy.Subscriber('stop_logger', Bool, sl.stop_logger, queue_size=1)
    sl.start_write_file()
