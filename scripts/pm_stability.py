#!/usr/bin/env python3

import os
import time
import datetime

import rospy
from rx_pci_single_ros.msg import ml2437a_msg

node_name = 'pm_status'
home_dir = '/home/amigos/data/experiment/save_pm_stability'

class monitor_pm(object):

    def __init__(self):
        self.timestamp = 0
        self.dBm = 0

    def callback(self, req):
        self.timestamp = req.timestamp
        self.dBm = req.dBm
        return

    def write_value(self):
        now = datetime.datetime.utcnow()
        day = now.strftime('%Y%m%d_')
        name = now.strftime('%H%M%S')
        filename = day + name + '.txt'
        saveto = os.path.join(home_dir, filename)
        print('SaveDir is {saveto}'.format(**locals()))
        while not rospy.is_shutdown():
            f = open(saveto, 'w')
            msg1 = '{self.timestamp:.1f} {self.dBm:+.3f}'.format(**locals())
            msg2 = '{self.timestamp:.1f} {self.dBm:+.3f}dBm'.format(**locals())
            print(msg2)
            f.write(msg1)
            f.close()

            time.sleep(0.1)
            continue
        return

if __name__ == '__main__':
        print('Start monitoring [Power Mater]')
        st = monitor_pm()
        rospy.init_node(node_name)
        sub_pm = rospy.Subscriber('ml2437a', ml2437a_msg, st.callback, queue_size=1)
        st.write_value()
