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

page = requests.get("https://www.google.com/search?ei=9Zb_W7PwO-W6ggeNjquwCg&q=NavigableString&oq=NavigableString&gs_l=psy-ab.12...0.0..333...0.0..0.0.0.......0......gws-wiz.H5KapB8mpMM")
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

print(words)
print(links)	
	