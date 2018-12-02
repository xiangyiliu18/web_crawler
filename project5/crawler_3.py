import requests, lxml.html
s = requests.session()

### Here, we're getting the login page and then grabbing hidden form
### fields.  We're probably also getting several session cookies too.
login = s.get('http://3.16.240.57/wp-login.php')
login_html = lxml.html.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
print(form)
 
### Now that we have the hidden form fields, let's add in our 
### username and password.
form['log'] ='user' # Enter an email here.  Not mine.
form['pwd'] = 'EN9fQcC3jnsS'# I'm definitely not telling you my password.
response = s.post('http://3.16.240.57/wp-login.php', data=form)

# ### How can we tell that we logged in?  Well, these worked for me:
print(response.url)
# 'https://www.yelp.com/cleveland'
# >>> 'Stephen' in response.text
# True