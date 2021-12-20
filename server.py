import socket
import time


class Server:
    
    def __init__(self):
        self.MCAST_GRP = '224.1.1.1'
        self.MCAST_PORT = 5007
        self.MULTICAST_TTL = 2
        self.clients = []
        self.timestamp_size = 8
        self.buffer_size = 512

        while True:
            try:
                """ self.ip = input('enter server IP: ')
                self.port = int(input('enter server port number: ')) """
                self.ip = '192.168.43.138'
                self.port = 8081

                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock.bind((self.ip, self.port))

                break
            except:
                print("Couldn't bind to that IP and port")

        self.mc_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.mc_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.MULTICAST_TTL)
        
    def run(self):    
        while True:
            try:
                data, addr = self.sock.recvfrom(self.buffer_size)
                #start_index = len(data) - self.timestamp_size - 1
                ack_data = data[-8:]
                print('ack data', int.from_bytes(ack_data, 'big'))
                mc_data = data[:-8]
                self.send_ack(ack_data, addr)
                """ client = Client.get_or_create(addr[0], addr[1])
                delay = client.get_delay()
                if delay > Client.threshold:
                    self.send_delay_feedback(client) """
                
                #print('this is delay from server ', delay)
                self.send_multicast(mc_data)
                """ self.sock.sendto(mc_data, ('192.168.43.138', 6968))
                self.sock.sendto(mc_data, ('192.168.43.23', 6968)) """
                print(str(len(data)) + ' bytes received from ' + str(addr))
            except Exception as e:
               print('receiving data from client ' + str(addr) + ' failed: ' + str(e))

    def send_ack(self, data, addr):
        self.sock.sendto(data, addr)   

    def send_multicast(self, data):
        try:
            self.mc_sock.sendto(data, (self.MCAST_GRP, self.MCAST_PORT))
            print(str(len(data)) + ' bytes sent to ' + str(self.MCAST_GRP))
        except Exception as e:
            print('sending multicast data failed: ' + str(e))

    def send_delay_feedback(self, client):
        data = b'd'
        self.sock.sendto(data, (client.ip, client.port))


class Client():

    connected_clients = []
    threshold = 0.05

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.last_packet_timestamp = None

    @classmethod
    def get_or_create(cls, ip, port) -> 'Client':
        print('size ', len(cls.connected_clients))
        for client in cls.connected_clients:
            if client.ip == ip and client.port == port:
                return client
        client = cls(ip, port)
        cls.connected_clients.append(client)
        return client

    def get_delay(self):
        if self.last_packet_timestamp == None:
            self.last_packet_timestamp = time.time()
            return 0
        else:
            real_time = time.time()
            delay = real_time - self.last_packet_timestamp
            self.last_packet_timestamp = real_time
            """ print('real time ', real_time)
            print('delat ', delay)
            print('last packet updated ', self.last_packet_timestamp) """
            return delay 

        
def main():
    server = Server()
    server.run()

if __name__ == '__main__':
    main()
