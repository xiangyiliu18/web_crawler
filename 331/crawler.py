import socket
import sys
import argparse
from urllib.parse import urlparse, urljoin, urlsplit, urlunsplit
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

### Common Error Codes
error_codes={'400':'BAD REQUEST', '401': 'UNAUTHORIZED', '403': 'FORBIDDEN','404': 'NOT FOUND','410':' GONE',
	'500': 'INTERNAL SERVER ERROR','501': 'NOT IMPLEMENTED','503':'SERVICE UNAVAILABLE','550':'PERMISSION DENIED'}

### Main Website ###
website = None
count_page = 0
count_depth = 0
login_url=[]
user_agent = None
page = 1
depth = 1
crawled_links=[]


##############################################################
#                Create 'wordsList'
###############################################################
def capitalization_permutations(s):
    # >>> list(capitalization_permutations('abc'))
    # ['ABC', 'aBC', 'AbC', 'abC', 'ABc', 'aBc', 'Abc', 'abc']
    # >>> list(capitalization_permutations(''))
    # ['']
    # >>> list(capitalization_permutations('X*Y'))
    # ['X*Y', 'x*Y', 'X*y', 'x*y']
    if s == '':
        yield ''
        return
    for rest in capitalization_permutations(s[1:]):
        yield s[0].upper() + rest
        if s[0].upper() != s[0].lower():
            yield s[0].lower() + rest

def lower_upper_permutation(words_list):
	new_list =[]
	for line in words_list:
		temp = list(capitalization_permutations(line))
		for item in temp:
			new_list.append(item)
	return new_list

# Function to reverse a string
def reverse(string):
    string = string[::-1]
    return string

# reverse
def reverse_chars(words_list):
	temp_list =[]
	for line in words_list:
		temp = reverse(line)
		if temp not in temp_list and temp not in words_list:
			temp_list.append(temp)
	return temp_list

# leet-speak with the following case-insensitive conversions
def leet_speak(words_list):
	temp_list = []
	for line in words_list:
		line = line.replace('a', '4').replace('A', '4')
		line = line.replace('e', '3').replace('E', '3')
		line = line.replace('l', '1').replace('L', '1')
		line = line.replace('t', '7').replace('T', '7')
		line = line.replace('o', '0').replace('O', '0')
		if line not in temp_list and line not in words_list:
			temp_list.append(line)
	return temp_list


def create_dict(words_file):  ## words_file = words.txt
	words_list =[]
	final_words = open("words_list.txt", "w+")
	with open(words_file, 'r', encoding="utf-8") as f:
		for line in f:
			if line and line.strip() !='':
				line = line.strip()
				temp = line.lower()
				if temp not in words_list:
					words_list.append(temp)
		f.close()
	if words_list != []:
		tmp = lower_upper_permutation(words_list)
		tmp = '\n'.join(tmp)
		tmp = tmp.strip()
		final_words.write(tmp)
		tmp = reverse_chars(words_list)
		tmp = '\n'.join(tmp)
		tmp = tmp.strip()
		final_words.write(tmp)
		tmp = leet_speak(words_list)
		tmp = '\n'.join(tmp)
		tmp = tmp.strip()
		final_words.write(tmp)
		final_words.close()
	else:
		print("No words")

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
    		with open('header.txt', 'w') as f:
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
    				break
    	self.split_response(response,filename)

    def post_response():
    	print("post")


############################## Crawler####################################
class Crawler:
	def __init__(self):
		self.choice = 'breadth'  ## Depth-first/Breadth-first choice of crawling -- deafult is breadth
		self.depth = 0  ## 0 stands for no limitation
		self.page = 0 ## 0 stands for no limitaion

		parser = argparse.ArgumentParser()
		parser.add_argument('-u', '--user', nargs='?', type=str, metavar='user_agent', help='must be provide a custom user-agent for use', required=True)
		parser.add_argument('url', type=str, help="please enter website's url")
		parser.add_argument('-c', '--choice', nargs='?', type=str, choices=['depth','breadth'], default='breadth', help="Depth-first/Breadth-first choice of crawling", required=False)
		parser.add_argument('-d', '--depth', nargs='?', type=int, metavar='num', default=0, help="Maximum depth of pages to crawl", required=False)
		parser.add_argument('-p','--page', nargs='?', type=int, metavar='num', default=0, help='Maximum total number of crawled pages', required= False)
		sys.args = parser.parse_args()

####################  Get Request ############################
	def http_get(self, url, filename):
		sock = MySocket()
		sock.get_response(url,filename)

	def isDead(self):
		with open("header.txt", encoding='utf-8') as f:
			firstline = f.readline().rstrip()
			code = firstline.split(' ')[1]
			if code in error_codes:
				return True
			else:
				return False
		return False

	def check_login(self,url):
		global login_url
		if "login" in url and '?' not in url:
			if url not in login_url:
				login_url.append(url)


