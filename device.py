import random
import datetime
import socket
from IP import IP

class device:
    def __init__(self, id, ip, gateway_address, gateway_port):
        self.id = id
        self.ip = ip
        self.gateway_address = gateway_address
        self.gateway_port = gateway_port
        self.mesurements_file = 'measures/measures_dev{}.csv'.format(self.id)

    def generate_random_measures(self, n_measures):
        f = open(self.mesurements_file, 'w')
        for i in range(n_measures):
            rand_time = datetime.time(random.randint(0, 23), 
                                        random.randint(0, 59),
                                        random.randint(0, 59))

            rand_temp = (int)(random.gauss(20, 5))
            rand_humidy = (int)(random.gauss(60, 5))
            f.write("{},{},{} \n".format(rand_time, rand_temp, rand_humidy))
        f.close()

    def read_measurements(self):
        file = open(self.mesurements_file)
        all_data = file.read()
        file.close()
        return all_data

    def send_data(self):
        gateway = (self.gateway_address, self.gateway_port)
        device = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        device.connect(gateway)

        #message = bytes(self.ip.ip_octets) + bytes(self.ip.subnet_octets) + self.read_measurements().encode('utf-8')
        message = self.ip.encode_ip_and_subnet() + self.read_measurements().encode('utf-8')
        device.send(message)
        device.close()
