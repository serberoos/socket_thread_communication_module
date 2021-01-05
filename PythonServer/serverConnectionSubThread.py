import socket, threading
 
class ServerConnectionSubThread(threading.Thread):
    def __init__(self, connectionSubThreadList, clientConnectionList, clientConnection, clientAddress):
        threading.Thread.__init__(self) #스레드를 클래스로 정의 할 때는 __init__메소드는 부모 클래스의 생성자를 반드시 호출 해야함
 

        self.connectionSubThreadList = connectionSubThreadList
        self.clientConnectionList = clientConnectionList
        self.clientConnection = clientConnection
        self.clientAddress = clientAddress
        self.daemon =True;  #백그라운드 스레드(메인스레드 종료시 종료)
 

    def run(self):
        try:
            while True:
                data = self.clientConnection.recv(1024).decode() #연결된 클라이언트의 메세지를 기다린다.
 
                if not data: # 만약 클라이언트의 서버접속 해제시 recv()는 0을 리턴한다.
                    print("client_disconnect : ",self.clientConnection)
                    break
 
 
                print("from client : ", data)
                if data == "hi\n":
                    print("to client : ","hello\n")
                    try:
                        self.clientConnection.sendall("hello\n".encode())
                    except:
                        pass
                
                elif data =="hello\n":
                    print("to client : ", "hi\n")
                    try:
                        self.clientConnection.sendall("hi\n".encode())
                    except:
                        pass
                    
        except:
            self.clientConnectionList.remove(self.clientConnection)
            self.connectionSubThreadList.remove(self)
            exit(0)

        self.clientConnectionList.remove(self.clientConnection)
        self.connectionSubThreadList.remove(self)
       
 
   
        