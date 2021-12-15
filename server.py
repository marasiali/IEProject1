#!/usr/bin/python3

import socket
import threading

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
MULTICAST_TTL = 2

class Server:
    def __init__(self):
            #self.ip = socket.gethostbyname(socket.gethostname())
            #self.ip = "192.168.1.4"
            while 1:
                try:
                    self.ip = input('Enter server IP : ')
                    self.port = int(input('Enter server port number : '))

                    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    self.s.bind((self.ip, self.port))

                    break
                except:
                    print("Couldn't bind to that IP and port")

            self.mc_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.mc_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
            while 1:
                try:
                    data,addr = self.s.recvfrom(1024)
                    self.multicast(data)
                
                except Exception as e:
                    print("1 "+str(e))
       
    def multicast(self, data):
        try:
            self.mc_sock.sendto(data, (MCAST_GRP, MCAST_PORT))
            print(str(len(data))+" bytes sent")
        except Exception as e:
            print("2 "+str(e))

        

server = Server()
