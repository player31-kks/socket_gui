from tkinter import *
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
from tkinter import filedialog
import threading
import os
import time

FILE_HEADER="[FILE]"
MESSAGE_HEADER="[MESG]"
DISCONNECT_MSG ="[!EXIT]"


bf_size = 65536

class Chating_gui(Frame):
    def __init__(self,master,sock,ID,Password):
        Frame.__init__(self, master)
        self.master = master
        self.sock = sock
        self.id = ID
        self.password = Password
        self.master.title(f"{self.id}의 GUI")
        self.master.geometry("370x600+300+100")
        self.master.resizable(False,False)
        #=================================================================================
        self.frame1 = Frame(self.master)
        self.frame1.pack()
        scrollbar=Scrollbar(self.frame1)
        scrollbar.pack(side="right",fill="y")

        self.Text_chating = Text(self.frame1,width=60,height=35,yscrollcommand=scrollbar.set,state='disable')
        self.Text_chating.pack()
        scrollbar.config(command=self.Text_chating.yview)
        #=================================================================================
        self.frame2 = Frame(self.master)
        self.frame2.pack(fill='x')
        self.txt = Text(self.frame2,width=40,height=5.5)
        self.txt.grid(row=0,column=0,rowspan=2)
        self.sendBtn = Button(self.frame2,text="send",width=10,height=2,command=self.sendMessage).grid(row=0,column=1,padx=2,pady=2)
        self.fileSendBtn = Button(self.frame2,text="file",width=10,height=2,command=self.sendFile).grid(row=1,column=1,padx=2,pady=2)
        #=================================================================================
        self.frame3 = Frame(self.master)
        self.frame3.pack(fill='x')
        self.p_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(self.frame3,maximum=100,length=300,variable=self.p_var)
        self.progress_bar.pack(pady=15)
        #========================================================================================
        if not(os.path.isdir(self.id)):
            os.makedirs(os.path.join(self.id))
        self.download_filepath =os.path.join(os.getcwd(),self.id)

    def test(self):
        pass
    def textUpdate(self,message):
        self.Text_chating.config(state="normal")
        self.Text_chating.insert(END,"\n"+message)
        self.Text_chating.config(state="disable")

    def sendMessage(self):
        message = self.txt.get("1.0",END) #1 : 첫번째 라인, 0번째 컬럼 위치
        try:
            self.sock.send(MESSAGE_HEADER.encode())
            self.sock.send(message.encode())
        except:
            #msgbox.showwarning("경고","오류입니다.")
            print("오류")
        else:
            self.txt.delete("1.0",END)

    def sendFile(self):
        files = filedialog.askopenfilenames(title="파일을 선택하세요",\
            filetypes=(('모든파일',"*.*"),("PNG파일","*.png"),('JPEG파일',"*.jpg")),\
            initialdir="C:/")
        if files:
            #===================파일 사이즈와 파일 이름 ===================
            file_size = os.path.getsize(files[0]) 
            filename=files[0].split('/')[-1]
            #===================파일보내기 위한 헤더 (클라 -> 서버) ===================
            self.sock.send(FILE_HEADER.encode())
            self.sock.send(f"{file_size},{filename}".encode())
            time.sleep(0.5)

            count = file_size//bf_size
            if file_size%bf_size!=0:
                count+=1
            #===================파일보내기 (클라 -> 서버) ===================
            with open(files[0],'rb') as f:
                try:
                    for i in range(count):
                        data=f.read(bf_size)
                        self.sock.sendall(data)
                except Exception as e:
                    print(e)
        
    def recvFile(self):
        print("recvFile start")
        file_info=self.sock.recv(bf_size).decode()
        print(file_info)
        self.textUpdate(file_info)

        filename = file_info.split(',')[1]
        filesize = int(file_info.split(',')[0])

        count = filesize//bf_size
        if filesize%bf_size!=0:
            count+=1

        path = os.path.join(self.download_filepath,filename)
        with open(path,'wb') as f:
            try:
                for _ in range(count):
                    data = self.sock.recv(bf_size)
                    f.write(data)
            except Exception as e:
                print(e)
        print("파일 전송이 완료되었습니다.")

    #thread 처리하기 
    def recvMessage(self):
        while True:
            try:
                data = self.sock.recv(10).decode()
                print(data)
                if not data:
                    break
                if data==FILE_HEADER:
                    self.recvFile()
                if data==MESSAGE_HEADER:
                    data = self.sock.recv(1024).decode()
                    self.textUpdate(data)
                if data==DISCONNECT_MSG:
                    break
            except Exception as e:
                print(e)
                break
                
    #thread 처리하기
    def chatting(self):
        self.master.mainloop()


if __name__ == '__main__':
    root = Tk()
    a = 1
    app=Chating_gui(root,a,'kks')
    root.mainloop()
    
