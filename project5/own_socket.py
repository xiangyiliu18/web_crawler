import socket
import sys
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urljoin
import re

links_depth={}

words_file = None
user_agent = None

final_words= open("words_list.txt", "w+", encoding='utf-8')
'''
s = socket.socket()
s.settimeout(5)   # 5 seconds
try:
    s.connect(('123.123.123.123', 12345))         # "random" IP address and port
except socket.error, exc:
    print "Caught exception socket.error : %s" % exc
'''
class OneSocket:
    global user_agent
    def __init__(self):
        ### AF_INET---> refers to the address family ipv4
        ### SOCK_STREAM ---> means connection oriented TCP protocol
        ### This is client
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, url):
        global user_agent
        url = urlparse(url)
        host = url.hostname
        path = url.path
        addr = socket.getaddrinfo(host, 80)[0][-1]
        self.sock.connect(addr)

    def get_response(self, url, filename):  ## one page response
        self.connect(url)
        if(user_agent):
            sent = self.sock.sendall(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\nUser-agent: %s\r\n\r\n' % (path, host, user_agent), 'utf8'))
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

    def get_post(self, url):
        self.connect(url)
        if(user_agent):
            post_msg ='Post /%s HTTP/1.0\r\nHost: %s\r\nuserName=%s&password=%s\r\nUser-agent: %s\r\n\r\n' % (path, host,userName,password,user_agent)
            sent = self.sock.sendall(bytes(post_msg), 'utf8')
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
        with open("header_post.txt", "w") as f:
            f.write(header)
            f.close()

        content = all_content.split('\r\n\r\n')[1]
        content = content.encode()
        with open("body_post.txt", 'wb') as f:
            f.write(content)
            f.close()

'''
##############################################################
   Create 'wordsList'
###############################################################
'''
def capitalization_permutations(s):
    """Generates the different ways of capitalizing the letters in
    the string s."""

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
    global final_words

    for line in words_list:
        temp = list(capitalization_permutations(line))
        for item in temp:
            final_words.write("%s\n" % item)

# Function to reverse a string
def reverse(string):
    string = string[::-1]
    return string

# reverse
def reverse_chars(words_list):
    global final_words

    for line in words_list:
        final_words.write("%s\n" %reverse(line))


# leet-speak with the following case-insensitive conversions
def leet_speak(words_list):
    global final_words

    for line in words_list:
        line = line.replace('a', '4').replace('A', '4')
        line = line.replace('e', '3').replace('E', '3')
        line = line.replace('l', '1').replace('L', '1')
        line = line.replace('t', '7').replace('T', '7')
        line = line.replace('o', '0').replace('O', '0')
        final_words.write("%s\n" %line)


def create_dict(words_file):  ## words_file = base_words
    words_list =[]
    base_words = open("base_words.txt", 'w', encoding='utf-8')
    with open(words_file, mode="r", encoding='utf-8') as f:
        for line in f:
            temp = line.lower()
            temp= re.sub(r'\W+', '', temp)
            if temp not in words_list:
                base_words.write("%s\n" %temp)
                words_list.append(temp)
        f.close()
    base_words.close()

    if words_list != []:
        print(words_list)
        final_words = open("words_list.txt", 'w+', encoding='utf-8')
        lower_upper_permutation(words_list)
        reverse_chars(words_list)
        leet_speak(words_list)

    final_words.close()

##############################################
#  Cawler  Class  and basic function
###############################################

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
    ############################################## Help #########################
    def help(self):
        parser.print_help()

    ############################################## Http--Get #########################
    def http_get(self, url, filename):
        print("Get")
        global user_agent
        if user_agent:
            self.sock=OneSocket()
            self.sock.get_response(url, filename)

    ############################################## Http--Post #########################
    def http_post(self,url):
        print("Post")
        global user_agent
        if user_agent:
            self.sock=OneSocket()
            self.sock.get_post(url)


    ############################################## Links List #########################
    def dfs(self, links_list):
        print("DFS")




##############################################################################################
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

#finding and putting all the words found on the website into the list words[] 
def find_words(soup,words):
    texts = soup.find_all(text=True)
    visible_texts = list(filter(tag_visible, texts)) 
    for n in range(len(visible_texts)):
        tmp=visible_texts[n].split()
        for i in range(len(tmp)):
            words.append(tmp[i])

#finding and putting all the links found on the website into the list links_depth[] at a specific level
def find_links(soup,links_depth,depth):
    allLinks = soup.findAll('a',href=True)
    temp_list = []
    for n in allLinks:
        temp_list.append(urljoin("http://songyy.pythonanywhere.com/quotes",n['href']))

    if depth in links_depth:
        links_depth[depth].extend(temp_list)
    else:
        links_depth[depth]=temp_list
 

#writing to output files
def output_files(words,links_depth,login):
    new_words =('\n'.join(words)).encode('utf-8','ignore')
    w = open("words.txt", "wb")
    w.write(new_words)

    #global links_depth
    l = open("links.txt", "wb")
    for n in links_depth:
        new_links =('\n'.join(links_depth[n])).encode('utf-8','ignore')
        l.write(new_links)

    w.close()
    l.close()


def main():
    global user_agent
    global final_words

    crawler = Crawler()
    own_config = dict()
    own_config['user_agent']= sys.args.user  # one user_agent
    own_config['choice'] = sys.args.choice  # breadth or depth
    own_config['depth']= sys.args.depth  #  depth of pages to crawling
    own_config['page'] = sys.args.page  # number of pages to crawled pages

    #3 lists
    words=[]
    login=[]

    web = open("home.html", encoding='utf8')
    soup = BeautifulSoup(web, "html.parser")
    links_depth[0]= ["http://songyy.pythonanywhere.com/quotes"]

    find_words(soup,words)
    find_links(soup,links_depth,1)   

    # depth=1 || page=1
    if own_config['depth']==1 or own_config['page']==1:
        output_files(words,links_depth,login)
        exit(0) 

    #Depth First Search
    # if own_config['choice'] == 'depth':
    #     print("here")

    # #Breadth First Search
    # else:
    #    page_opened=1
    #    current_depth=1 
    #    for cd in range(1,own_config['depth']-1):
    #         for each_link in links_depth[cd]:
    #             page_opened+=1
                

    #             if page_opened==own_config['page']:
    #                 break;
    #     if page_opened==own_config['page']:
    #         break;            
    output_files(words,links_depth,login)

main()