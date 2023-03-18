import redis
import socket

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=False)
r = redis.Redis(connection_pool=pool)

Udp_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Udp_Socket.bind(("", 5005))
Udp_Socket.settimeout(50)

while True:

    try:
        data, address = Udp_Socket.recvfrom(10240000)
        r.set('CAM' + str(data[0]), data[1:], px=30)
    except socket.timeout:
        print('Timed out, no data received')



