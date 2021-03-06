import os
import socket
import select
import sys
import threading
from os import path
import configparser
from bs4 import BeautifulSoup

class Client(threading.Thread):
    def __init__(self):
        # threading.Thread.__init__(self)
        self.host = '127.0.0.1'
        self.port = 80
        self.client = None
        self.size = 1024

    def init_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host,self.port))

    def get_response(self,response):  
        while True:
            received = self.client.recv(1024)
            response += received         
            if len(received) < 1024:
                break
        return response

    def get_index(self):
        request_header = b'GET / HTTP/1.0\r\n\r\n'
        self.client.send(request_header)
        response = self.get_response(b'')
        
        responses = response.rsplit(b'\r\n',1)
        content = responses[1].decode('utf-8')
        print(responses[0])

        soup = BeautifulSoup(content, 'html.parser')
        print(soup.get_text())

    def get_listdir(self, request_dirname):
        request_header = f'GET /{request_dirname} HTTP/1.0\r\n\r\n'.encode('utf-8')
        self.client.send(request_header)
        response = self.get_response(b'')
        responses = response.split(b'\r\n', 3)
        http_status = responses[0].split(b' ',1)
        print(responses[0])

        content = responses[3].decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        print(soup.get_text())

    def get_file(self, file_request):
        request_header = f'GET /{file_request} HTTP/1.0\r\n\r\n'.encode('utf-8')
        self.client.send(request_header)
        response = self.get_response(b'')

        content = response
        soup = BeautifulSoup(content, 'html.parser')
        print(soup.get_text())
        
        # responses = response.split(b'\r\n', 3)
        # http_status = responses[0].split(b' ',1)
        # print(responses[0])
        # print(response)

        # if http_status[1] == b'200 OK':
        #     with open(file_request,'wb') as file:
        #         content = responses[3]
        #         file.write(content)

        # elif http_status[1] == b'404 Not found':
        #     content = responses[3].decode('utf-8')
        #     soup = BeautifulSoup(content, 'html.parser')
        #     print(soup.get_text())

    def run(self, file_request = '/'):
        self.init_socket()
        try:
            while True:
                if file_request == '/' or file_request == 'index.html':
                    self.get_index()
                elif file_request[-1] == '/':
                    self.get_listdir(file_request)
                else:
                    self.get_file(file_request)
                
                file_request = input()
                
       
        except KeyboardInterrupt:
            self.client.close()
            sys.exit(0)

if __name__ == "__main__" :
    client = Client()
    client.run()