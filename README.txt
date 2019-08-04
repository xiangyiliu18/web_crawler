cse331 SBU 11/29/18
Web Crawler + Form Brute
Cheryl

2. Info
"http://songyy.pythonanywhere.com"

login_url = "https://3.16.240.57/wp-login.php"
starting_page = "http://songyy.pythonanywhere.com/quotes"
    #crawler.http_post("https://3.16.240.57/wp-login.php","usersdds","EN9fQcC3jnsS")


3. Limit:
  3.1 must use sockets to create http's Get and Post
  3.2 can use urllib.parse to cnvert relative urls to their absolute conterpart