####################################  Basic Functions ##############################
def tag_visible(element):
	if element.parent.name in ['style','script', 'head', 'title', 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	return True

## find one page's words
def find_words(soup,words):
    texts = soup.find_all(text=True)
    visible_texts = list(filter(tag_visible, texts))
    for n in range(len(visible_texts)):
    	tmp=visible_texts[n].split()
    	for i in range(len(tmp)):
    		tmp[i]= re.sub(r'[^a-zA-Z0-9!#$%&*+-<=>?@^_~]', '', tmp[i])
    		if tmp[i] !='':
    			if tmp[i] not in words:
    				words.append(tmp[i])
    return words

### find one page's links
def find_links(soup):
	global website
	allLinks = soup.findAll('a', href = True)
	temp_list = []
	domain = urlsplit(website)[1].split(':')[0]
	for ele in allLinks:
		thehttp=urlparse(ele['href'])
		## netloc -- network location part: domain
		if(thehttp.netloc == domain):
			thehttp = urljoin(website, ele['href'])
		else:
			continue
		if thehttp not in temp_list:
			temp_list.append(thehttp)
	return temp_list
#finding and putting all the links found on the website into the list links_depth[] at a specific level
def find_links_bfs(soup,links_depth,depth,logins,crawler):
	allLinks = find_links(soup)
	temp_list=[]
	for ele in allLinks:
		found = 0
		for n in range(len(links_depth)):
			if ele in links_depth[n]:
				found = 1
				break
		if ele in temp_list:
			found = 1
		if found == 0:
			crawler.check_login(ele)
			temp_list.append(ele)

	if depth in links_depth:
		links_depth[depth].extend(temp_list)
	else:
		links_depth[depth]=temp_list


################ BFS ####################
def do_bfs(crawler, words, links_depth):
	global page
	current_depth = 1
	page_opened = page
	while(1):
		if (crawler.depth != 0) and (current_depth == crawler.depth):
			break
		if current_depth in links_depth:
			for each_link in links_depth[current_depth]:
				crawler.http_get(each_link, "content.html")
				if crawler.isDead():
					continue
				page_opened += 1
				web = open("content.html", encoding ='utf8')
				soup = BeautifulSoup(web, 'html.parser')
				words = find_words(soup, words)
				find_links_bfs(soup, links_depth, current_depth+1, login_url, crawler)
				if page_opened == crawler.page:
					break
			if page_opened == crawler.page:
				break
			current_depth += 1
		else:
			break
	page = page_opened
	return words

####################### DFS -- recursion ##############################
'''
crawler -- the instantiated Crawler class
words -- store the page's words
links -- store the page's links
crawler --links -- store the links which already are crawled, avoid repetation
page -- current crawled pages
depth - current crawled depth
'''
def do_dfs(crawler, words, links):
	global login_url
	global page
	global depth
	global crawled_links

	while(links):
		if crawler.page != 0 and page >= crawler.page:
			break
		if  crawler.depth != 0 and depth > crawler.depth:
			break
		temp = links.pop(0)  ## remove and return the first element of the links array
		if temp not in crawled_links:
			crawler.http_get(temp, "content.html")
			if crawler.isDead():
				continue
			crawler.check_login(temp)
			web = open("content.html", encoding ='utf-8')
			soup = BeautifulSoup(web, "html.parser")
			words = find_words(soup, words)
			t_links = find_links(soup)
			crawled_links.append(temp)
			page += 1
			depth += 1
			if len(t_links) > 0:
				do_dfs(crawler, words, t_links)
			else:
				depth -= 1
	return (words)

#change subdomain
def replace_subdomain(subdomain):
	global website
	old_host = list(urlsplit(website))
	old_host[1] = subdomain+'.'+old_host[1]
	new_host = urlunsplit(old_host)
	return new_host


def more_links(crawler):
	global website
	temp_links =[]
	robot_website = website + '/robots.txt'
	crawler.http_get(robot_website, "robots.txt")
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


def cracker(words):
	global login_url
	with open("words.txt", "w+", encoding="utf-8") as f:
		if 'user' not in words:
			words.append('user')
		if 'EN9fQcC3jnsS' not in words:
			words.append('EN9fQcC3jnsS')
		words = "\n".join(words)
		words = words.rstrip()
		f.write(words)
		f.close()
	create_dict("words.txt")
#######################  Main function #####################
def main():
	global user_agent
	global website
	global login_url
	global page
	global depth
	global crawled_links

	words = []
	links = []

	crawler = Crawler()
	user_agent = sys.args.user
	website = sys.args.url
	crawler.choice = sys.args.choice
	crawler.depth = sys.args.depth
	crawler.page = sys.args.page

	crawler.http_get(website, "content.html")
	if crawler.isDead():
		print("This website is dead-end page!!")
		exit(0)
	crawler.check_login(website)

	web = open("content.html", encoding = "utf-8")
	soup = BeautifulSoup(web, "html.parser")
	words = find_words(soup, words)
	links = find_links(soup)

	extra_links = more_links(crawler)

	if crawler.page == 1 or crawler.depth == 1:
		print()
	else:
		if crawler.choice == 'depth':
			do_dfs(crawler, words, links)
			print(page)
			if crawler.page == 0 or (page < crawler.page):
				depth = 1
				do_dfs(crawler,words,extra_links) 
		else:
			links_depth={}
			links_depth[0] = [website]
			find_links_bfs(soup,links_depth,1,login_url,crawler) 
			do_bfs(crawler, words, links_depth)
			if crawler.page == 0 or (page < crawler.page):
				links_depth = {}
				links_depth[0] = extra_links
				find_links_bfs(soup,links_depth,1,login_url,crawler)
				do_bfs(crawler, words, links_depth) 
	if words:
		cracker(words)
	crawler.http_get(login_url[0], 'login.html')
	with open("login.html", encoding= 'utf8') as f:
		soup2 = BeautifulSoup(f,"html.parser")
		allForm = soup2.findAll('form')
		user= None
		pwd = None
		for ele in allForm:
			t = ele.find('input').get('id')
			pwd = ele.find('input', type="password").get('name')
			if "log" in t:
				user = ele.find('input').get('name')

	return (user, pwd)

(user_1,pwd_1) =  main()

