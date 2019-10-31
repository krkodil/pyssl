import socket
import ssl

HOST = 'localhost'
PORT = 10443

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setblocking(True)
sock.connect((HOST, PORT))

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations('keys/server.pem')
context.load_cert_chain(certfile="keys/client1.crt", keyfile="keys/client1.key")

secure_sock = context.wrap_socket(sock, server_hostname=HOST)   # Set HOST for SNI verification

cert = secure_sock.getpeercert()
print(cert)

secure_sock.write(b'Hello!')

print('\nServer response:', secure_sock.read(1024))

secure_sock.close()
sock.close()
