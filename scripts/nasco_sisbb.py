import rospy
import std_msgs
import rx_pci_single_ros.msg import nasco_sisbb_pub_msg
import rx_pci_single_ros.msg import nasco_sisbb_sub_msg

import sys
import time
import threading
import pyinterface.pci3165 as pci3165 # AD
import pyinterface.pci3342 as pci3342 # DA


nodename = 'nasco_sisbb'
topicname = 'nasco_sisbb'
rate = rospy.get_param('~rate')

class bb_controller(object):

    def set_command(self, req):
        self.timestamp = req.timestamp
        self.ch = req.ch
        self.mv = req.mv
        self.flag = 0
        return

    
    def nascosisbb_set_voltage(self):
        while True:
            if self.flag == 1:
                time.sleep(1)
                continue
            else:
                pci3342.set_voltage(self.ch, self.mv)
                self.flag = 1
                pass
            time.sleep(rate)
            continue
                

    def start_thread_ROS(self):
        th = threading.Thread(target=self.nascosisbb_iv_monitor)
        th.setDaemon(True)
        th.start()
        th2 = threading.Thread(target=self.nascosisbb_set_voltage)
        th2.setDaemon(True)
        th2.start()
        
    def nascosisbb_iv_monitor(self):
        pub = rospy.Publisher(topicname, nasco_sisbb_msg, queue_size=1)
        msg = nasco_sisbb_msg()

        while True:
            ret = pci3165.query_input()
            
            msg.timestamp = time.time()
            msg.ch1_mv = ret[?]
            msg.ch1_ua = ret[?]
            msg.ch2_mv = ret[?]
            msg.ch2_ua = ret[?]

            pub.publish(msg)
            time.sleep(rete)

if __name__ == '__main__':
    rospy.init_node(nodename)
    b = bb_controller()
    b.start_thread_ROS()
    print('[nasco_sisbb.py] : START SUBSCRIBER')
    sub = rospy.Subscriber(topicname, nasco_sisbb_msg, b.nascosisbb_set_voltage)
    rospy.spin()
