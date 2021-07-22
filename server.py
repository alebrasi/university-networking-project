import socket
import signal
import sys
import time
import struct
from IP_Address import IP_Address

SERVER_IP = '10.10.10.2'
SERVER_SUBNET = '255.255.255.0'
SERVER_PORT = 8008
BUFFER_SIZE = 2048

def kill_server(sig, frame):
    print('Server killed')
    server.close()
    sys.exit(0)

ip = IP_Address(SERVER_IP, SERVER_SUBNET)

print('Server started. Buffer size: {} bytes \n'.format(BUFFER_SIZE))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', SERVER_PORT))
server.listen(2)

signal.signal(signal.SIGINT, kill_server)

print('Listening for incoming data...')

try:
    while True:
        gateway_connection, address = server.accept()


        message = gateway_connection.recv(BUFFER_SIZE)
        finish_time = time.perf_counter()

        #The first 4 bytes are the ip address of the sender
        source_ip = message[:4]

        #The next 4 bytes are the subnet of the sender
        source_subnet = message[4:8]

        #Creates the IP_Address structure of the sending device
        ip_sender = IP_Address.bytes_to_IP(source_ip, source_subnet)
        
        print('Accepted connection from {}'.format(ip_sender.ip))

        #Convert the 8 bytes into a double, which is the time the packet was sent
        start_time = struct.unpack('d', message[8:16])

        #The remaining bytes are the encoded data
        payload = message[16:]

        if ip.is_in_same_network(ip_sender):
            print('Data received from gateway {}'.format(ip_sender.ip))
            print('Total elapsed time for receiving the TCP packet: {} seconds'.format(finish_time - start_time[0]))
            try:
                print('\nMeasurements received: \n')
                decoded_payload = payload.decode('utf-8').split('\n')

                for i, entry in enumerate(decoded_payload, 1):
                    if entry != '':
                        print('{}) {}%'.format(i, entry))

                gateway_connection.close()
                print('\nListening for incoming data... \n')
            except Exception as e:
                print(e)
        else:
            print('Message received from a host outside the network. Discarded.')
except Exception as e:
    print(e)
finally:
    gateway_connection.close()
    server.close()