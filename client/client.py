from tkinter import *
import tkinter.messagebox as msgbox
import socket
from chating_gui import Chating_gui
import threading
import sys

root = Tk()
root.title("GUI")
root.geometry("620x150+300+100")
#root.resizable(False,False)

#첫번째 줄
server_label = Label(root,text="Server IP",width=10)
server_label.grid(row=0,column=0,sticky=N+E+W+S,padx=3,pady=3)
server_entry =Entry(root,width=30)
server_entry.insert(END,"localhost")
server_entry.grid(row=0,column=1,sticky=N+E+W+S,padx=3,pady=3)

port_label = Label(root,text="port",width=10)
port_label.grid(row=0,column=2,sticky=N+E+W+S,padx=3,pady=3)
port_entry =Entry(root,width=30)
port_entry.grid(row=0,column=3,sticky=N+E+W+S,padx=3,pady=3)
port_entry.insert(END,"9000")

#두번째 줄
ID_label = Label(root,text="ID",width=10)
ID_label.grid(row=1,column=0,sticky=N+E+W+S,padx=3,pady=3)
ID_entry = Entry(root,width=30)
ID_entry.grid(row=1,column=1,sticky=N+E+W+S,padx=3,pady=3)

password_label = Label(root,text="password",width=10)
password_label.grid(row=1,column=2,sticky=N+E+W+S,padx=3,pady=3)
password_entry = Entry(root,width=30)
password_entry.grid(row=1,column=3,sticky=N+E+W+S,padx=3,pady=3)

def login():
    global clientsock
    clientsock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    try:
        clientsock.connect((server_entry.get(),int(port_entry.get())))
    except:
        msgbox.showwarning("경고","서버가 연결을 거부하였습니다.")
    else:
        client_info = f"{ID_entry.get()}/{password_entry.get()}"
        clientsock.send(client_info.encode())
        data=clientsock.recv(1024).decode()
        if data=="환영":                
        #새로운창 만들기
            global chatingWindow,app,recvThread,appThread
            
            chatingWindow=Tk()
            app=Chating_gui(chatingWindow,clientsock,ID_entry.get(),password_entry.get())
            root.destroy()
            
            recvThread = threading.Thread(target = app.recvMessage)
            recvThread.start()
            chatingWindow.mainloop()
            clientsock.sendall('[!EXIT]'.encode())
        elif data == "비틀림": # 비밀번호 틀림
            msgbox.showwarning("경고","알맞은 비밀번호를 입력하시오")
            clientsock.close()
            del clientsock
        elif data == "아중복": #아이디 중복
            msgbox.showwarning("경고","이미 존재하는 아이디입니다")
            clientsock.close()
            del clientsock
        #clientsock.close()




LoginBtn = Button(root,text="Login",bg="green",width=15,height=3,command=login)
LoginBtn.grid(row=2,column=1,padx=3,pady=3)


CancleBtn = Button(root,text="Cancle",bg="Yellow",width=15,height=3,command=root.destroy)
CancleBtn.grid(row=2,column=3,padx=3,pady=3)

root.mainloop()
#채팅창 꾸미기 



