import numpy as np
from geomagic_control.msg import DeviceFeedback
from geometry_msgs.msg import PoseStamped
import rospy
from geometry_msgs.msg import Vector3
from collections import OrderedDict
from collections import deque
import rospkg
rospack = rospkg.RosPack()
packagePath = rospack.get_path('geomagic_control')
PATH = packagePath + "/scripts/gprfile_rbf_best.txt"
import math
from geometry_msgs.msg import Twist


trajectory = np.loadtxt(PATH)
trajectory = np.array(list(OrderedDict.fromkeys(map(tuple, trajectory))))
trajectory = deque(trajectory)
# [0:344,:]
max_error = 80

def euclidean_distance(point, point_set):

    return np.linalg.norm(point_set - point, axis=1)


class Callback:
    def __init__(self):
        self.pub = rospy.Publisher("force_feedback",DeviceFeedback,queue_size=1)
        self.pos = None
        self.footpedal = None
        global trajectory
        self.trajectory = trajectory
        self.popleft =  np.array([9999, 9999, 9999])

    def pos_callback(self,msg):
        self.pos = msg
        self.handleCallback()
    


    def footpedal_callback(self,msg):
        self.footpedal = msg
        self.handleCallback()
        
    def handleCallback(self):
        if self.pos is not None and self.footpedal is not None:
            ratio = 0.0015
            DFB = DeviceFeedback()
            if self.footpedal.x == 1 or self.footpedal.y == 0 or self.footpedal.z == 1: 
                DFB.force.x = 0
                DFB.force.y = 0
                DFB.force.z = 0

            else:
                x = self.pos.pose.position.x
                y = self.pos.pose.position.y
                z = self.pos.pose.position.z
                
                point = np.array([x, y, z])
                # print(point)

                distances = euclidean_distance(point,  self.trajectory)
                min_index, min_value = min([(i, x) for i, x in enumerate(distances)], key=lambda x: x[1])

                if min_value < max_error:
                    # for i in range(0,min_index):
                    #     self.popleft = self.trajectory.popleft()     
                    pass

                else:
               
                    nearest_point = self.trajectory[min_index]
                    DFB.force.x = (point[1] - nearest_point[1])*ratio
                    DFB.force.y = (point[2] - nearest_point[2])*ratio
                    DFB.force.z = -(point[0] - nearest_point[0])*ratio

                    # print(-(point[0] - nearest_point[0])*0.0005)
            self.pub.publish(DFB)




if __name__ == '__main__':
    rospy.init_node('listener')

    mycallback = Callback()
    rospy.Subscriber('/Geomagic/microPose', PoseStamped, mycallback.pos_callback, queue_size=1)

    rospy.Subscriber('/Geomagic/footPedal', Vector3 ,mycallback.footpedal_callback, queue_size=1)
    rospy.spin()