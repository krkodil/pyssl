@ echo off

rem ---- Initial clean up
del *.key
del *.crt

set openssl=C:\OpenSSL\bin\openssl.exe

rem ---- Self signed root CA cert
%openssl% req -nodes -x509 -newkey rsa:2048 -keyout ca.key -out ca.crt -subj "/C=US/ST=NY/L=Boston/O=Python/OU=root/CN=localhost" -days 365

rem ----  Server cert
%openssl% req -nodes -newkey rsa:2048 -keyout server.key -out server.csr -subj "/C=US/ST=NY/L=Boston/O=Python/OU=server/CN=localhost"
rem ----  Signed server cert
%openssl% x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365

rem ---- Clients cert
%openssl% req -nodes -newkey rsa:2048 -keyout client.key -out client.csr -subj "/C=US/ST=NY/L=Boston/O=Python/OU=client/CN=localhost"

rem ---- Sign the clients
%openssl% x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAserial ca.srl -out client.crt -days 365

rem ---- Post clean up
del *.csr
del *.srl
del ca.key
