import requests

from bs4 import BeautifulSoup

from getpass import getpass

url = 'https://jutge.org/'
login_data = {'email': 'aleix.bone@est.fib.upc.edu', 'password': getpass('Password: '), 'submit': ''}
s = requests.Session()
r = s.post(url, data=login_data)


cookies = requests.utils.dict_from_cookiejar(s.cookies)

web = 'https://jutge.org/problems/X71570_ca'

open('file_a.txt','w').write(s.get(web).text)

response = requests.get(web, cookies=cookies)

open('file_b.txt','w').write(response.text)
