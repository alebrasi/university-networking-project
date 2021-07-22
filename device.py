import random
import datetime
import socket
import os
import time
import struct
from IP import IP

class device:
    def __init__(self, id, ip):
        """
        Initialize a new device

        Parameters
        ----------
        id : int
            The id of the device
        ip : str
            The ip of the device
        """
        self.id = id
        self.ip = ip
        self.measurements_folder = 'measures'
        self.mesurements_file = '{}/measures_dev{}.csv'.format(self.measurements_folder, self.id)

    def generate_random_measures(self, n_measures):
        """
        Generates a csv file containing a number of random measurements

        Parameters
        ----------
        n_measurements : int
            The number of random measures to create
        """
        if not os.path.exists(self.measurements_folder):
            os.mkdir(self.measurements_folder)
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
        """
        Read the measurements made from the device
        """
        file = open(self.mesurements_file)
        all_data = file.read()
        file.close()
        return all_data

    def send_data(self, gateway_address, gateway_port):
        """
        Send the collected measurements to the gateway

        Parameters
        ----------
        gateway_address = IP
            The IP of the gateway
        gateway_port = IP
            The port of the gateway
        """
        gateway = (gateway_address, gateway_port)
        device = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        device.connect(gateway)

        #Encode the current time (double) into a byte array
        encoded_measures = self.read_measurements().encode('utf-8')
        start_time_encoded = struct.pack('d', time.perf_counter())
        #The message consists of the encoded ip and subnet mask, the encoded start time and the encoded measurements
        message = self.ip.encode_ip_and_subnet() + start_time_encoded + encoded_measures
        device.send(message)
        device.close()

    def print_info(self):
        """
        Prints the info of the device and the data that is going to send to the gateway
        """
        print('Device {} \nIP: {} \nSubnet: {} \n \nData to send: \n{}'
                .format(self.id, self.ip.ip, self.ip.subnet, self.read_measurements()))
