import os
import time

import cv2
import numpy as np

imgPath = ".yolov5/od_imgs/"
if not os.path.exists(imgPath):
    os.makedirs(imgPath)

num = 2000
times = 0
cap = cv2.VideoCapture(2)

time.sleep(3)

while(times<500):
    # get a frame
    ret, frame = cap.read()

    imgName = imgPath + str(num) + ".png"
    # print(imgName)
    num = num + 1
    times = times + 1
    # show a frame
    cv2.imwrite(imgName,frame)
    # frame = cv2.flip(frame, -1)

    # cropImg = frame[:y_end, x_start:x_end]
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # time.sleep(0.2)
cap.release()
cv2.destroyAllWindows()
# import os
#
# img_list = os.listdir(imgPath)
# num = 2400
# for img_item in img_list:
#     img_path = os.path.join(imgPath, img_item)
#     img = cv2.imread(img_path)
#     x = cv2.flip(img, 0)
#     cv2.imshow("capture", x)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#     cv2.imwrite(imgPath+"open_"+str(num)+"_flipx.png", x)
#     num = num + 1
#     y = cv2.flip(img, 1)
#     cv2.imwrite(imgPath+"open_"+str(num)+"_flipy.png", y)
#     num = num + 1
#     xy = cv2.flip(img, -1)
#     cv2.imwrite(imgPath+"open_"+str(num)+"_flipxy.png", xy)
#     num = num + 1


