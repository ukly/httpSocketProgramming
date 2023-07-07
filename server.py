from socket import *
import os
from datetime import datetime

serverPort = 8080                                #8080포트를 이용하여 통신 구현
serverSocket = socket(AF_INET, SOCK_STREAM)      #server socket 생성
serverSocket.bind(('', serverPort))              #8080포트를 통해 오든 모든 IP의 연결을 수신
serverSocket.listen(1)                           #한 번에 하나의 연결을 수신함
methods = ['GET', 'POST', 'PUT', 'HEAD']         #요청 가능한 request method들
SupportedHTTPVersions = ['HTTP/1.1', 'HTTP/2']   #HTTP/1.1과 HTTP/2만 지원한다고 가정
print('The server is ready to receive')

class BadRequest(Exception):                     # 400 에러 발생을 위한 오류
    pass
class NotSupportedVersion(Exception):            # 505 에러 발생을 위한 오류
    pass

while True:
    connectionSocket, address = serverSocket.accept()      #serverSocket을 통해 연결된 socket을 생성
    requestMessage = connectionSocket.recv(1024).decode()  #연결된 socket을 통해 받아온 내용을 decode
    requestFile = requestMessage.split()[1]                #요청 받은 파일 명
    requestMethod = requestMessage.split()[0]              #요청 받은 method
    requestVersion = requestMessage.split()[2]             #요청 받은 HTTP 버전
    try:
        if requestMethod not in methods:                   #지원하지 않는 method일 경우 오류 발생
            raise BadRequest
        if requestVersion not in SupportedHTTPVersions:    #지원하지 않는 HTTP 버전일 경우 오류 발생
            raise NotSupportedVersion
        if requestMethod == 'GET':                         #GET 요청 시
            f = open(requestFile, 'rt', encoding='utf-8')  #f = open()에 rt 옵션을 통해 읽어옴
            outputData = f.read()                          #outputData에 data body 내용 저장
            f.close()
        elif requestMethod == 'POST':                      #POST 요청 시
            f = open(requestFile, 'w')                     #f = open()에 w 옵션을 통해 파일 생성
            inputData = requestMessage.split()[3]          #요청 받은 내용을 토대로 파일 작성
            f.write(inputData)
            f.close()
            f = open(requestFile, 'rt', encoding='utf-8')
            f.close()
        elif requestMethod == 'PUT':                       #PUT 요청 시
            f = open(requestFile, 'a')                     #기존의 내용에 수정 또는 새롭게 생성
            inputData = requestMessage.split()[3]
            f.write(inputData)
            f.close()
            f = open(requestFile, 'rt', encoding='utf-8')
            f.close()
        elif requestMethod == 'HEAD':                      #HEAD 요청 시
            f = open(requestFile, 'rt', encoding='utf-8')  #기존에 존재하는 파일을 읽어옴
            f.close()

        responseMessage = '%s 200 OK\r\n' %(requestMessage.split()[2])  # responseMessage의 status line 작성

        filePath = requestMessage.split()[1]                            # 요청받은 파일 경로를 반환
        fileSize = os.path.getsize(filePath)                            # os.path를 이용하여 파일의 크기 저장
        fileLastModified = os.path.getmtime(filePath)                   # os.path를 이용하여 수정 시간 저장 및 datetime 형태로 변환
        LastModified = datetime.fromtimestamp(fileLastModified).strftime("%a, %d %b %Y %H:%M:%S GMT")

        responseMessage += "Content-Type: %s\r\n" %(filePath)           # responseMessage에 추가
        responseMessage += "Content-Length: %s\r\n" %(fileSize)
        responseMessage += "Last-Modified: %s\r\n" %(LastModified)
        responseMessage += "\r\n"


        if requestMethod == 'GET':                                      # method가 GET 일때만 data body를 responseMessage에 추가
            responseMessage += outputData

        connectionSocket.send(responseMessage.encode('utf-8'))          # 작성된 responseMessage를 연결된 socket을 통해 전송
        print('OK')                                                     # 정상 전송 시 OK 출력
        connectionSocket.close()
    except IOError:                                                     # GET 또는 HEAD로 f=open()을 통해 읽어올 때 존재하지 않는 파일일 경우 404 오류
        connectionSocket.send(('%s 404 Not Found' %(requestMessage.split()[2])).encode('utf-8'))
        connectionSocket.close()
    except BadRequest:                                                  # 존재하지 않는 method로 요청 시 400 오류
        connectionSocket.send(('400 Bad Request').encode('utf-8'))
        connectionSocket.close()
    except NotSupportedVersion:                                         # 지원하지 않는 HTTP version으로 요청 시 505 오류
        connectionSocket.send(('505 HTTP Version Not Supported').encode('utf-8'))
        connectionSocket.close()

severSocket.close()                                                     # 연결 종료