import threading


HEADER =64
FORMAT ="utf-8"
DISCONNECT_MSG ="[!EXIT]"
HOST ='localhost'
PORT = 9000
lock = threading.Lock()
FILE_HEADER="[FILE]"
MESSAGE_HEADER="[MESG]"

class UserManager:
    count = 0
    def __init__(self):
        self.users ={}
        self.disusers={}

    def addUser(self,username,new_password,conn,addr):
        print(username)
        if username in self.users or username in self.disusers:
            ####disusers
            if username in self.disusers:
                if self.disusers[username]!=new_password:
                    return 2
                else:
                    ###정상
                    lock.acquire()
                    self.users[username]=(conn,addr,new_password)
                    lock.release()
                    del self.disusers[username]
                    print(f'{username}님이 재입장하셨습니다.')
                    return 4
                    lock.release()
                    
            ####users
            elif username in self.users:    
                conn,add,old_password=self.users[username]
                print(username,old_password)
                if old_password!=new_password:
                    return 2
                return 3

        lock.acquire()
        self.users[username]=(conn,addr,new_password)
        lock.release()
        
        print(f'{username}님이 입장하셨습니다.')
        UserManager.count+=1
        print(f"============대화 참여자 수  {len(self.users)+len(self.disusers)}============")
        return 1
    
    def removeUser(self,username):
        if username not in self.users:
            return
        conn,addr,password=self.users[username]
        try:
            conn.sendall(DISCONNECT_MSG.encode())
        except Exception as e:
            lock.acquire()
            del self.users[username]
            lock.release()
            self.disusers[username] = password
            print(f"{username}님이 비활성되었습니다.")
            self.sendMessageToAll(f"{username}님이 비활성되었습니다.")
        else:
            lock.acquire()
            del self.users[username]
            lock.release()
            self.sendMessageToAll(f"{username}님이 퇴장하셨습니다.")
            print('--- 대화 참여자 수 [%d]' %len(self.users))

    def messageHandler(self,username,msg):
        if msg[0] !="!":
            self.sendMessageToAll(f'[{username}] : {msg}')
            return
        if msg.strip()==DISCONNECT_MSG:
            self.removeUser(username)
            return -1

    def sendMessageToAll(self,msg,option=1):
        if option==1:
            for conn,addr,_ in self.users.values():
                conn.send(MESSAGE_HEADER.encode())
                conn.send(msg.encode())
        else:
            for conn,addr,_ in self.users.values():
                conn.send(FILE_HEADER.encode())
                conn.send(msg.encode())


    def sendFileToAll(self,username,data):
        for conn,addr,_ in self.users.values():
            conn.send(data)
