import socket
import sys
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urljoin

error_codes=['400 BAD REQUEST', '401 UNAUTHORIZED', '403 FORBIDDEN','404 NOT FOUND','410 GONE','500 INTERNAL SERVER ERROR','501 NOT IMPLEMENTED','503 SERVICE UNAVAILABLE','550 PERMISSION DENIED']

links_depth={} #For BFS

starting_page="http://songyy.pythonanywhere.com/quotes"

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


# All upper and lowercase permutations of a string
lower_upper = open("lower_upper.txt", "w")


def lower_upper_permutation(words_list):
    with open(words_list, 'r') as f:
        for line in f:
            temp = list(capitalization_permutations(line))
            for item in temp:
                lower_upper.write("%s" % item)
        f.close()
    lower_upper.close()


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
        thehttp=urljoin(starting_page,n['href'])
        
        #check if the link is already in the dict
        found=0
        for n in range(len(links_depth)):
            if thehttp in links_depth[n]:
                found=1
        if thehttp in temp_list:
            found=1
        if found==0:        
            temp_list.append(thehttp)

    if depth in links_depth:
        links_depth[depth].extend(temp_list)
    else:
        links_depth[depth]=temp_list
 

#writing to output files
def output_files(words,links_depth,login):
    new_words =('\n'.join(words)).encode('utf-8','ignore')
    w = open("words.txt", "wb")
    w.write(new_words)

    l = open("links.txt", "wb")
    for n in range(len(links_depth)):
        new_links =('\n'.join(links_depth[n])).encode('utf-8','ignore')
        l.write(new_links)

    w.close()
    l.close()

# reverse a word file
reversed_words_file = open("reversed_words.txt", "w")


def reverse_chars(words_list):
    with open(words_list, 'r') as f:
        for line in f:
            reversed_words_file.write(reverse(line))
            # print(reverse(line))
        f.close()
    reversed_words_file.close()


# Function to reverse a string
def reverse(string):
    string = string[::-1]
    return string


# leet-speak with the following case-insensitive conversions:
leet_speak_file = open("leet_speak_file.txt", "w")


def leet_speak(words_list):
    with open(words_list, 'r') as f:
        for line in f:
            line = line.replace('a', '4').replace('A', '4')
            line = line.replace('e', '3').replace('E', '3')
            line = line.replace('l', '1').replace('L', '1')
            line = line.replace('t', '7').replace('T', '7')
            line = line.replace('o', '0').replace('O', '0')
            leet_speak_file.write(line)
        f.close()
    leet_speak_file.close()

def main():
    global user_agent

    crawler = Crawler()
    own_config = dict()
    own_config['user_agent']= sys.args.user  # one user_agent
    own_config['choice'] = sys.args.choice  # breadth or depth
    own_config['depth']= sys.args.depth  #  depth of pages to crawling
    own_config['page'] = sys.args.page  # number of pages to crawled pages
    user_agent = own_config['user_agent']
    crawler.http_get(starting_page, 'home.html')

    #check deadend of the very first page
    header = open("header.txt", encoding='utf8')
    firstline=header.readline().rstrip()
    for codes in error_codes: 
        error_message="HTTP/1.1 "+codes
        if firstline==error_message:
            print("Cannot open this page!")
            exit(1)
            

    #2 lists
    words=[]
    login=[]

    web = open("home.html", encoding='utf8')
    soup = BeautifulSoup(web, "html.parser")
    links_depth[0]= [starting_page]

    find_words(soup,words)
    find_links(soup,links_depth,1) 

    # depth=1 || page=1
    if own_config['depth']==1 or own_config['page']==1:
        output_files(words,links_depth,login)
        exit(0) 

    #Depth First Search
    if own_config['choice'] == 'depth':
        print("HI")
        
    #hardcoding it first may change this value later
    if(own_config['depth']==0):
        own_config['depth']=1000

    # Breadth First Search
    else:
        page_opened=1
        for current_depth in range(1,own_config['depth']-1):
            if current_depth in links_depth:
                for each_link in links_depth[current_depth]:
                    crawler.http_get(each_link, 'home.html')

                    #check deadend
                    header = open("header.txt", encoding='utf8')
                    firstline=header.readline().rstrip()
                    error=0
                    for codes in error_codes: 
                        error_message="HTTP/1.1 "+codes
                        if firstline==error_message:
                            error=1
                    if error==1:
                        continue        

                    page_opened+=1
                    web = open("home.html", encoding='utf8')
                    soup = BeautifulSoup(web, "html.parser")
                    
                    find_words(soup,words)
                    find_links(soup,links_depth,current_depth+1) 

                    if page_opened==own_config['page']:
                        break
                if page_opened==own_config['page']:
                    break   
            else:
                break                
    
    output_files(words,links_depth,login)
           
main()