import socket
import signal
import sys
import time
import struct
from IP import IP

SERVER_IP = '10.10.10.2'
SERVER_SUBNET = '255.255.255.0'
SERVER_PORT = 8008

ip = IP(SERVER_IP, SERVER_SUBNET)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', SERVER_PORT))
server.listen(2)

def kill_server(sig, frame):
    print('Server killed')
    server.close()
    sys.exit(0)

signal.signal(signal.SIGINT, kill_server)

print('Listening for incoming data...')

while True:
    gateway_connection, address = server.accept()

    finish_time = time.perf_counter()

    message = gateway_connection.recv(4096)

    #The first 4 bytes are the ip address of the sender
    source_ip = message[:4]

    #The next 4 bytes are the subnet of the sender
    source_subnet = message[4:8]

    #Creates the IP structure of the sending device
    ip_sender = IP.bytes_to_IP(source_ip, source_subnet)

    #Convert the 4 bytes into a float, which is the time the packet was sent
    start_time = struct.unpack('f', message[8:12])

    #The remaining bytes are the encoded data
    payload = message[12:]

    if ip.is_in_same_network(ip_sender):
        print('Data received from gateway {}:'.format(ip_sender.ip))
        print("Total elapsed time for receiving the TCP packet: {}".format(finish_time - start_time[0]))
        decoded_payload = payload.decode('utf-8').split('\n')
        for i, entry in enumerate(decoded_payload, 1):
            print('{}) {}'.format(i, entry))
        
        gateway_connection.close()
        print('\n Listening for incoming data... \n')
    else:
        print('Message received from a host outside the network. Discarded.')
