<center><h1> A simple Python Chat Application with GUI
👋</h1></center>

using library
```python
import socket
import threading
from tkinter import *
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
from tkinter import filedialog
import os
import time
```

```
/socket_gui
|-- client
|    |--chating_gui.py : 로그인 및 채팅창 gui 에서 동작하는 기능을 수행하기 위한 코드
|    |--client.py      : 각 클라이언트들이 채팅 프로그램을 실행하기 위한 코드
|    
|-- server
    |--server.py       : 서버 측 구현을 위한 코드
    |--UserManager.py  : 각 클라이언트이 접속 및 연결 정보를 관리하기 위한 코드
```

## About the Project
## 1. 기본 로그인 기능

우선, 채팅 프로그램이 동작하기 위해서는 서버가 실행되어야 합니다. server.py 파일을
클릭해서 서버를 열게되면 다음과 같이 서버가 실행됩니다.
![네트워크 학기말 과제 보고서](https://user-images.githubusercontent.com/57718605/103261062-5bb62680-49e3-11eb-8b52-da6c620ef8c6.png)
위와 같이 서버가 열린 후, 클라이언트는 client.py 파일을 더블클릭 후 실행하게 되고,
다음과 같은 로그인 GUI 화면을 볼 수 있습니다.
<br><br>

![네트워크 학기말 과제 보고서](https://user-images.githubusercontent.com/57718605/103261099-8902d480-49e3-11eb-8b26-e850b368ad5f.png)
같은 호스트내에서 접근할 경우에는 server IP 란에 ‘localhost’를 입력하면 되고, 같은
네트워크 상의 다른 호스트에서 접근하기 위해서는 서버 호스트의 ip 정보를 해당 란에
입력하여야 합니다. 서버의 포트 넘버는 9000 번으로 설정되어 있습니다. 최초 로그인
하는 경우 ID 와 password 란에 각각 원하는 값을 입력해서 로그인 할 수 있습니다.
로그인에 성공할 경우, 메시지와 파일을 주고받을 수 있는 채팅창이 다음과 같이
열립니다. (아이디가 ‘개구리’인 경우)
<br><br>

<center><img src="https://user-images.githubusercontent.com/57718605/103261146-b8b1dc80-49e3-11eb-99e7-51dc18fba6ac.png" width=200 height=></img>
</center>

유저를 추가적으로 생성하고 싶으면 client.py 를 새롭게 열고 다른 아이디와 비밀번호를
입력해주시면 됩니다. 이때 이미 접속중인(ex 개구리) 아이디와 비밀번호를 입력하면
“이미 존재하는 아이디입니다” 라는 경고창이 뜨고 아이디 생성이 되지 않습니다.
<center><img src="https://user-images.githubusercontent.com/57718605/103261337-894f9f80-49e4-11eb-9b8c-d19667796ab8.png" width=600 height=200></img>
</center>
<br><br>

서버는 유저가 새로 생성될 때마다 “ㅇㅇ님이 입장하셨습니다” 라는 문구와 함께 전체
대화 참여자 수를 표시합니다.
![네트워크 학기말 과제 보고서](https://user-images.githubusercontent.com/57718605/103261409-d2075880-49e4-11eb-8747-22a9ea1cc0b0.png)

## 2. 채팅 및 파일 전송 기능
채팅을 하기 위해 채팅 GUI 화면에서 원하는 텍스트를 입력한 후, send 버튼를 누르게
되면 본인을 포함한 모든 채팅창에서 해당 내용의 채팅이 전송됩니다.
![네트워크 학기말 과제 보고서](https://user-images.githubusercontent.com/57718605/103261572-59ed6280-49e5-11eb-86bc-00137864a5cd.png)
파일 전송기능을 위해서는 file 버튼을 클릭하면 파일 첨부창이 뜨게 되는데, 첨부하고
싶은 파일을 찾아서 모든 유저에게 전송할 수 있습니다. 해당 클라이언트가 서버에 파일을
전송하고 서버가 모든 클라이언트에게 broadcast 해 주는 방식으로 구현했기 때문 특정
유저에게 파일을 전송하는 것은 불가능합니다. 파일을 전송하게 되면 본인을 포함한 모든
클라이언트 창에 전송된 파일 명이 나오고, 각각 client.py 을실행된 동일한 디렉토리
내에서 파일이 다운로드가 됩니다.

<img src="https://user-images.githubusercontent.com/57718605/103261634-82755c80-49e5-11eb-9ec0-2cdba7440662.png" width=350 height=400></img>
<img src="https://user-images.githubusercontent.com/57718605/103261703-ca947f00-49e5-11eb-94d4-8be33af3cb8a.png" width=350 height=400></img>

※ File 버튼을 클릭할 경우 ‘tk’라는 타이틀을 가진 공란의 GUI 창이 생성되는데, 이는
TKinter 상에서 발생하는 오류로 보이며, 단순히 창을 꺼서 종료가 가능합니다.

## 3.사용 종료 및 비활성화 기능
만약 정상적으로 종료를 하고 싶으시면 채팅 GUI 에서 오른쪽 상단에 있는 X 를 누르면
됩니다. 서버는 이를 정상 종료로 인식하고 [유저명] 접속종료중이라는 메시지와 함께
바뀐 대화 참여자수를 표시합니다.

![네트워크 학기말 과제 보고서](https://user-images.githubusercontent.com/57718605/103261902-89509f00-49e6-11eb-9ba6-2c9a98d1f900.png)

만약 그 외의 방법(네트워크 오류 등)으로 유저가 종료를 하면 서버는 에러메시지와 함께
[유저명] 이 비활성되었습니다 라는 창을 띄우고 대화 참여자수는 바뀌지 않습니다. 해당
비활성 메시지는 클라이언트 GUI 에도 표시가 됩니다
![네트워크 학기말 과제 보고서](https://user-images.githubusercontent.com/57718605/103261924-9d949c00-49e6-11eb-89ed-94622ee6d674.png)

<center><img src="https://user-images.githubusercontent.com/57718605/103261957-bf8e1e80-49e6-11eb-8e98-72b50ba3a63b.png" width=250 height=350></img></center>
비활성된 유저가 다시 접속하기 위해서는, main.py 를 열어서 비활성화된 ID 명과 알맞은
password 를 입력하면 서버에서 “00 님이 재입장하셨습니다”라는 문구가 뜨고 유저는
다시 채팅을 할 수 있습니다.

![네트워크 학기말 과제 보고서](https://user-images.githubusercontent.com/57718605/103262053-1b58a780-49e7-11eb-8470-6b53dc4df4aa.png)
이 때, 알맞지 않은 비밀번호를 입력한다면 다음과 같은 경고창이 생성됩니다.

<center><img src="https://user-images.githubusercontent.com/57718605/103262136-58249e80-49e7-11eb-9504-8f970ed27c33.png" width=600 height=200></img></center>

모든 유저들이 접속을 다 종료해도 server.py 는 종료되지 않고 계속 새로운 유저가
들어올 때까지 대기합니다.
