from IP import IP
from device import device

N_MEASURES = 4
IP_ADDRESS_DEVICE = "192.168.1.3"
SUBNET_DEVICE = "255.255.255.0"
GATEWAY_ADDRESS = 'localhost'
GATEWAY_PORT = 8000
ID = 1

ip = IP(IP_ADDRESS_DEVICE, SUBNET_DEVICE)

dev = device(ID, ip, GATEWAY_ADDRESS, GATEWAY_PORT)

dev.generate_random_measures(N_MEASURES)
dev.send_data()