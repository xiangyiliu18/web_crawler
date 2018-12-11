from urllib.parse import urlparse, urljoin, urlsplit, urlunsplit
import socket
import sys
import argparse
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urljoin
import base64
import re
import os
import validators
import requests
import webbrowser
import random
import math

user_agent = 'Mozilla/5.0'
###################### Personal Socket ###################
class MySocket:
    global user_agent
    def __init__(self):
    	''' Crete one socket instance
    	#### AF_INET refers to the address family ipv4
    	#### the SOCK_STREAM means connection oriented TCP protocol--> which is used to connect to a server
    	'''
    	self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, url):
        url = urlparse(url)
        host = url.hostname
        path = url.path
        addr = socket.getaddrinfo(host, 80)[0][-1]
        self.sock.connect(addr)
        return (host, path)


    def split_response(self, response, filename):
    	if len(response) > 0:
    		response= b''.join(response)
    		response = response.decode("utf-8", "ignore")
    		response = response.split('\r\n\r\n')
    		header = response[0]
    		with open('header_test.txt', 'w') as f:
    			f.write(header)
    			f.close()
    		content = (response[1]).encode("utf-8", "ignore")
    		with open(filename, "wb") as f:
    			f.write(content)
    			f.close()
    	else:
    		print("No available response")


    ## 'Get' request && its reposne
    def get_response(self, url, filename):  ## Send 'Get' Request
    	tmp = self.connect(url)
    	request = ('GET /%s HTTP/1.0\r\nHost: %s\r\nUser-Agent: %s\r\n\r\n' % (tmp[1], tmp[0], user_agent))
    	sent = self.sock.sendall(bytes(request, "utf-8"))
    	if sent == 0:
    		print("socket connection broken\n")
    	else:
    		response = []
    		while(1):
    			data = self.sock.recv(4096)
    			if data:
    				response.append(data)
    			else:
    				self.sock.close()
    				break
    	self.split_response(response,filename)

website='https://scrapinghub.com'
# # website ='http://3.16.240.57'

def replace_subdomain(subdomain):
	global website
	old_host = list(urlsplit(website))
	old_host[1] = subdomain+'.'+old_host[1]
	new_host = urlunsplit(old_host)
	return new_host


def more_links():
	global website
	temp_links =[]
	robot_website = website + '/robots.txt'
	s = MySocket()
	s.get_response(robot_website,'robots_test.txt')
	with open('robots.txt', 'r') as f:
		for line in f:
			if "Disallow" in line or "Allow" in line:
				line = line.rstrip().split(' ')
				if len(line) > 1:
					line_link = website + line[1]
					if line_link not in temp_links:
						if validators.url(line_link):
							temp_links.append(line_link)

	with open('subdomains-100.txt', 'r') as f:
		for line in f:
			line = line.rstrip()
			tmp = replace_subdomain(line)
			if tmp not in temp_links:
				if validators.url(tmp):
					temp_links.append(tmp)
		f.close()
	return temp_links

print(more_links())

