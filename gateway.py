import socket
from IP import IP

GATEWAY_IP_DEVICE_INTERFACE = IP("192.168.1.1", "255.255.255.0")
GATEWAY_IP_SERVER_INTERFACE = IP("10.10.10.1", "255.255.255.0")

GATEWAY_DEVICE_SIDE_PORT = 8000
SERVER_PORT = 8008

def send_data_to_server(data_str):
    gateway_server_side = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    message = GATEWAY_IP_SERVER_INTERFACE.encode_ip_and_subnet() + data_str.encode()

    gateway_server_side.connect(('localhost', SERVER_PORT))
    gateway_server_side.send(message)
    gateway_server_side.close()

gateway_devices_side = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
gateway_devices_side.bind(('localhost', GATEWAY_DEVICE_SIDE_PORT))

data_str = ''

devices = 0
while True:
    mess = gateway_devices_side.recv(4096)

    #The first 4 bytes are the ip address of the sender
    source_ip = mess[:4]

    #The next 4 bytes are the subnet of the sender
    source_subnet = mess[4:8]

    #Creating the IP structure of the sending device
    ip_sender = IP.bytes_to_IP(source_ip, source_subnet)

    payload = mess[8:]

    #Check if the device is in the same network
    if GATEWAY_IP_DEVICE_INTERFACE.is_in_same_network(ip_sender):
        print('Data received from {}'.format(ip_sender.ip))
        s = payload.decode('utf-8').split('\n')
        #Formatting data
        for n in s:
            if n != '':
                data_str += ip_sender.ip + ' - ' + n.replace(',', ' - ') + '\n'
        devices += 1
        if devices == 4:
            print('Data received from all the devices')
            print('Sending data to server...')
            send_data_to_server(data_str)
            print('\n Listening for incoming data... \n')
            data_str = ''
            devices = 0
    else:
        print('Message received from a host in another network. Discarded')

