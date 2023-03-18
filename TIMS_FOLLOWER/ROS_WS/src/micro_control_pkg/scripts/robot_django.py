#!/usr/bin/env python

import rospy
import json
import websocket
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import PoseStamped
from micro_control_pkg.msg import micro_pose
# from geometry_msgs.msg import Vector3
# ws = websocket.WebSocket()
# # 164.11.72.246
# # 10.167.102.253 wifi
# ws.connect("ws://10.167.99.204:8000/ws/chat/lobby/")

class Callback:
    def __init__(self):
        self.pos = None
        self.current_data = None
        self.message = None
        # self.force = None

    def pos_callback(self,msg):
        self.pos = msg
        self.handleCallback()

    # def force_callback(self,msg):
    #     self.force = msg
    #     self.handleCallback()
   
        
    def handleCallback(self):
        if self.pos is not None:
            self.current_data = {
                'dev': "micro",
                'x': self.pos.Pose.pose.position.x,
                'y':  self.pos.Pose.pose.position.y,
                'z':  self.pos.Pose.pose.position.z,
                'r': self.pos.r,
                'taskFlag':self.pos.taskFlag,
                'time': str(self.pos.Pose.header.stamp),
                # 'force_x': self.force.x,
                # 'force_y': self.force.y,
                # 'force_z': self.force.z,
            }
            # print(self.current_data)
            self.message = json.dumps({
                'message' : self.current_data})

            ws.send(self.message)


if __name__ == '__main__':
    rospy.init_node('listener')
    serverIP = rospy.get_param("serverIP")
    ws = websocket.WebSocket()
    ws.connect("ws://" + serverIP + ":8000/ws/chat/lobby/")
    mycallback = Callback()
    rospy.Subscriber('/micro_pose', micro_pose, mycallback.pos_callback, queue_size=1)
    # rospy.Subscriber('/force_feedback', Vector3, mycallback.force_callback, queue_size=1)

    rospy.spin()