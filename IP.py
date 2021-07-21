class IP:
    def __octet_splitter(self, ip):
        """
        Split an ip into octets

        Attributes
        ----------
        ip : str
            The ip in string format
        """
        octets = []
        for octet in ip.split("."):
            octets.append(int(octet))
        return octets

    def __init__(self, ip, subnet):
        """
        Creates an IP

        Attributes
        ----------
        ip : str
            The ip in string format
        subnet : str
            The subnet in string format
        """
        self.ip = ip
        self.subnet = subnet
        self.ip_octets = self.__octet_splitter(ip)
        self.subnet_octets = self.__octet_splitter(subnet)

    def is_in_same_network(self, ip):
        """
        Checks if an IP is in the same network

        Attributes
        ----------
        ip : IP
            The IP to check
        """
        for i in range(4):
            if (self.ip_octets[i] & self.subnet_octets[i]) != (ip.ip_octets[i] & ip.subnet_octets[i]):
                return False
        return True

    def encode_ip_and_subnet(self):
        """
        Encodes the ip and the subnet mask
        """
        return bytes(self.ip_octets) + bytes(self.subnet_octets)

    def bytes_to_IP(ip_bytes, subnet_bytes):
        """
        Creates an IP given the ip and the subnet mask in bytes

        Attributes
        -----------
        ip_bytes : byte
            The ip in bytes
        subnet_bytes : byte
            The subnet mask in bytes
        """
        ip_str = ''
        subnet_str = ''
        for i in range(4):
            ip_str += str(ip_bytes[i]) + ('.' if i < 3 else '')
            subnet_str += str(subnet_bytes[i]) + ('.' if i < 3 else '')
        return IP(ip_str, subnet_str)