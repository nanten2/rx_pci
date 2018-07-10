#!/usr/bin/env python3

import sys
import rospy
import time
import threading
from rx_pci_single_ros.msg import ml2437a_msg

node_name = 'logger_high'

class ml2437a(object):

    def __init__(self):
        self.sub1 = rospy.Subscriber('ml2437a', ml2437a_msg, self.callback1, queue_size=1)
        pass

    def callback1(self, req):
        print(req)
        

    def status_thread(self):
        #status = threading.Thread(target = self.pub_status)
        #status.setDaemon(True)
        #status.start()
        pass

    def pub_status(self):
        msg = ml2437a_msg()
        while not rospy.is_shutdown():
            msg.dBm = 0.1#?????????
            msg.timestamp = time.time()
            self.pub.publish(msg)
            time.sleep(1)
        return

if __name__ == '__main__':
    rospy.init_node(node_name)
    ml2437a = ml2437a()    
    ml2437a.status_thread()
    rospy.spin()
