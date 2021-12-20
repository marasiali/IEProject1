import socket
import pyaudio
import struct


class Client():

    def __init__(self): 
        self.MCAST_GRP = '224.1.1.1'
        self.MCAST_PORT = 5007
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.MCAST_PORT))
        
        mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        """ self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('192.168.43.138', 6968)) """
        self.chunk_size = 252
        self.buffer_size = 512
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100

        self.pyaudio = pyaudio.PyAudio()
        self.playing_stream = self.pyaudio.open(
            format=self.audio_format, 
            channels=self.channels, 
            rate=self.rate, 
            output=True, 
            frames_per_buffer=self.chunk_size)

    def receive(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(self.buffer_size)
                self.playing_stream.write(data)
                print(str(len(data)) + ' bytes received from ' + str(addr))
            except Exception as e:
                print('receiving data from server failed: ' + str(e))


def main():
    client = Client()
    client.receive()

if __name__ == '__main__':
    main()