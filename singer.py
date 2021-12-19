import socket
import pyaudio
import wave


class Client:
    
    def __init__(self):
        self.audio_folder = './audio/'
        self.chunk_size = 512   
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       
        while True:
            try:
                self.server_ip = input('enter IP address of server: ')
                self.server_port = int(input('enter target port of server: '))
                self.file_name = input('enter .wav file name from audio folder: ')
                break
            except:
                print('incorrect input')

        self.wave_file = wave.open(self.audio_folder + self.file_name, 'rb')
        
        self.pyaudio = pyaudio.PyAudio()
        self.recording_stream = self.pyaudio.open(
            format=self.get_format_from_width(self.wave_file.getsampwidth()), 
            channels=self.wave_file.getnchannels(), 
            rate=self.wave_file.getframerate(), 
            input=True, 
            frames_per_buffer=self.chunk_size)

            
    def send(self):
        data = self.wave_file.readframes(self.chunk_size)
        while data != b'':
            try:
                self.socket.sendto(data, (self.server_ip, self.server_port))
                print(data)
                print(str(len(data)) + ' bytes sent to ' + str(self.server_ip))
                data = self.wave_file.readframes(self.chunk_size)
            except Exception as e:
                print('sending data to server failed: ' + str(e))


def main():
    client = Client()
    client.send()

if __name__ == '__main__':
    main()