#!/usr/bin/env python3
import sys
import rospy
import time
import threading
from rx_pci_single_ros.msg import ml2437a_msg
from NASCORX_System.device import ML2437A

node_name = 'ml2437a'

IP_adress = '192.168.100.44'
port = 13

class ml2437a(object):

    def __init__(self):
        self.pub = rospy.Publisher('ml2437a',ml2437a_msg, queue_size=1)
        pass


    def status_thread(self):
        status = threading.Thread(target = self.pub_status)
        status.setDaemon(True)
        status.start()
        return

    def pub_status(self):
        msg = ml2437a_msg()
        p_meter = ML2437A.ml2437a(IP_adress, port)
        while not rospy.is_shutdown():
            msg.dBm = p_meter.measure()
            msg.timestamp = time.time()
            self.pub.publish(msg)
            time.sleep(0.01)
        return

if __name__ == '__main__':
    rospy.init_node(node_name)
    ml2437a = ml2437a()    
    ml2437a.pub_status()
