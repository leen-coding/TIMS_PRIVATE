#! /usr/bin/env python
import websocket
import rospy
import json

from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped
ws = websocket.WebSocket()
from geometry_msgs.msg import Vector3
ws.connect("ws://localhost:8000/ws/chat/lobby/")
rospy.init_node("django2ros_node")
tactile_pub = rospy.Publisher("tactileInfo", Bool, queue_size=1)
micro_pose_pub = rospy.Publisher("microPose", PoseStamped, queue_size=1)

tactileInfo = Bool()
microInfo = PoseStamped()

while(ws.recv() and (not rospy.is_shutdown())):
    pose = ws.recv()
    receive_info = json.loads(pose)["message"]
    
    if receive_info ['dev'] == 'cam2_tactile':
        if receive_info ['touch'] == 1:
            tactileInfo = True
        else:
            tactileInfo = False
        tactile_pub.publish(tactileInfo)
    elif  receive_info['dev'] == 'micro':
        microInfo.header.stamp = rospy.Time.now()
        microInfo.pose.position.x =  receive_info['x']
        microInfo.pose.position.y =  receive_info['y']
        microInfo.pose.position.z =  receive_info['z']
        micro_pose_pub.publish(microInfo)
    else:
        pass
