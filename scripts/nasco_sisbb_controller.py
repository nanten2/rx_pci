import rospy
from rx_pci_single_ros.msg import nasco_sisbb_controller_msg

node_name = 'sisbb_controller'
rospy.init_node(node_name)

pub = rospy.Publisher('sisbb_controller', nasco_sisbb_controller_msg, queue_size=1)

def nasco_sisbb_set_voltage(ch, voltage, interval):
    """
    ch : channel 1 or 2
    voltage [mV] : list
    interval [ms?] : list
    """
    cm = nasco_sisbb_controller_msg()
    cm.ch = ch
    cm.voltage = voltage
    cm.interval = interval
    pub.publish(cm)
    print(cm)
    
