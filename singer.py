from math import ceil
import socket
import pyaudio
import wave
import time
import random
import threading


class Client:
    
    def __init__(self):
        self.audio_folder = './audio/'
        self.audio_format = pyaudio.paInt16
        self.chunk_size = 252
        self.buffer_size = 512   
        self.channels = 1
        self.rate = 44100
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       
        while True:
            try:
                """ self.server_ip = input('enter IP address of server: ')
                self.server_port = int(input('enter target port of server: '))
                self.file_name = input('enter .wav file name from audio folder: ') """
                self.server_ip = '192.168.43.138'
                self.server_port = 8081
                self.file_name = 'a.wav'
                break
            except:
                print('incorrect input')

        #self.wave_file = wave.open(self.audio_folder + self.file_name, 'rb')
        self.p = pyaudio.PyAudio()
        self.recording_stream = self.p.open(
            format=self.audio_format, 
            channels=self.channels, 
            rate=self.rate, 
            input=True, 
            frames_per_buffer=self.chunk_size)
            
    def send(self):
        #data = self.wave_file.readframes(self.chunk_size)
        #sample_rate = self.wave_file.getframerate()
        while True:
            try:
                data = self.recording_stream.read(self.chunk_size)
                timestamp = round(time.time() * 1000)
                data += int.to_bytes(timestamp, 8, 'big')
                delay = random.randint(0, 80) / 1000
                #time.sleep(delay)
                #time.sleep(0.8 * self.chunk_size / sample_rate)
                self.socket.sendto(data, (self.server_ip, self.server_port))
                
                #print('this is delay from client ', delay)
                #print(str(len(data)) + ' bytes sent to ' + str(self.server_ip))
                #data = self.wave_file.readframes(self.chunk_size)
            except Exception as e:
                print('sending data to server failed: ' + str(e))

    def receive_delay_feedback(self):
        """ while True:
            data, addr = self.socket.recvfrom(1)
            if data == b'd':
                print('you have delay') """
        
        while True:
            data, addr = self.socket.recvfrom(self.buffer_size)
            newtimestamp = round(time.time() * 1000)
            latency = (newtimestamp - int.from_bytes(data, 'big'))
            if latency > 50:
                print('your delay is:', latency, 'ms and it is high')	
            else:
                print('your delay is:', latency, ' ms and it is low')


def main():
    client = Client()
    receiving_thread = threading.Thread(target=client.receive_delay_feedback)
    receiving_thread.start()
    client.send()

if __name__ == '__main__':
    main()