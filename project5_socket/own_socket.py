import socket
import sys
import urllib.request

from bs4 import BeautifulSoup


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
        _, _, host, path = url.split('/',3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        self.sock.connect(addr)
        sent = self.sock.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
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



####################################################
def parse_url(url):
    print("For manipulating data by using beautifuSoup")




###############################################################
  # 1. The scraping rules can be found in the robots.txt file.  which can be 
  #     found by adding a/robots.txt path to the main domain of the site
###############################################################
def crawl(urls_list,use_agent, choice,max_depth, max_total):
    ### the total url_list i need to crawl
    ## custome User_Agent
    ## choie --: Depth-first, or Breadth-first
    ## Maximum depth of pages to crawl
    ## Maximum total number of crawled pages
    print("crawl")


def main():
    sock=OwnSocket()
    response = sock.connect("http://songyy.pythonanywhere.com/quotes")
    response = b''.join(response)
    all_content = response.decode()

    header = all_content.split('\r\n\r\n')[0]

    content = all_content.split('\r\n\r\n')[1]

    with open("header.txt", "w") as f:
        f.write(header)
        f.close()
## Get html
    content = content.encode('utf8')
    with open("home.html", 'wb') as f:
         f.write(content)
         f.close()

    # get = urllib.request.urlopen("http://songyy.pythonanywhere.com/quotes")
    # html = get.read()
    # print(html)
    # soup = BeautifulSoup(html,features="")
    # with open("test.html", "w+") as f:
    #     f.write(str(soup.html.encode('utf8')))

main()