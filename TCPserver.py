from socket import *
import sys
import os

#Membuat TCP Socket dan bind (IP address, port)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('192.168.10.4', 1234))
serverSocket.listen(1)

while True:
    #Menunggu koneksi dari client
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print('Connected from', addr)

    try:
        #Menerima HTTP request dari client
        message = connectionSocket.recv(1024).decode()
        
        #Mengesktrak filename yang diminta
        filename = message.split()[1]
        
        #Mengecek file yang diminta client
        if os.path.isfile(filename[1:]):
            #Membuka file yang diminta oleh client
            with open(filename[1:], 'rb') as file:
                outputdata = file.read()
            
            #Mengirim HTTP response header
            response_header = 'HTTP/1.1 200 OK\r\n\r\n'
            connectionSocket.send(response_header.encode())
            
            #Mengirim content file yang diminta oleh client
            connectionSocket.sendall(outputdata)
        else:
            response_headers = "HTTP/1.1 {}\r\n".format("404 Not Found")
            response_headers += "Content-Type: text/html\r\n"
            response_headers += "\r\n"
            response_body = "<html><body><h1>{}</h1></body></html>".format("File Not Found")
            response = response_headers.encode() + response_body.encode()
            connectionSocket.send(response)
        
        #Menutup koneksi soket
        connectionSocket.close()
        
    except Exception as e:
        print('Error:', str(e))
        #Menutup koneksi socket jika terdapat masalah
        connectionSocket.close()

#Menutup koneksi socket
serverSocket.close()
sys.exit()