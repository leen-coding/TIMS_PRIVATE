#!/usr/bin/env python
import rospy
import json
import websocket
from sensor_msgs.msg import JointState
from turtlesim.msg import Pose
from geometry_msgs.msg import PoseStamped
from micro_control_pkg.msg import micro_pose
from geometry_msgs.msg import Vector3
import os

PATH = 'C:\LeenWS\src\micro_control_pkg\scripts\data_record\local'





record_num = len(os.listdir(PATH))

class Callback:
    def __init__(self):
        self.pos = None
        # self.button = None
        # self.footpedal = None


    def pos_callback(self,msg):
        self.pos = msg
        self.dataRecord()
    
    # def button_callback(self,msg):
    #     self.button = msg
    #     self.dataRecord()

    # def footpedal_callback(self,msg):
    #     self.footpedal = msg
    #     self.dataRecord()
    

    def dataRecord(self):
        if self.pos is not None:
            timeStamp = self.pos.Pose.header.stamp
            new_x = self.pos.Pose.pose.position.x
            new_y = self.pos.Pose.pose.position.y
            new_z = self.pos.Pose.pose.position.z
            new_r = self.pos.r
            stage = self.pos.taskFlag
            # print("pos_x: {}".format(new_x))
            # print("gray b: {}".format(new_gray_b))
            # print("foot_x: {}".format(foot_x))

            # new_record = "dev: {}   time: {}    x: {}   y: {}  z: {}    gray: {}    white: {}   foot_x: {}  foot_y: {}  foot_z: {}".format('omni',str(timeStamp),
            # round(new_x,8),round(new_y,8),round(new_z,8),new_gray_b,new_white_b,foot_x,foot_y,foot_z)
            # print(timeStamp)
            windows_side = {
            'dev': 'micro', 
            'time': str(timeStamp),
            'x': round(new_x, 8),
            'y': round(new_y, 8),
            'z': round(new_z, 8),
            'r': round(new_r, 8),
            'taskFlag': stage
            }
            
            js = json.dumps(windows_side)   
            global record_num 
            with open(PATH +'/local_participant' +str(record_num)+'.txt','a') as f:    #设置文件对象
                f.write(js)      
                f.write('\n')     
                f.close()      #将字符串写入文件中
        else:
            pass



if __name__ == '__main__':
    rospy.init_node('windows_record_listener')

    mycallback = Callback()
    rospy.Subscriber('micro_pose', micro_pose, mycallback.pos_callback, queue_size=1)

    # rospy.Subscriber('/Geomagic/footPedal', Vector3 ,mycallback.footpedal_callback, queue_size=1)
    

    rospy.spin()