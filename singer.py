import socket
import pyaudio
import time
import threading


class Client:
    
    def __init__(self):
        self.audio_format = pyaudio.paInt16
        self.chunk_size = 252
        self.buffer_size = 512   
        self.channels = 1
        self.rate = 44100
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timestamp_data_size = 8
       
        while True:
            try:
                self.server_ip = input('enter IP address of server: ')
                self.server_port = int(input('enter target port of server: '))
                break
            except:
                print('incorrect input')

        self.socket.sendto(b'Hello', (self.server_ip, self.server_port))
        self.p = pyaudio.PyAudio()
        self.recording_stream = self.p.open(
            format=self.audio_format, 
            channels=self.channels, 
            rate=self.rate, 
            input=True, 
            frames_per_buffer=self.chunk_size)
            
    def send(self):
        while True:
            try:
                data = self.recording_stream.read(self.chunk_size)
                timestamp = round(time.time() * 1000)
                data += int.to_bytes(timestamp, self.timestamp_data_size, 'big')
                self.socket.sendto(data, (self.server_ip, self.server_port))
            except Exception as e:
                print('sending data to server failed: ' + str(e))

    def receive_delay_feedback(self):
        lastTimestamp = 0
        while True:
            data, addr = self.socket.recvfrom(self.buffer_size)
            newtimestamp = round(time.time() * 1000)
            latency = (newtimestamp - int.from_bytes(data, 'big'))
            if (newtimestamp - lastTimestamp) >= 1000 :
                if latency >= 100:
                    print('your delay is:', latency, 'ms and it is high')	
                else:
                    print('your delay is:', latency, ' ms and it is low')
                lastTimestamp = newtimestamp


def main():
    client = Client()
    receiving_thread = threading.Thread(target=client.receive_delay_feedback)
    receiving_thread.start()
    client.send()

if __name__ == '__main__':
    main()
