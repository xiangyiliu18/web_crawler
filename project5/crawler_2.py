import socket
import sys
import argparse
from urllib.parse import urlparse
from bs4.element import Comment
from urllib.parse import urljoin
import base64
import re


# ###################### Personal Socket ###################
class OneSocket:
    global user_agent
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, url):
        global user_agent
        url = urlparse(url)
        host = url.hostname
        path = url.path
        addr = socket.getaddrinfo(host, 80)[0][-1]
        self.sock.connect(addr)
        return (host, path, url.port)

    ## 'POST' request
    def post_response(self, url,filename, userName, password):
        global user_agent
        tmp=self.connect(url)
        data = "log=user&pwd=EN9fQcC3jnsS"
        msg=('POST /%s HTTP/1.1\r\nHost: %s\r\nUser-Agent: %s\r\nConent-Type: %s\r\n\r\n' % (tmp[1], tmp[0],"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36","application/x-www-form-urlencoded"))
        request = msg+data
        sent = self.sock.sendall(bytes(request, 'utf8'))
        print(self.sock.recv(4096))
        
        if sent == 0:
        	raise RuntimeError("socket connection broken")
        ############################## Get Response  ####################################
        response=[]
        while True:
            data = self.sock.recv(4096)
            if data:
                response.append(data)
            else:
                break
        self.sock.close()

        response = b''.join(response)
        all_content = response.decode("utf8", "ignore")

        header = all_content.split('\r\n\r\n')[0]
        with open("header.txt", "w") as f:
            f.write(header)
            f.close()

        content = all_content.split('\r\n\r\n')[1]
        content = content.encode()
        with open(filename, 'wb') as f:
            f.write(content)
            f.close()

crawler = OneSocket()
crawler.post_response("http://3.16.240.57/wp-login.php","result.html","users","EN9fQcC3jnsS")

