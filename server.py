import socket


class Server:
    
    def __init__(self):
        self.MCAST_GRP = '224.1.1.1'
        self.MCAST_PORT = 5007
        self.MULTICAST_TTL = 2
        
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
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                self.send_multicast(data)
                print(str(len(data)) + ' bytes received from ' + str(addr))
            except Exception as e:
                print('receiving data from client ' + str(addr) + ' failed: ' + str(e))
       
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