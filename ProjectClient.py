import socket,numpy,cv2	 
import threading

port = 12346
ip = "172.31.84.186"
sock = None
accepted = False
to = None
def recvVideo():
    while True:
        try:
            arr2 = sock.recv(921600)
            arr2 = numpy.frombuffer(arr2, dtype='uint8')
            print ( arr2 ) 
            arr3 = arr2.reshape((480,640,3))
            cv2.imshow('Image',arr3)
            key=cv2.waitKey(1)
            if key==ord('q'):
                break
        except:
            pass

def recv():
    global accepted,to,sock
    while(True):
        msg = str(sock.recv(1024).decode())
        print(msg)
        if msg == 'ConnectReq':
            ip = str(sock.recv(1024).decode())
            print(ip)
            to = ip
            sock.send(bytes('ConnectRep ','utf-8'))
            sock.send(bytes('Accepted ','utf-8'))
            sock.send(bytes(ip,'utf-8'))
            accepted = True
        if msg == 'Message':
            print(msg)
        if msg == 'ConnectRep':
            msg = str(sock.recv(1024).decode())
            if(msg == 'Accepted'):
                accepted = True
            else:
                to = None
            
    
def startClient():
    global ip,port,sock,to
    sock = socket.socket()					 
    sock.connect((ip, port))  
    print("Successfully Connected")
    t1 = threading.Thread(target=recv)
    t1.start()
    opt= int(input("Enter Option"));
    if(opt==1):
        sock.send(b'ConnectReq')
        to = '172.31.84.186'
        sock.send(bytes(to,'utf-8'))
    while to == None or accepted==False:
         pass
    while(True):
        text = input("What do you want to say")
        sock.send(bytes(text,'utf-8'))
    t1.join()

startClient()