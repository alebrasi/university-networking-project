import socket
import socket
from IP import IP

SERVER_IP = '10.10.10.2'
SERVER_SUBNET = '255.255.255.0'

ip = IP(SERVER_IP, SERVER_SUBNET)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8008))
server.listen(2)

while True:
    gateway_connection, address = server.accept()

    message = gateway_connection.recv(4096)

    #The first 4 bytes are the ip address of the sender
    source_ip = message[:4]

    #The next 4 bytes are the subnet of the sender
    source_subnet = message[4:8]

    #Creating the IP structure of the sending device
    ip_sender = IP.bytes_to_IP(source_ip, source_subnet)

    payload = message[8:]

    if ip.is_in_same_network(ip_sender):
        print('Data received from gateway {}:'.format(ip_sender.ip))
        s = payload.decode('utf-8').split('\n')
        for i, m in enumerate(s, 1):
            print('{}) {}'.format(i, m))
        
        gateway_connection.close()
        print('\n Listening for incoming data... \n')
    else:
        print('Message received from a host outside the network. Discarded.')
