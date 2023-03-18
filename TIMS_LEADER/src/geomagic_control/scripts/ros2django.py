#!/usr/bin/env python


import rospy
import json
import websocket
import math
from sensor_msgs.msg import JointState
from turtlesim.msg import Pose
from geometry_msgs.msg import PoseStamped
from geomagic_control.msg import DeviceButtonEvent
from geomagic_control.msg import DeviceFeedback
from geometry_msgs.msg import Vector3
ws = websocket.WebSocket()

ws.connect("ws://localhost:8000/ws/chat/lobby/")

class Callback:
    def __init__(self):
        self.pos = None
        self.button = None
        self.footpedal = None
        self.DFB = None


    def pos_callback(self,msg):
        self.pos = msg
        self.todjango()
    
    def button_callback(self,msg):
        self.button = msg
        self.todjango()

    def footpedal_callback(self,msg):
        self.footpedal = msg
        self.todjango()
    
    def DFB_callback(self,msg):
        self.DFB = msg
        self.todjango()
    

    def todjango(self):
        if self.pos is not None and self.button is not None and self.footpedal is not None:
            new_x = self.pos.pose.position.x
            new_y = self.pos.pose.position.y
            new_z = self.pos.pose.position.z
            timeStamp = str(self.pos.header.stamp)
            new_gray_b = self.button.grey_button
            new_white_b = self.button.white_button
            foot_x = self.footpedal.x
            foot_y = self.footpedal.y
            foot_z = self.footpedal.z
            if self.DFB == None:
                F = 0
            else:
                F_x = self.DFB.force.x
                F_y = self.DFB.force.y
                F_z = self.DFB.force.z
                F = math.sqrt(F_x**2 + F_y**2 + F_z**2)
   
            position = {
            'dev': 'omni', 
            'x': round(new_x,8),
            'y': round(new_y,8),
            'z': round(new_z,8),
            'grey': new_gray_b,
            'white': new_white_b,
            'foot_x':foot_x,
            'foot_y':foot_y,
            'foot_z':foot_z,
            'force': F,
            'time': timeStamp 
            }
            message = json.dumps({'message' : position },ensure_ascii=False).encode('charmap')
            ws.send(message)
            # print("send success")
        else:
            pass




if __name__ == '__main__':
    rospy.init_node('listener')

    mycallback = Callback()
    rospy.Subscriber('/Geomagic/pose', PoseStamped, mycallback.pos_callback, queue_size=1)
    rospy.Subscriber('/Geomagic/button', DeviceButtonEvent ,mycallback.button_callback, queue_size=1)
    rospy.Subscriber('/Geomagic/footPedal', Vector3 ,mycallback.footpedal_callback, queue_size=1)
    rospy.Subscriber('/Geomagic/force_feedback', DeviceFeedback ,mycallback.DFB_callback, queue_size=1)
    

    rospy.spin()