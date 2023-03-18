import redis
from django.http import StreamingHttpResponse
from django.shortcuts import render

r = redis.Redis(host='localhost', port=6379, decode_responses=False)


def getmonitor(request, camNo):
    return StreamingHttpResponse(gen(camNo),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def gen(camNo):
    while True:

        try:
            last_frame = r.get('CAM' + str(camNo))
            # print(len(last_frame))
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + last_frame + b'\r\n\r\n')
        except:
            continue
