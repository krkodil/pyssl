import socket
import ssl

HOST = 'localhost'
PORT = 10443

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

client, address = server_socket.accept()
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


# verify client
if not cert or ('organizationName', 'Test') not in cert['subject'][3]:
    raise Exception("Client cert not match!")

try:
    data = secure_sock.read(1024)
    secure_sock.write(data)
finally:
    secure_sock.close()
    server_socket.close()
