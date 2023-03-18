#!/usr/bin/env python

# from geomagic_control.msg import DeviceFeedback

import os
import rospy 
from geometry_msgs.msg import PoseStamped
NO = len(os.listdir("C:/LeenWS/src/micro_control_pkg/scripts/GPR_data/"))
from micro_control_pkg.msg import micro_pose
PATH = "C:/LeenWS/src/micro_control_pkg/scripts/GPR_data/RECORD" + str(NO + 1) +".txt"

def Posecallback(pos):
    if pos is not None:
        # timeStamp = pos.Pose.header.stamp
        x = pos.Pose.pose.position.x
        y = pos.Pose.pose.position.y
        z = pos.Pose.pose.position.z
        content = "{} {} {}\n".format(x,y,z)
        fp = open(PATH,'a+')
        # print(content)
        fp.write(content)
        fp.close()

if __name__=="__main__":
    rospy.init_node("record_traj",anonymous=True)
    rospy.Subscriber('micro_pose', micro_pose, Posecallback, queue_size=1)

    rospy.spin()
