#!/usr/bin/env python
import rospy
import json

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from micro_control_pkg.msg import Pose_button
import os

PATH = 'C:\LeenWS\src\micro_control_pkg\scripts\data_record\django'
    # os.mkdir(os.path.join(participant_path,"from_django"))




record_num = len(os.listdir(PATH))

class Callback:
    def __init__(self):
        self.pos = None


    def pos_callback(self,msg):
        self.pos = msg
        self.dataRecord()
    
    

    def dataRecord(self):
        if self.pos is not None:
            timeStamp = self.pos.Pose.header.stamp
    
            new_x = self.pos.Pose.pose.position.x
            new_y = self.pos.Pose.pose.position.y
            new_z = self.pos.Pose.pose.position.z
            gray = self.pos.grey_button
            white = self.pos.white_button
            foot_x = self.pos.Footpedal.x
            foot_y = self.pos.Footpedal.y
            foot_z = self.pos.Footpedal.z
            django_side = {
            'dev': 'omni', 
            'time': str(timeStamp),
            'x': round(new_x,8),
            'y': round(new_y,8),
            'z': round(new_z,8),
            'gray': gray,
            'white': white,
            'foot_x': foot_x,
            'foot_y': foot_y,
            'foot_z': foot_z
            }
            
            js = json.dumps(django_side)   
            global record_num 
            with open(PATH+'/django_participant' +str(record_num)+'.txt','a') as f:    #设置文件对象
                f.write(js)      
                f.write('\n')     
                f.close()      #将字符串写入文件中
        else:
            pass



if __name__ == '__main__':
    rospy.init_node('django_record_listener')

    mycallback = Callback()
    rospy.Subscriber('robotPose', Pose_button, mycallback.pos_callback, queue_size=1)
    # rospy.Subscriber('/Geomagic/tactileInfo',Bool ,mycallback.tactile_callback, queue_size=1)

    

    rospy.spin()