import serverSocketMainThread #서버 소켓과 서버 메인스레드

serverSocketMainThread = serverSocketMainThread.ServerSocketMainThread("192.168.200.121", 7777)
serverSocketMainThread.start() #서버 스레드 시작 serverSocketMainThread의 run() 시작


