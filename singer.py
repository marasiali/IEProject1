#!/usr/bin/python3

import socket
import threading
import pyaudio

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.server_ip="192.168.1.4"
        while 1:
            try:
                self.server_ip = input('Enter IP address of server --> ')
                self.server_port = int(input('Enter target port of server --> '))
                break
            except:
                print("Incorrect input")

        chunk_size = 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 44100

        self.p = pyaudio.PyAudio()
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
        print("Sending your voice ...")
        self.send_data_to_server()
            

    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(512)
                self.s.sendto(data,(self.server_ip,self.server_port))
            except Exception as e:
                print("2 "+str(e))

client = Client()
