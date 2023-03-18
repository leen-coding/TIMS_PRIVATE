#!/usr/bin/env python
import rospy
import json
from geometry_msgs.msg import PoseStamped

import os
from std_msgs.msg import Bool
import rospkg
rospack = rospkg.RosPack()
packagePath = rospack.get_path('geomagic_control')
PATH = packagePath + "/scripts/data_record/django"


record_num = len(os.listdir(PATH))

class Callback:
    def __init__(self):
        self.pos = None
        self.tactile = None


    def pos_callback(self,msg):
        self.pos = msg
        self.dataRecord()
    
    def tactile_callback(self,msg):
        self.tactile = msg.data
        self.dataRecord()
    

    def dataRecord(self):
        if self.pos is not None and self.tactile is not None:
            timeStamp = self.pos.header.stamp
            new_x = self.pos.pose.position.x
            new_y = self.pos.pose.position.y
            new_z = self.pos.pose.position.z
            tactile = self.tactile
            django_side = {
            'dev': 'micro', 
            'time': str(timeStamp),
            'x': round(new_x,8),
            'y': round(new_y,8),
            'z': round(new_z,8),
            'tictile': int(tactile)
            }
            
            js = json.dumps(django_side)   
            global record_num 
            with open(PATH+'/django_participant' +str(record_num)+'.txt','a') as f:    
                f.write(js)      
                f.write('\n')     
                f.close()      
        else:
            pass



if __name__ == '__main__':
    rospy.init_node('django_record_listener')
    bool_value = rospy.get_param("/record")
    if bool_value:
        mycallback = Callback()
        rospy.Subscriber('/Geomagic/microPose', PoseStamped, mycallback.pos_callback, queue_size=1)
        rospy.Subscriber('/Geomagic/tactileInfo',Bool ,mycallback.tactile_callback, queue_size=1)
        rospy.spin()