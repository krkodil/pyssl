import socket
import ssl
from _thread import *

HOST = 'localhost'
PORT = 10443


def server_thread(server):
    while True:
        client, address = server.accept()
        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        secure_sock = ssl.wrap_socket(client,
                                      server_side=True,
                                      ca_certs="keys/clients.pem",
                                      certfile="keys/server.crt",
                                      keyfile="keys/server.key",
                                      cert_reqs=ssl.CERT_REQUIRED,
                                      ssl_version=ssl.PROTOCOL_TLSv1_2)

        print(secure_sock.cipher())

        cert = secure_sock.getpeercert()
        print(cert)
        start_new_thread(client_thread, (secure_sock, address[0]))


def client_thread(client, client_ip):
    while True:
        try:
            request = client.recv(255)
        except ConnectionResetError:
            break
        if request:
            client.send(request)
        break
    print('Client {} disconnected.'.format(client_ip))
    client.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

start_new_thread(server_thread, (server_socket, ))

input('Press \'Enter\' to stop the server ...\n\n')
server_socket.close()
