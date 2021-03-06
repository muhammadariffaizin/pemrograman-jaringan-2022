import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url = 'www.its.ac.id'
# url = 'www.python.org'

server_address = (url, 80)
client_socket.connect(server_address)

request_header = 'GET / HTTP/1.0\r\nHost: ' + url + '\r\n\r\n'
client_socket.send(request_header.encode())

response = ''

while True:
    received = client_socket.recv(1024)
    if not received:
        break
    response += received.decode('utf-8')
    break;
    
print('HTTP version of', url, ':', response.split('\n')[0].split()[0])
client_socket.close()