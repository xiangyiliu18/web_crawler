import socket
import sys
import argparse
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urljoin
import base64
import re
import os


### Common Error Codes
error_codes={'400':'BAD REQUEST', '401': 'UNAUTHORIZED', '403': 'FORBIDDEN','404': 'NOT FOUND','410':' GONE','500': 'INTERNAL SERVER ERROR','501': 'NOT IMPLEMENTED','503':'SERVICE UNAVAILABLE','550':'PERMISSION DENIED'}
#####################For storting links base on BFS/DFS
links_depth={}
#######################   Website #################
starting_page=None
###################### Get all words (without any manipulation)######################
words_list = None
########### Get all words by applying for upper,lower, reverse and leet-speak conversion
final_words =None
############## Login URL ##############
login_url = []

###################### Personal Socket ###################
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
        try:
            self.sock.connect(addr)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            self.sock.close()
            exit(1)
        return (host, path)

    ## 'Get' Response
    def get_response(self, url, filename):  ## Response
        tmp=self.connect(url)
        if(user_agent):
            sent = self.sock.sendall(bytes('GET /%s HTTP/1.1\r\nHost: %s\r\nUser-Agent: %s\r\n\r\n' % (tmp[1], tmp[0], user_agent), 'utf8'))
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

    ## 'POST' request
    def post_response(self, url,filename, userName, password):
        global user_agent
        tmp=self.connect(url)
        if(user_agent):
            sent = self.sock.sendall(bytes('POST /%s HTTP/1.1\r\nHost: %s\r\nUser-Agent: %s\r\nAuthorization: %s:%s\r\n' % (tmp[1], tmp[0], user_agent), 'utf8'))
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

##############################################################
#                Create 'wordsList'
###############################################################
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
#  Basic functions
###############################################

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
    return words

#finding and putting all the links found on the website into the list links_depth[] at a specific level
def find_links(soup,links_depth,depth,logins,crawler):
    allLinks = soup.findAll('a',href=True)
    temp_list = []
    for n in allLinks:
        #check domain
        if (urlparse(n['href']).hostname)==None:
            thehttp=urljoin(starting_page,n['href'])
        else:
            if (urlparse(n['href']).hostname) != (urlparse(starting_page).hostname):
                continue
            thehttp=n['href']
        
        #check if the link is already in the dict
        found=0
        for n in range(len(links_depth)):
            if thehttp in links_depth[n]:
                found=1
        if thehttp in temp_list:
            found=1
        if found==0:
            if login_page(thehttp,crawler)==True:
                logins.append(thehttp)        
            temp_list.append(thehttp)

    if depth in links_depth:
        links_depth[depth].extend(temp_list)
    else:
        links_depth[depth]=temp_list


#check if it is a login page
def login_page(html,crawler):
    crawler.http_get(html , 'check.html')
    website = open("check.html", encoding='utf8')
    soup2 = BeautifulSoup(website, "html.parser")
    allforms = soup2.findAll('form')
    for form in allforms:
        if form.get('name')==None:
            continue
        s=form.get('name').encode().decode()
        if bool(re.search('log[\s_]*in',s ,re.IGNORECASE))==True:
            return True
        if bool(re.search('sign[\s_]*in', s,re.IGNORECASE))==True:
            return True
    return False        

#writing to output files
def output_files(words,links_depth,logins):
    new_words =('\n'.join(words)).encode('utf-8','ignore')
    w = open("words.txt", "wb")
    w.write(new_words)

    l = open("links.txt", "wb")
    for n in range(len(links_depth)):
        new_links =('\n'.join(links_depth[n])).encode('utf-8','ignore')
        l.write(new_links)

    new_logins =('\n'.join(logins)).encode('utf-8','ignore')
    log = open("logins.txt", "wb")
    log.write(new_logins)   

    w.close()
    l.close()
    log.close()

 
