import http.client
import ssl

HOST = 'localhost'
PORT = 443

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations('keys/ca.crt')
context.load_cert_chain(certfile='keys/client.crt', keyfile='keys/client.key')

connection = http.client.HTTPSConnection(HOST, PORT, context=context)

connection.request(method="GET", url='/api/list/all')

response = connection.getresponse()
print(response.status, response.reason)

data = response.read()
print(data)
