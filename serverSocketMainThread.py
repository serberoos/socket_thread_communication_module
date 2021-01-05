import socket, threading
import serverConnectionSubThread

class ServerSocketMainThread(threading.Thread):
    def __init__(self, HOST, PORT):
        threading.Thread.__init__(self) #부모클래스의 생성자 호출(threading.Thread)

        self.HOST = HOST
        self.PORT = PORT

        self.chatBotServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chatBotServerSocket.bind((self.HOST, self.PORT))
        self.chatBotServerSocket.listen(1)
        
        self.clientConnectionList = []
        self.connectionSubThreadList = []

    def run(self):
        try:
            while True:
                print("Waiting Client Connection") #클라이언트 접속대기
                clientConnection, clientAddress = self.chatBotServerSocket.accept() #클라이언트 접속
                self.clientConnectionList.append(clientConnection)  #접속한 클라이언트의 소켓 정보를 리스트에 추가

                print("connect at ", clientAddress)
    
                connectionSubThread = serverConnectionSubThread.ServerConnectionSubThread(self.connectionSubThreadList, self.clientConnectionList, clientConnection, clientAddress)
                connectionSubThread.start() #접속한 해당 클라이언트의 서브스레드를 시작
                self.connectionSubThreadList.append(connectionSubThread) #시작된 서브 스레드 리스트에 추가

        except:
            print("serverThread error")
 
  