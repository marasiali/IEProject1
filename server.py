import socket


class Server:
    
    def __init__(self):
        self.MCAST_GRP = '224.1.1.1'
        self.MCAST_PORT = 5007
        self.MULTICAST_TTL = 2
        self.clients = []
        self.timestamp_size = 8
        self.buffer_size = 512
        self.ack_data_size = 8

        while True:
            try:
                self.ip = input('enter server IP: ')
                self.port = int(input('enter server port number: '))

                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock.bind((self.ip, self.port))
                break
            except:
                print("Couldn't bind to that IP and port")

        self.mc_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.mc_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.MULTICAST_TTL)
        
    def run(self):  
        print('server is running ...')  
        while True:
            try:
                data, addr = self.sock.recvfrom(self.buffer_size)
                ack_data = data[-self.ack_data_size:]
                mc_data = data[:-self.ack_data_size]
                self.send_ack(ack_data, addr)
                self.send_multicast(mc_data)
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

        
def main():
    server = Server()
    server.run()

if __name__ == '__main__':
    main()
