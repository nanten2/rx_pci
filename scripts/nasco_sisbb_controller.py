import rospy
import time
from rx_pci_single_ros.msg import nasco_sisbb_sub_msg

node_name = 'sisbb_controller'
rospy.init_node(node_name)

pub = rospy.Publisher('nasco_sisbb_command', nasco_sisbb_sub_msg, queue_size=1)

def nasco_sisbb_set_voltage(ch, voltage, interval):
    """
    ch : channel 1 or 2
    voltage [mV] : float
    interval [ms?] : float
    """
    cm = nasco_sisbb_controller_msg()
    cm.ch = ch
    cm.voltage = voltage
    cm.interval = interval
    cm.timestamp = time.time()
    pub.publish(cm)
    print(cm)
    
