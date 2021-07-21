from device import device
from IP import IP

N_MEASURES = 4
IP_ADDRESS_DEVICE = "192.168.1.2"
SUBNET_DEVICE = "255.255.255.0"
GATEWAY_ADDRESS = 'localhost'
GATEWAY_PORT = 8000
ID = 1

ip = IP(IP_ADDRESS_DEVICE, SUBNET_DEVICE)

dev = device(ID, ip, GATEWAY_ADDRESS, GATEWAY_PORT)

dev.generate_random_measures(N_MEASURES)
dev.read_measurements()
dev.send_data()

"""
def generate_random_measures():
    f = open('measures/measures_dev{}.csv'.format(ID), 'w')
    for i in range(N_MEASURES):
        rand_time = datetime.time(random.randint(0, 23), 
                                    random.randint(0, 59),
                                    random.randint(0, 59))

        rand_temp = (int)(random.gauss(20, 5))
        rand_humidy = (int)(random.gauss(60, 5))
        f.write("{}, {}, {} \n".format(rand_time, rand_temp, rand_humidy))
    f.close()

generate_random_measures()

gateway = (GATEWAY_ADDRESS, GATEWAY_PORT)
device = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
device.connect(gateway)

message = bytes(ip.ip_octets) + bytes(ip.subnet_octets) + 'rozzi'.encode('utf-8')

device.send(message)
device.close()
"""