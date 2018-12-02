cse331 SBU 11/29/18
Web Crawler + Form Brute
Cheryl


2. Info
"http://songyy.pythonanywhere.com"


3. Limit:
  3.1 must use sockets to create http's Get and Post
  3.2 can use urllib.parse to cnvert relative urls to their absolute conterpart


No you are not. You are building a malicious crawler so you obviously don't have to follow what robots.txt says. The reason why you are reading it is to find sudomains and paths that you wouldn't be able to find just by crawling the website. In other words, you are using robots.txt for the opposite reason of why it was created.

Correct, the user agent is just sent to the website in a request header.  The project requirement is that the user should be able to specify the user agent string.
