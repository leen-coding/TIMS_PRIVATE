call conda activate yolov5

start python udp_camClient.py --targetIP 10.167.98.208 --source 0 --camPosition 1

start python .\yolov5\yolov5\detect.py --targetIP 10.167.98.208 --source 1 --camPosition 2
