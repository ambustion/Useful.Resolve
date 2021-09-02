import socket
import struct
import binascii
import time
TCP_IP = '127.0.0.1'
TCP_PORT = 9060
BUFFER_SIZE = 1024

def convertBinaryTC(data):
    tc = struct.unpack("5B", data)
    tc = tc[1:]
    timecode = list(tc)
    tc2 = []
    for x in timecode:
        x = str(str(x).zfill(2))
        tc2.append(x)
    tc3 = ":".join(tc2)
    print(tc3)
    return tc3

def connect():
    MESSAGE=b'connect'
    Mlen = len(MESSAGE)
    mLenbytes=struct.pack("i" , Mlen)
    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.connect((TCP_IP , TCP_PORT))
        s.send(mLenbytes)
        s.send(MESSAGE)
        #s.send(M2)

        # print(send)
        data=s.recv(BUFFER_SIZE)
    print('Received' , repr(data))

def gettc():

    MESSAGE=b'gettc'
    Mlen=len(MESSAGE)
    mLenbytes=struct.pack("i" , Mlen)
    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.setsockopt(socket.IPPROTO_TCP , socket.TCP_NODELAY , 1)
        ls = []
        s.connect((TCP_IP , TCP_PORT))
        s.sendall(mLenbytes)
        s.sendall(MESSAGE)
        time.sleep(1)
        data=s.recv(BUFFER_SIZE)
    print('Received' , repr(data))
    tc = convertBinaryTC(data)
def play():

    MESSAGE=b'play'
    Mlen = len(MESSAGE)
    mLenbytes=struct.pack("i" , Mlen)
    speed = struct.pack("f" , 1)
    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.connect((TCP_IP , TCP_PORT))
        s.send(mLenbytes)
        s.send(MESSAGE)
        s.send(speed)
        time.sleep(1)
        data=s.recv(BUFFER_SIZE)
    print('Received' , repr(data))
def settc(timecode):

    MESSAGE=b'goto'
    tc = timecode.split(":")
    print(tc)
    sendtc=[]

    #sendtc=b''.join(sendtc)
    print(sendtc)
    Mlen=len(MESSAGE)
    mLenbytes=struct.pack("i" , Mlen)
    # m2 = struct.pack("B" , MESSAGE)

    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.setsockopt(socket.IPPROTO_TCP , socket.TCP_NODELAY , 1)

        ls=[]
        s.connect((TCP_IP , TCP_PORT))

        s.sendall(mLenbytes)
        s.sendall(MESSAGE)
        print(sendtc)
        for x in tc:
            #x=struct.pack("B" , int(x))
            newx = bytes(x,'utf-8')

            #newx = struct.pack("B" , x)


            sendtc.append(newx)
            print(newx)
            #s.sendall(newx)
        sendtc = struct.pack("4B" ,int(sendtc[0]),int(sendtc[1]),int(sendtc[2]),int(sendtc[3]))
        s.sendall(sendtc)
        print(sendtc)
        time.sleep(1)
        data=s.recv(BUFFER_SIZE)
    print('Received' , repr(data))




connect()
gettc()
#settc("01:00:00:00")
#play()
