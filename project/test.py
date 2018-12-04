import requests
import webbrowser







usr = 'log'
password ='pwd'
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
headers ={
	'Userr_Agent': user_agent
}
login_data ={
	'log':'user',
	'pwd':"EN9fQcC3jnsS",
	#'csrf_token':"IjViNDI2MDhjMGM3Y2IwYmRkNTFmNTQ2MjliZDI3NzBjNzkzOGY3NDQi.XARP5Q.Hh7Hs1fCKFLRobNpnAWMVgv77oA"
	# 'wp-submit': 'Log In'
}

with requests.Session() as s:
	# url = "https://3.16.240.57/wp-login.php"
	url="http://3.16.240.57/wp-login.php"
	r = s.post(url, data = login_data, headers=headers, verify=False)
	with(open('final.html', "wb+")) as f:
		if r.url != url:
			print("cracke it !!!!")
		else:
			print('faile')
		print(r.status_code)
		f.write(r.content)