class Crawler:
    def __init__(self):
        self.choice = 'breadth' ##Depth-first(depth) / Breadth-first(breadth)
        self.depth = 0 ##  max depth of pages to crawl
        self.page = 0 ## max total number of pages
        self.user_agent = None
    ################### Argument && Configurable option
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--user', nargs='?+', type=str, metavar='user_agent', help='must be provide a custom user-agent for use', required=True)
        parser.add_argument('url', type=str, help="website's url", required=True)
        parser.add_argument('-c', '--choice', nargs='?', type=str, choices=['depth','breadth'], default='breadth', help="Depth-first/Breadth-first choice of crawling", required=False)
        parser.add_argument('-d', '--depth', nargs='?', type=int, metavar='num', default=0, help="Maximum depth of pages to crawl", required=False)
        parser.add_argument('-p','--page', nargs='?', type=int, metavar='num', default=0, help='Maximum total number of crawled pages', required= False)
        sys.args = parser.parse_args()

    ############################################## Help #########################
    def help(self):
        parser.print_help()

    ############################################## Http--Get #########################
    def http_get(self, url, filename):
        if self.user_agent:
            sock=OneSocket()
            self.sock.get_response(url, filename)

    ############################################## Http--Post #########################
    def http_post(self, url,userName, password):
        if self.user_agent:
            sock=OneSocket()
            self.sock.post_request(url,userName,password)

    ############################################## Links List ########################
#check dead end of the very first page
    def isDead(self):
        with open("header.txt", encoding='utf8') as f:
            if f:
                firstline=f.readline().rstrip()
                code = firstline.split(" ")[1]
                if error in error_codes:
                    return True
            else:  ########## no return
                return True

        return False

################### Main Entry ##############################
def main():
	global starting_page
	global words_list  ##### basic unique, lowercase words list
	global final_words ###  final words dict
	global login_url

	starting_page = None
	################ Remove created files
	if os.path.exists("words_list.txt"):
		os.remove("words_list.txt")
	if os.path.exists("words.txt"):
		os.remove("words.txt")

	############## Re-create necessary files ###############
	starting_page="http://songyy.pythonanywhere.com/quotes"
	words_list = open("words.txt", 'w+', encoding='utf-8')
	########### Get all words by applying for upper,lower, reverse and leet-speak conversion
	final_words= open("words_list.txt", "w+", encoding='utf-8')

	########################### Configurable Options ##############
	crawler = Crawler() #------------->  Own crawler
    crawler.user_agent= sys.args.user  # required
    crawler.choice = sys.args.choice  # breadth or depth ; default = breadth
    crawler.depth= sys.args.depth  #  the depth of pages to crawling; default = 0
    crawler.page= sys.args.page  # number of pages to crawled pages; default = 0

    ################ Begin to scrapy pages's words and links
    soup = None
    links_depth = {}

    starting_page ="https://ec2-3-16-240-57.us-east-2.compute.amazonaws.com"
     
    crawler.http_get(starting_page, 'home.html')
    if crawler.isDead():
        print("No available website can be crawled")
        exit(0)  

    ########################### Get words_list.txt && links.txt######################
    with open ("home.html", encoding='utf8') as web:
        soup = BeautifulSoup(web, "html.parser")
        links_depth[0]= [starting_page] ### start node of the tree

    if login_page(starting_page,crawler)==True:
        login_url.append(starting_page)
    find_words(soup,words)
    find_links(soup,links_depth,1,logins,crawler) 

    # depth=1 || page=1
    if own_config['depth']==1 or own_config['page']==1:
        output_files(words,links_depth,logins)
        exit(0) 

    #Depth First Search
    if own_config['choice'] == 'depth':
        print("HI")
        
    # Breadth First Search
    else:
        page_opened=1
        current_depth=1

        while(True):
            if own_config['depth']!=0 and current_depth==own_config['depth']:
                break
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
                    find_links(soup,links_depth,current_depth+1,logins,crawler) 

                    if page_opened==own_config['page']:
                        break
                if page_opened==own_config['page']:
                    break 
                current_depth+=1      
            else:
                break                

    output_files(words,links_depth,logins)
main()