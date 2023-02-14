import socket
import json
from datetime import datetime

def log_request(request, client_address):
    lines = request.split('\r\n')
    request_line = lines[0].split()
    method, url, _ = request_line
    subdomain, _, path = url.partition('/')
    data = {
        'time': str(datetime.now()),
        'attacker_ip': client_address[0],
        'attacker_port': client_address[1],
        'method': method,
        'subdomain': subdomain,
        'url': path,
        'headers': {},
        'body': ''
    }
    for i, line in enumerate(lines[1:]):
        if not line:
            data['body'] = '\r\n'.join(lines[i+2:])
            break
        key, value = line.split(': ')
        data['headers'][key] = value
    with open('log.json', 'a') as f:
        f.write(json.dumps(data) + '\n')

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(1)
    print('Listening on 0.0.0.0:80...')
    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(4096).decode('utf-8')
        log_request(request, client_address)
        response = 'HTTP/1.1 200 OK\r\n\r\nThis is a honeypot. The request has been logged.'
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

if __name__ == '__main__':
    start_server()
