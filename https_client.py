import http.client
import ssl

HOST = 'localhost'
PORT = 443

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='keys/server.pem')
context.load_cert_chain(certfile='keys/client1.crt', keyfile='keys/client1.key')

connection = http.client.HTTPSConnection(HOST, PORT, context=context)

connection.request(method="GET", url='/api/list/all')

response = connection.getresponse()
print(response.status, response.reason)

data = response.read()
print(data)
