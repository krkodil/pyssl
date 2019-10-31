from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

HOST = 'localhost'
PORT = 443


class Cert:
    def __init__(self, crt):
        self.subject = dict([x[0] for x in crt.get('subject')])
        self.issuer = dict([x[0] for x in crt.get('issuer')])
        self.version = crt.get('version')
        self.serialNumber = crt.get('serialNumber')
        self.notBefore = crt.get('notBefore')
        self.notAfter = crt.get('notAfter')


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def get_client_cert(self):
        crt = self.connection.getpeercert()
        if not crt:
            raise ValueError("Empty or invalid certificate")
        return Cert(crt)

    def do_GET(self):
        cert = self.get_client_cert()
        cipher = self.connection.cipher()
        self.connection
        self.send_response(200)
        self.end_headers()
        response = 'GET {} {}, server: {}, system: {}, cipher: {}, cert: {}'.format(
            self.path, self.protocol_version, self.server_version, self.sys_version, cipher, cert.serialNumber)

        self.wfile.write(bytearray(response, 'utf-8'))


httpd = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket(httpd.socket,
                               server_side=True,
                               ca_certs="keys/ca.crt",
                               certfile="keys/server.crt",
                               keyfile="keys/server.key",
                               cert_reqs=ssl.CERT_REQUIRED,
                               ssl_version=ssl.PROTOCOL_TLSv1_2)

httpd.serve_forever()
