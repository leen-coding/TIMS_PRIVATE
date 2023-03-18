#! /usr/bin/env python
import websocket
import rospy
import json
import os
# from geometry_msgs.msg import Pose
from micro_control_pkg.msg import Pose_button

# 164.11.72.246
# 10.167.102.253 wifi

rospy.init_node("dataFromdjango")
serverIP = rospy.get_param("serverIP")
ws = websocket.WebSocket()
ws.connect("ws://" + serverIP + ":8000/ws/chat/lobby/")
pub_pose = rospy.Publisher("robotPose", Pose_button, queue_size=1)
robotPose = Pose_button()

while(ws.recv()):
    pose = ws.recv()
    omni_info = json.loads(pose)["message"]
    
    # print(omni_info)
    if omni_info['dev'] == 'omni':
        robotPose.Pose.header.stamp = rospy.Time.now()
        robotPose.Pose.pose.position.x = omni_info["x"]
        robotPose.Pose.pose.position.y = omni_info["y"]
        robotPose.Pose.pose.position.z = omni_info["z"]
        robotPose.grey_button = omni_info["grey"]
        robotPose.white_button = omni_info["white"]
        robotPose.Footpedal.x = omni_info["foot_x"]
        robotPose.Footpedal.y = omni_info["foot_y"]
        robotPose.Footpedal.z = omni_info["foot_z"]
        pub_pose.publish(robotPose)
    else:
        pass

