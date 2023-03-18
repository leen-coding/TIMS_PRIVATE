import time
from socket import *
import cv2
import time

import argparse

def run(targetIP,
        camPosition,
        source):
    
    host = targetIP
    port = 5005
    Udp_Socket = socket(AF_INET,SOCK_DGRAM)
    video = cv2.VideoCapture(source)

    print("Streaming CAM "+ str(source)+ " in Position "+ str(camPosition) + " of Web page")
    while True:
        success, image = video.read()
        # unixTime = str(time.time())
        # font = cv2.FONT_HERSHEY_SIMPLEX
        image = cv2.resize(image, (400, 300))
        # image = cv2.putText(image, unixTime, (2, 290), font, 1,
        #                     (0, 0, 255), 1, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', image)



        frame_b = jpeg.tobytes()
        camPosition_b = camPosition.to_bytes(1,'big')

        Udp_Socket.sendto(camPosition_b+frame_b, (host, port))
    
        # print("send success")
        # clientSocket.send(frame)

        # time.sleep(0.03)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            Udp_Socket.close()
            video.release()
            break

   
def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--targetIP', type=str, default='0.0.0.0', help='target server IP')
    parser.add_argument('--camPosition', type=int, default=2, help='cam postion in web page 1 or 2')
    parser.add_argument('--source', type=int, default=1, help='select cam')
    opt = parser.parse_args()
    return opt

if __name__ == "__main__":
    opt = parse_opt()
    run(**vars(opt))