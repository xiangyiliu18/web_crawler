import socket
import sys
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup

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
        url = urlparse(url)
        host = url.hostname
        path = url.path
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
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--user', nargs='?', type=str, metavar='user_agent', help='must be provide a custom user-agent for use', required=True)
        parser.add_argument('-c', '--choice', nargs='?', type=str, choices=['depth','breadth'], default='depth', help="Depth-first/Breadth-first choice of crawling", required=False)
        parser.add_argument('-d', '--depth', nargs='?', type=int, metavar='num', default=0, help="Maximum depth of pages to crawl", required=False)
        parser.add_argument('-p','--page', nargs='?', type=int, metavar='num', default=0, help='Maximum total number of crawled pages', required= False)
        sys.args = parser.parse_args()
    
    def help(self):
        parser.print_help()


def create_dict(words_file):
    with open(words_file, 'r') as f:
        words_list=[]
        for line in f:
            words_list += line.split()
        f.close()
        return words_list


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
    sock=OwnSocket()
    sock.get_response("http://songyy.pythonanywhere.com/quotes", "home.html")
    crawler = Crawler()
    own_config = dict()
    own_config['user_agent']= sys.args.user  # one user_agent
    own_config['choice'] = sys.args.choice   # breadth or depth
    own_config['depth']= sys.args.depth      # depth of pages to crawling
    own_config['page'] = sys.args.page       # number of pages to crawled pages


main()