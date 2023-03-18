#!/usr/bin/env python
from sensapex import UMP
import threading
import numpy as np
from micro_control_pkg.msg import micro_pose
import rospy
from micro_control_pkg.msg import Pose_button
from geometry_msgs.msg import Vector3



ump = UMP.get_ump()
dev_ids = ump.list_devices()

device = ump.get_device(dev_ids[0])
device.ump.restart_device
device.goto_pos((9999, 9999, 9999, 9999), speed=2000)
print('UMP READY!!!!!!!!')

currentPose = [9999, 9999, 9999, 9999]
taskFlag = 0

#######
import socket
import struct
import time


#######

class msg:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.grey = 0
        self.white = 0
        

class SubscribeC:
    def __init__(self):
        global device
        self.device = device
        self.Omni_msg = msg()
        self.Omni_msg_pre = msg()
        self.gap = msg()
        self.footpedal = Vector3()

        self.First = True
        # 35 2/9
        self.Ratio_scale = 35
        self.closeFlag = False
        self.startFlag = False
        self.clutchFlag = False

        self.current = np.array([9999, 9999, 9999, 9999])
        self.t1_end=np.array([15930.8095703125, 13384.58984375, 14567.8359375])
        self.jumpTorleance = np.array([600,600,7000])
        self.t1_upper = self.t1_end + self.jumpTorleance
        self.t1_lower = self.t1_end - self.jumpTorleance
        self.t2_start=np.array([15210.166,13613.1338,12973.5800])
        
        self.taskFlag = 1
        self.taskTrans = 0

        self.subPose = rospy.Subscriber('robotPose', Pose_button, self.poseCallback, queue_size=1)
        

        
    def control_micro(self,Pose_sub):
        self.Omni_msg.x = Pose_sub.Pose.pose.position.z
        self.Omni_msg.y = -Pose_sub.Pose.pose.position.x
        self.Omni_msg.z = -Pose_sub.Pose.pose.position.y


        self.Omni_msg.grey = Pose_sub.grey_button
        self.Omni_msg.white = Pose_sub.white_button
        self.footpedal = Pose_sub.Footpedal

        if self.footpedal.x == 1 or self.startFlag:
            if self.startFlag == False:
                print("START CONTROL!!!!!!!!")
                self.startFlag = True
            
        if self.startFlag:
            if self.footpedal.z == 1 or self.closeFlag:
                if self.closeFlag == False:
                    self.device.goto_pos((9999, 9999, 9999, 9999), speed=2000)
                    self.device.ump.restart_device
                    self.device.ump._update_moves
                    print("device close!!!!!")
                    self.closeFlag = True
                    self.device.ump.close()

            
            if not self.closeFlag:
                if self.First:
                    self.Omni_msg_pre.x = self.Omni_msg.x
                    self.Omni_msg_pre.y = self.Omni_msg.y
                    self.Omni_msg_pre.z = self.Omni_msg.z

                    self.First = False
                    

                if self.footpedal.y == 1:
                    self.clutchFlag = False
                    self.gap.x = self.Omni_msg.x - self.Omni_msg_pre.x if (self.Omni_msg.x - self.Omni_msg_pre.x) < 50 else 50
                    self.gap.y = self.Omni_msg.y - self.Omni_msg_pre.y if (self.Omni_msg.y - self.Omni_msg_pre.y) < 50 else 50
                    self.gap.z = self.Omni_msg.z - self.Omni_msg_pre.z if (self.Omni_msg.z - self.Omni_msg_pre.z) < 50 else 50
                    

                    if self.Omni_msg.grey == 1 or self.Omni_msg.white == 1:
                        
                        if self.Omni_msg.grey == 1 and self.Omni_msg.white == 0:
                            #r+++
                            self.current[3] = self.current[3] + 50
                            self.device.goto_pos([self.current[0],self.current[1],self.current[2],self.current[3]],speed = 2500)
                                
                        elif self.Omni_msg.grey == 0 and self.Omni_msg.white == 1:
                            #r---
                            self.current[3] = self.current[3] - 50
                            self.device.goto_pos([self.current[0],self.current[1],self.current[2],self.current[3]],speed = 2500)
                        else:
                            self.current[3] = 9999
                            self.device.goto_pos([self.current[0],self.current[1],self.current[2],self.current[3]],speed = 2500)
                            print("RECOVER!!!!")
                    else:

                        if self.gap.x != 0 or  self.gap.y != 0 or  self.gap.z != 0:
                            global currentPose
                            currentPose = self.device.get_pos()
                            self.current = currentPose
                            self.device.goto_pos([self.current[0]+self.gap.x * self.Ratio_scale ,self.current[1]+self.gap.y * self.Ratio_scale,self.current[2] + self.gap.z * self.Ratio_scale,self.current[3]], 2000)

                elif not self.footpedal.y and not self.clutchFlag:
                    # device.stop()
                    self.clutchFlag = True
                    print("CLUTHING!!!!!!!!!!")
                    

                if not self.First:
                    self.Omni_msg_pre.x = self.Omni_msg.x
                    self.Omni_msg_pre.y = self.Omni_msg.y
                    self.Omni_msg_pre.z = self.Omni_msg.z


    def poseCallback(self, Pose_sub):
        global taskFlag
        taskFlag = self.taskFlag
        if self.taskFlag == 1:
            flag = np.all(self.current[0:3]<self.t1_upper) and np.all(self.current[0:3]>self.t1_lower)
            if (flag):
                print("goto setp 2")
                self.taskFlag = 2

            else:
                self.control_micro(Pose_sub)

        if self.taskFlag == 2:
            global currentPose
            self.current = device.get_pos()
            currentPose = self.current
            
            dist = np.linalg.norm(self.current[0:3] - self.t2_start)
            if dist > 5:
                
                device.goto_pos([self.t2_start[0],self.t2_start[1],self.t2_start[2],self.current[3]], 500)
                
            else:
                print("go to step 3")
                self.taskFlag = 3

        if self.taskFlag == 3:
            self.control_micro(Pose_sub)

                


def pubPose(pub):
    rate = rospy.Rate(10)
    while True:
        nowPose =  micro_pose()
        global taskFlag
        global currentPose
        
        nowPose.Pose.header.stamp = rospy.Time.now() 
        nowPose.Pose.pose.position.x = currentPose[0]
        nowPose.Pose.pose.position.y = currentPose[1]
        nowPose.Pose.pose.position.z = currentPose[2]
        nowPose.r = currentPose[3]
        nowPose.taskFlag = taskFlag

        pub.publish(nowPose)
  
        rate.sleep()

def micro_control():
    ic = SubscribeC()
    rospy.spin()

   
   
   
if __name__ == '__main__':
    rospy.init_node('robotPoseDispatcher', anonymous=True)
    pub = rospy.Publisher("micro_pose", micro_pose, queue_size=1)
    t1 = threading.Thread(target=micro_control)
    t1.daemon = True
    t1.start()
    pubPose(pub)




