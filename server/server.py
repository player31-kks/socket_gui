import socket
import threading 
from UserManager import UserManager
import time

HOST =""
PORT =9000
HEADER =64
FORMAT ="utf-8"
DISCONNECT_MSG ="[!EXIT]"
FILE_HEADER="[FILE]"
MESSAGE_HEADER="[MESG]"
bf_size = 65536

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
user = UserManager()



def runServer():
    print("============채팅서버를 시작합니다.============")
    server.listen()
    print("[LISTENING] server is listening")
    while True:
        conn,addr=server.accept()
        client_info = conn.recv(1024).decode()
        username,password=client_info.split('/')
        #### user 추가하기
        case=user.addUser(username,password,conn,addr)
        if case==1:
            conn.sendall("환영".encode())
            thread = threading.Thread(target=handle_client,args=(username,conn,addr))
            thread.demon=True
            thread.start()
        elif case==2:
            conn.sendall("비틀림".encode())
        elif case==3:
            conn.sendall("아중복".encode())
        elif case==4:
            conn.sendall("환영".encode())
            thread = threading.Thread(target=handle_client,args=(username,conn,addr))
            thread.demon=True
            thread.start()
            
            
            

def handle_client(username,conn,addr):
    print(f"[NEW connection ] {addr} connected")
    connected = True
    while connected:
        try:
            msg = conn.recv(10).decode(FORMAT)
            if msg ==DISCONNECT_MSG:
                connected=False
                print(f"[{addr}] {msg}")

            if msg == FILE_HEADER:
                #===================파일 헤더 와 info 정보받기===================
                file_info = conn.recv(bf_size).decode()
                #===================파일 정보 보내기 (서버 -> 전체 클라)===================
                user.sendMessageToAll(file_info,2)
                #===================파일 보내기 (서버 -> 전체 클라)===================
                fileSize = int(file_info.split(',')[0])
                count=fileSize//bf_size
                if fileSize%bf_size!=0:
                    count+=1

                for i in range(count):
                    data = conn.recv(bf_size)
                    user.sendFileToAll(username,data)

            #메세지라면 성공
            if msg == MESSAGE_HEADER:
                msg = conn.recv(1024).decode(FORMAT)
                user.messageHandler(username,msg)
        except Exception as e:
            connected=False
            print(e)
    print('[%s] 접속종료중' %username)
    user.removeUser(username)

if __name__ == '__main__':
    runServer()
    
