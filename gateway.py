import socket
import signal
import sys
import struct
import time
from IP import IP

GATEWAY_IP_DEVICE_INTERFACE = IP("192.168.1.1", "255.255.255.0")
GATEWAY_IP_SERVER_INTERFACE = IP("10.10.10.1", "255.255.255.0")

GATEWAY_DEVICE_SIDE_PORT = 8000
GATEWAY_DEVICE_SIDE_ADDRESS = 'localhost'
SERVER_PORT = 8008
NUMBER_OF_DIFFERENT_CLIENTS = 4

def send_data_to_server(data_str):
    gateway_server_side = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Message = IP + SUBNET + START TIME + DATA
    start_time_encoded = struct.pack('f', time.perf_counter())
    message = GATEWAY_IP_SERVER_INTERFACE.encode_ip_and_subnet() + start_time_encoded + data_str.encode('utf-8')

    gateway_server_side.connect((GATEWAY_DEVICE_SIDE_ADDRESS, SERVER_PORT))
    gateway_server_side.send(message)
    gateway_server_side.close()

def kill_gateway(sig, frame):
    print('Gateway killed')
    gateway_devices_side.close()
    sys.exit(0)

gateway_devices_side = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
gateway_devices_side.bind(('localhost', GATEWAY_DEVICE_SIDE_PORT))

data_str = ''

signal.signal(signal.SIGINT, kill_gateway)

device_list = []

devices = 0
print('Listening for devices...')
while True:
    mess = gateway_devices_side.recv(1024)

    finish_time = time.perf_counter()

    #The first 4 bytes are the ip address of the sender
    source_ip = mess[:4]

    #The next 4 bytes are the subnet of the sender
    source_subnet = mess[4:8]

    #Creates the IP structure of the sending device
    ip_sender = IP.bytes_to_IP(source_ip, source_subnet)

    #Convert the 4 bytes into a float, which is the time the packet was sent
    start_time = struct.unpack('f', mess[8:12])


    #The remaining bytes are the encoded data
    payload = mess[12:]

    #Check if the device is in the same network
    if GATEWAY_IP_DEVICE_INTERFACE.is_in_same_network(ip_sender) and (ip_sender.ip not in device_list):
        print('Data received from {}'.format(ip_sender.ip))
        print("Total elapsed time for receiving the UDP packet: {}".format(finish_time - start_time[0]))
        decoded_payload = payload.decode('utf-8').split('\n')
        #Formatting data
        for entry in decoded_payload:
            if entry != '':
                data_str += ip_sender.ip + ' - ' + entry.replace(',', ' - ') + '\n'
        device_list.append(ip_sender.ip)
        if len(device_list) == NUMBER_OF_DIFFERENT_CLIENTS:
            print('Data received from all the devices')
            print('Sending data to server...')
            send_data_to_server(data_str)
            print('\n Listening for incoming data... \n')
            data_str = ''
            device_list = []
    else:
        print('Message received from a host in another network or has already sent data. Message discarded')