import socket
import sys
import argparse
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urljoin


links_depth={}

# count_page = -1
class OwnSocket:
    def __init__(self, sock=None):
        if sock is None:
            ### AF_INET---> refers to the address family ipv4
            ### SOCK_STREAM ---> means connection oriented TCP protocol
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    '''
        self.sock.connect("http://songyy.pythonanywhere.com/quotes", 22)
        onc the connect completes, the socket 'sock' can be used to send
        in a request for the text of the page
    '''
    def connect(self, url):
        global count_page
        _, _, host, path = url.split('/',3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        self.sock.connect(addr)
        sent = self.sock.sendall(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        # count_page++
        if sent == 0:
                raise RuntimeError("socket connection broken")
        total_data=[]

        while True:
            data = self.sock.recv(2048)
            if data:
                total_data.append(data)
            else:
                break

        self.sock.close()
        return total_data


    def get_response(self,url, filename):  ## one page response
        response = self.connect(url)
        response = b''.join(response)
        all_content = response.decode()

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
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--user', nargs='?', type=str, metavar='user_agent', help='must be provide a custom user-agent for use', required=True)
        parser.add_argument('-c', '--choice', nargs='?', type=str, choices=['depth','breadth'], default='depth', help="Depth-first/Breadth-first choice of crawling", required=False)
        parser.add_argument('-d', '--depth', nargs='?', type=int, metavar='num', default=0, help="Maximum depth of pages to crawl", required=False)
        parser.add_argument('-p','--page', nargs='?', type=int, metavar='num', default=0, help='Maximum total number of crawled pages', required= False)
        sys.args = parser.parse_args()
    
    def help(self):
        parser.print_help()


def create_base_dict(words_file):
    with open(words_file, 'r') as f:
        words_list=[]
        for line in f:
            words_list += line.split()
        f.close()
        return words_list

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
   #global links_depth

    crawler = Crawler()
    sock=OwnSocket()
    sock.get_response("http://songyy.pythonanywhere.com/quotes", "home.html")
    crawler = Crawler()
    own_config = {}
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

    if own_config['choice'] == 'depth':
        print("DEPTH\n")

    else:
       print("BREADTH\n")

       page_opened=1
       current_depth=1 
       for cd in range(1,own_config['depth']-1):
            for each_link in links_depth[cd]:
                page_opened+=1
                





             


    output_files(words,links_depth,login)

main()