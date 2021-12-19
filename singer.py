import socket
import pyaudio


class Client:
    
    def __init__(self):
        self.chunk_size = 512
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       
        while True:
            try:
                self.server_ip = input('enter IP address of server: ')
                self.server_port = int(input('enter target port of server: '))
                break
            except:
                print('incorrect input')

        self.pyaudio = pyaudio.PyAudio()
        self.recording_stream = self.pyaudio.open(
            format=self.audio_format, 
            channels=self.channels, 
            rate=self.rate, 
            input=True, 
            frames_per_buffer=self.chunk_size)
            
    def send(self):
        while True:
            try:
                data = self.recording_stream.read(512)
                self.socket.sendto(data, (self.server_ip, self.server_port))
                print(str(len(data)) + ' bytes sent to ' + str(self.server_ip))
            except Exception as e:
                print('sending data to server failed: ' + str(e))


def main():
    client = Client()
    client.send()

if __name__ == '__main__':
    main()