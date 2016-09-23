import requests
import configparser
from pprint import pprint

def create_session():
	cf = configparser.ConfigParser()
	cf.read('config.ini')
	cookies = cf.items('cookies')
	cookies = dict(cookies)
	cookies['aspsky']=r'username=%E5%91%A8%E6%85%A7%E6%95%8F&usercookies=3&userid=510555&useranony=&userhidden=2&password=dc80cdcb6602ba15'
	pprint(cookies)
	email = cf.get('info', 'email')
	password = cf.get('info', 'password')

	session = requests.session()
	login_data = {'email':email, 'password':password}
	header = {
	    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
        'Host': 'www.zhihu.com',
        'Referer': 'http://www.cc998.org/'
	}
	response = session.post('http://www.zhihu.com/login/email',data = login_data, headers = header)
	if response.json()['r'] == 1:
		print('Login Failed, reason is:')
		for reason in response.json()['data']:
			print(response.json()['data'][reason])
		print('So we use cookies to login in...')
		has_cookies = False
		for key in cookies:
			if key != '__name__' and cookies[key] != '':
				has_cookies = True
				break
		if has_cookies is False:
			raise ValueError('please perfect config.ini')
		else:
			response = session.get('http://www.cc98.org/login.asp', cookies=cookies)
	with open('login.html', 'w') as fp:
		fp.write(str(response.content))

	return session, cookies

if __name__ == '__main__':
	requests_session, requests_cookies = create_session()
	url = 'http://www.cc98.org/list.asp?boardid=182'
	content = requests_session.get(url, cookies = requests_cookies)
	#content = requests.get(url)
	print(content.content.decode())