import socket
import sys
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup

user_agent = None
'''
s = socket.socket()
s.settimeout(5)   # 5 seconds
try:
    s.connect(('123.123.123.123', 12345))         # "random" IP address and port
except socket.error, exc:
    print "Caught exception socket.error : %s" % exc
'''
# count_page = -1
class OneSocket:
    global user_agent
    def __init__(self):
        ### AF_INET---> refers to the address family ipv4
        ### SOCK_STREAM ---> means connection oriented TCP protocol
        ### This is client
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    '''
        self.sock.connect("http://songyy.pythonanywhere.com/quotes", 22)
        onc the connect completes, the socket 'sock' can be used to send
        in a request for the text of the page
    '''
    def connect(self, url):
        global user_agent
        url = urlparse(url)
        host = url.hostname
        path = url.path
        addr = socket.getaddrinfo(host, 80)[0][-1]
        self.sock.connect(addr)
        if(user_agent):
            sent = self.sock.sendall(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\nUser-agent: %s\r\n\r\n' % (path, host, user_agent), 'utf8'))
            if sent == 0:
                raise RuntimeError("socket connection broken")
        ############################## Get Response  ####################################
        total_data=[]

        while True:
            data = self.sock.recv(4096)
            if data:
                total_data.append(data)
            else:
                break
        self.sock.close()
        return total_data


    def get_response(self, url, filename):  ## one page response
        response = self.connect(url)
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

###############################################################
  # 1. The scraping rules can be found in the robots.txt file.  which can be 
  #     found by adding a/robots.txt path to the main domain of the site
###############################################################


class Crawler:

    def __init__(self):
        self.words = []  ### Empty words list
        self.choice = 'depth' ##Depth-first(depth) / Breadth-first(breadth)
        self.maxD = 1 ##  max depth of pages to crawl
        self.maxTotal = 0 ## max total number of pages
        self.sock = None 

        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--user', nargs='?', type=str, metavar='user_agent', help='must be provide a custom user-agent for use', required=True)
        parser.add_argument('-c', '--choice', nargs='?', type=str, choices=['depth','breadth'], default='depth', help="Depth-first/Breadth-first choice of crawling", required=False)
        parser.add_argument('-d', '--depth', nargs='?', type=int, metavar='num', default=0, help="Maximum depth of pages to crawl", required=False)
        parser.add_argument('-p','--page', nargs='?', type=int, metavar='num', default=0, help='Maximum total number of crawled pages', required= False)
        sys.args = parser.parse_args()
    
    def help(self):
        parser.print_help()

    def http_get(self, url, filename):
        print("Get")
        global user_agent
        if user_agent:
            self.sock=OneSocket()
            self.sock.get_response(url, filename)

    def http_post(self):
        print("Post")



# def create_dict(words_file):
#     with open(words_file, 'r') as f:
#         words_list=[]
#         for line in f:
#             words_list += line.split()
#         f.close()

#     new_words_list =[]
#     for ele in words_list:
#         temp = ele.lower()
#         if temp not in new_words_list:
#             new_words_list.append(temp)
#     return new_words_list


def main():
    global user_agent
    crawler = Crawler()
    own_config = {}
    own_config['user_agent']= sys.args.user  # one user_agent
    own_config['choice'] = sys.args.choice  # breadth or depth
    own_config['depth']= sys.args.depth  #  depth of pages to crawling
    own_config['page'] = sys.args.page  # number of pages to crawled pages

    user_agent = own_config['user_agent']
    crawler.http_get("http://songyy.pythonanywhere.com/quotes", 'home.html')
    crawler.http_get("http://www.google.com", "home_1.html")




main()