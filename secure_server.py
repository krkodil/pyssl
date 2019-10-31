import socket
import ssl
from _thread import *

HOST = 'localhost'
PORT = 10443


class Cert:
    def __init__(self, crt):
        self.subject = dict([x[0] for x in crt.get('subject')])
        self.issuer = dict([x[0] for x in crt.get('issuer')])
        self.version = crt.get('version')
        self.serialNumber = crt.get('serialNumber')
        self.notBefore = crt.get('notBefore')
        self.notAfter = crt.get('notAfter')


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


def server_thread(server):
    while True:
        client, address = server.accept()
        cipher = client.cipher()
        cert = Cert(client.getpeercert())
        print("Accepted connection from {}:{}, Peer: {}, Cipher: {}, {} {}bit".format(
            address[0], address[1],
            cert.subject.get("organizationalUnitName"),
            cipher[0],
            cipher[1],
            cipher[2])
        )
        start_new_thread(client_thread, (client, address[0]))


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_server = ssl.wrap_socket(server_socket,
                                 server_side=True,
                                 ca_certs="keys/ca.crt",
                                 certfile="keys/server.crt",
                                 keyfile="keys/server.key",
                                 cert_reqs=ssl.CERT_REQUIRED,
                                 ssl_version=ssl.PROTOCOL_TLSv1_2)

    ssl_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssl_server.bind((HOST, PORT))
    ssl_server.listen(10)

    start_new_thread(server_thread, (ssl_server,))

    input("Server running on port {}\nPress Enter to terminate ...\n".format(PORT))
