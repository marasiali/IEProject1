import socket, pyaudio
#import struct

MCAST_GRP = '224.1.1.1'
interface='192.168.1.4'
MCAST_PORT = 5007
IS_ALL_GROUPS = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if IS_ALL_GROUPS:
    # on this port, receives ALL multicast groups
    sock.bind(('', MCAST_PORT))
else:
    # on this port, listen ONLY to MCAST_GRP
    sock.bind((MCAST_GRP, MCAST_PORT))
#mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
mreq = socket.inet_aton(MCAST_GRP) + socket.inet_aton(interface)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

chunk_size = 512
audio_format = pyaudio.paInt16
channels = 1
rate = 44100

p = pyaudio.PyAudio()
playing_stream = p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)

while True:

    try:
        data,addr = sock.recvfrom(1024)
        playing_stream.write(data)
        print(str(len(data))+" bytes received from "+str(addr))
    except Exception as e:
        print("1 "+str(e))
