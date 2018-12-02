from bs4 import BeautifulSoup
from bs4.element import Comment
import requests

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

words=[]
links=[]

page = requests.get("http://songyy.pythonanywhere.com")
soup = BeautifulSoup(page.content, "html.parser")

texts = soup.find_all(text=True)
visible_texts = list(filter(tag_visible, texts)) 
allLinks = soup.findAll('a',href=True)

#putting all the words found on the website into the list words[] 
for n in range(len(visible_texts)):
	tmp=visible_texts[n].split()
	for i in range(len(tmp)):
		words.append(tmp[i])

#putting all the links found on the website into the list links[] 
for n in allLinks:	
	links.append(n['href'])


#writing to files
new_words =('\n'.join(words)).encode()
w = open("words.txt", "wb")
w.write(new_words)

new_links =('\n'.join(links)).encode()
l = open("links.txt", "w")
l.write(new_links)

w.close()
l.close()	
	