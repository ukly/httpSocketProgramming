from socket import *

serverName = '127.0.0.1'                        #local 호스트에 연결
serverPort = 8080                               #8080 포트 사용

clientSocket = socket(AF_INET, SOCK_STREAM)     #client socket 생성
clientSocket.connect((serverName, serverPort))  #localhost에 8080포트로 연결

method = input('Enter request method:')         #요청할 method 입력
requestFile = input('Enter request file:')      #요청할 file명 입력
version = input('Enter HTTP Version:')          #요청할 HTTP version 입력

if method == 'POST':                            #POST 요청시 작성한 data와 method, requestFile, version을 request에 저장
    data = input('Enter POST data:')
    request = '%s %s %s %s' %(method, requestFile, version, data)
elif method == 'PUT':                           #PUT 요청시 작성한 data 입력 후 data와 method, requestFile, version을 request에 저장
    data = input('Enter PUT data:')
    request = '%s %s %s %s' %(method, requestFile, version, data)
elif method == 'GET':                           #GET 요청시 method와 requestFile, version을 request에 저장
    request = '%s %s %s' %(method, requestFile, version)
else:                                           #HEAD 요청시 method와 requestFile, version을 request에 저장
    request = '%s %s %s' %(method, requestFile, version)

clientSocket.send(request.encode())             #request를 연결된 socket을 통해 encoding 한 후 전달

response = clientSocket.recv(1024)              #연결된 socket을 통해 response를 받음
print('From server:', response.decode())        #reponse받은 내용을 decode한 후 출력
clientSocket.close()                            #연결 종료