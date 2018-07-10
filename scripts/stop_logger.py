import rospy, time
from std_msgs.msg import Bool
"""
try:
    rospy.init_node('stop_logger')
except:
    pass
"""

def stop_logger():
    pub = rospy.Publisher('stop_logger', Bool, queue_size=1)
    time.sleep(2)#to wait until publisher is registered by roscore
    pub.publish()
    print('Published message to save_logger.py to stop')
