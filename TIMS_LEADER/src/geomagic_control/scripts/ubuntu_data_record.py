#!/usr/bin/env python
import rospy
import json
import websocket
from sensor_msgs.msg import JointState
from turtlesim.msg import Pose
from geometry_msgs.msg import PoseStamped
from geomagic_control.msg import DeviceButtonEvent
from geometry_msgs.msg import Vector3
import os
import rospkg
rospack = rospkg.RosPack()
packagePath = rospack.get_path('geomagic_control')
PATH = packagePath + "/scripts/data_record/local"


record_num = len(os.listdir(PATH))

class Callback:
    def __init__(self):
        self.pos = None
        self.button = None
        self.footpedal = None


    def pos_callback(self,msg):
        self.pos = msg
        self.dataRecord()
    
    def button_callback(self,msg):
        self.button = msg
        self.dataRecord()

    def footpedal_callback(self,msg):
        self.footpedal = msg
        self.dataRecord()
    

    def dataRecord(self):
        if self.pos is not None and self.button is not None and self.footpedal is not None:
            timeStamp = self.pos.header.stamp
            new_x = self.pos.pose.position.x
            new_y = self.pos.pose.position.y
            new_z = self.pos.pose.position.z
            new_gray_b = self.button.grey_button
            new_white_b = self.button.white_button
            foot_x = self.footpedal.x
            foot_y = self.footpedal.y
            foot_z = self.footpedal.z

            ubuntu_side = {
            'dev': 'omni', 
            'time': str(timeStamp),
            'x': round(new_x,8),
            'y': round(new_y,8),
            'z': round(new_z,8),
            'grey': new_gray_b,
            'white': new_white_b,
            'foot_x':foot_x,
            'foot_y':foot_y,
            'foot_z':foot_z,
            }
            
            js = json.dumps(ubuntu_side)   
            global record_num 
            with open(PATH +'/local_participant' +str(record_num)+'.txt','a') as f:    #设置文件对象
                f.write(js)      
                f.write('\n')     
                f.close()      #将字符串写入文件中
        else:
            pass



if __name__ == '__main__':
    rospy.init_node('ubuntu_record_listener')
    bool_value = rospy.get_param("/record")
    if bool_value:
        mycallback = Callback()
        rospy.Subscriber('/Geomagic/pose', PoseStamped, mycallback.pos_callback, queue_size=1)
        rospy.Subscriber('/Geomagic/button', DeviceButtonEvent ,mycallback.button_callback, queue_size=1)
        rospy.Subscriber('/Geomagic/footPedal', Vector3 ,mycallback.footpedal_callback, queue_size=1)
        

        rospy.spin()