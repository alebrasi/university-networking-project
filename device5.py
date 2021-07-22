from device import device
from IP_Address import IP_Address

N_MEASURES = 4
IP_ADDRESS_DEVICE = "192.168.1.6"
SUBNET_MASK_DEVICE = "255.255.254.0"
GATEWAY_ADDRESS = 'localhost'
GATEWAY_PORT = 8000
ID = 5

ip = IP_Address(IP_ADDRESS_DEVICE, SUBNET_MASK_DEVICE)

dev = device(ID, ip)

dev.generate_random_measures(N_MEASURES)
dev.print_info()
dev.send_data(GATEWAY_ADDRESS, GATEWAY_PORT)