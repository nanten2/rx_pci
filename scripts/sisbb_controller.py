import rospy
import time
from rx_pci_single_ros.msg import sisbb_sub_msg

nname = 'sisbb_controller'
tname = 'sisbb_command'
rospy.init_node(nname)

pub = rospy.Publisher(tname, sisbb_sub_msg, queue_size=1)
time.sleep(0.1)

def nasco_sisbb_set_voltage(ch, voltage, interval):
    """
    ch : channel 1 or 2
    voltage [mV] : float
    interval [ms?] : float
    """
    msg = sisbb_sub_msg()
    msg.ch = ch
    msg.voltage = voltage
    msg.interval = interval
    msg.timestamp = time.time()
    pub.publish(msg)
    print(msg)
    
