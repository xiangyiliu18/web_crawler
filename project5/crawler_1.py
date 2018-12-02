import requests
import webbrowser


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
headers ={
	'user_agent': user_agent
}
login_data ={
	'log':'user',
	'pwd':"EN9fQcC3jnsS",
	# 'wp-submit': 'Log In'
}

with requests.Session() as s:
	# url = "https://3.16.240.57/wp-login.php"
	url="http://3.16.240.57/wp-login.php"
	r = s.post(url, data = login_data, headers=headers, verify=False)
	with(open('f1.html', "wb+")) as f:
		print(r.status_code)
		print("\nNew URL", r.url)
		print("\nRedirection:")
		for i in r.history:
			print(i.status_code, i.url)
			# Open r in the browser to check if I logged in
			new = 2  # open in a new tab, if possible
			# webbrowser.open(r.url, new=new)

		f.write(r.content)