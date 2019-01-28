import socket, numpy, cv2 , threading

sockArr = numpy.array([])
mp = {}
busy = {}

def sendVideo(sock, video):
    sock.send(video) 

        
def clientHandler(sock,addr):
    while(True):
        msg = sock.recv(1024).decode()
        print(str(msg),'F')
        if str(msg) == 'ConnectRep':
            replyMsg = str(sock.recv().decode())
            print(replyMsg)
            if replyMsg == 'Accepted':
                    ip = str(sock.recv().decode())
                    print(ip)
                    mp[ip].send(bytes('ConnectRep','utf-8'))  
                    mp[ip].send(bytes(replyMsg,'utf-8')) 
        if str(msg) == 'ConnectReq':
            ip = str(sock.recv(1024).decode())
            print(ip)
            if ip in mp:    
                mp[ip].send(bytes(msg,'utf-8'))
                mp[ip].send(bytes(addr[0],'utf-8'))
            else:
                mp[addr[0]].send(b"Not Online")
                
        elif str(msg) == 'Video':
            ip = str(sock.recv(1024).decode())
            print(ip)
            while True:
                videoBytes = sock.recv(921600)
                mp[ip].send(videoBytes)
        
        elif str(msg) == 'Message':
            ip = str(sock.recv(1024).decode())
            print(ip)
            while True:
                msg = sock.recv(1024)
                mp[ip].send(bytes(msg,'utf-8'))
    

def startServer():
    global sockArr
    s = socket.socket()		 
    print ("Socket successfully created")
    port = 12346				
    s.bind((socket.gethostname(), port))		 
    print ("socket binded to %s" %(port) ) 
    s.listen(10)	 
    print ("socket is listening") 
    while True:
        sock, addr = s.accept()
        print ('Got connection from', addr )
        sockArr = numpy.append(sockArr,sock)
        mp[addr[0]] = sock		
        t1 = threading.Thread(target=clientHandler, args=(sock,addr,))
        t1.start()
    
startServer()
