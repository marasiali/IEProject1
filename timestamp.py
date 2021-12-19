import time

timestamp= round(time.time() * 1000)
print(timestamp)
# in miliseconds from epoch
data = b"voice"
#voice data from mic (byte array)
start_index = len(data)
#timestamp's starting bit in packet data
data+=int.to_bytes(timestamp,8,'big')
#covert timestamp to 8 bytes
#and add it to packet data
#send packet to server
#in server code get data from socket:
print(data[:start_index])
# get voice data from packet	
print(int.from_bytes(data[start_index:],'big'))
#get timestamp from packet

#send a packet with only this timestamp as ack to client ( singer )

# create thread for recieving data in singer.py
#in singer code compute latency when it receives ack of sent packets from server 
newtimestamp = round(time.time() * 1000)
latency = ( newtimestamp - timestamp)/2
print(latency)	