#!/usr/bin/env python

# from geomagic_control.msg import DeviceFeedback

import os
import rospy 
from geometry_msgs.msg import PoseStamped
import rospkg
rospack = rospkg.RosPack()
packagePath = rospack.get_path('geomagic_control')
PATH = packagePath + "/scripts/RECORD10_ubuntu.txt"


def Posecallback(Pose_sub):
    x = Pose_sub.pose.position.x 
    y = Pose_sub.pose.position.y 
    z = Pose_sub.pose.position.z
    content = "{} {} {}\n".format(x,y,z)
    fp = open(PATH,'a+')
    # print(content)
    fp.write(content)
    fp.close()

if __name__=="__main__":
    rospy.init_node("record_traj",anonymous=True)
    rospy.Subscriber("/Geomagic/microPose",PoseStamped,Posecallback,queue_size=1)
    rospy.spin()
