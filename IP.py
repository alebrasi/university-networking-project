class IP:
    def __octet_splitter(self, ip):
        octets = []
        for octet in ip.split("."):
            octets.append(int(octet))
        return octets

    def __init__(self, ip, subnet):
        self.ip = ip
        self.subnet = subnet
        self.ip_octets = self.__octet_splitter(ip)
        self.subnet_octets = self.__octet_splitter(subnet)

    def is_in_same_network(self, ip):
        for i in range(4):
            if (self.ip_octets[i] & self.subnet_octets[i]) != (ip.ip_octets[i] & ip.subnet_octets[i]):
                return False
        return True

    def get_ip_in_byte_array(self):
        byte_array = []
        for octet in self.ip_octets:
            byte_array.append(bytes(octet))
        return byte_array

    def encode_ip_and_subnet(self):
        return bytes(self.ip_octets) + bytes(self.subnet_octets)

    def bytes_to_IP(ip_bytes, subnet_bytes):
        ip_str = ''
        subnet_str = ''
        for i in range(4):
            ip_str += str(ip_bytes[i]) + ('.' if i < 3 else '')
            subnet_str += str(subnet_bytes[i]) + ('.' if i < 3 else '')
        return IP(ip_str, subnet_str)