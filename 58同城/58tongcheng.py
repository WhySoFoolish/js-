import requests
import cchardet
import re
import execjs
import os
import time


username = input('Enter username: ')
password = input('Enter password: ')


# 获取path
headers = {
    'authority': 'cdata.58.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'iframe',
    'accept-language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://passport.58.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'referer': 'https://passport.58.com/',
    'content-length': '0',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://passport.58.com',
    'pragma': 'no-cache',
}
session = requests.Session()
response = session.get('https://passport.58.com/login/', headers=headers).content
encoding = cchardet.detect(response)['encoding']
html = response.decode(encoding)
path = re.search('window.PATH = "(.+?)"', html).group(1)


# js生成jsonCallback和加密password
with open(os.getcwd() + '\\58tongcheng.js', 'r', encoding='utf8') as js_file:
    js = js_file.read()
js = execjs.compile(js)
password = js.call('get_password', password)
jc = js.call('get_jc')


# 获取所需cookies finger_session 和 ppStore_fingerprint
headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://passport.58.com/login/',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
}
params = {
    'finger2': 'zh-CN|24|2|8|1440_900|1440_860|-480|1|1|1|undefined|1|unknown|Win32|unknown|3|false|false|false|false|false|0_false_false|d41d8cd98f00b204e9800998ecf8427e|2a3efcbd0a53bbb98d8f4f80e9060ba3'
}
session.headers = headers
r = session.get("https://passport.58.com/sec/58/fingerprint", params=params)


# 获取token
params = {
    'source': '58-homepage-pc',
    'path': path,
    'psdk-d': 'jsdk',
    'psdk-v': '1.0.6',
    'callback': jc
}
session.headers["referer"] = "https://passport.58.com/login/?path=https%3A%2F%2Fbj.58.com%2F&source=58-homepage-pc&PGTID=0d100000-0000-1c0f-6f8d-1fbc67d111de&ClickID=2"
response = session.get('https://passport.58.com/58/login/init', params=params).content
encoding = cchardet.detect(response)['encoding']
html = response.decode(encoding)
token = re.search("\"token\":\"(.*?)\",", html).group(1)


# 获取cookies id58
# print(session.cookies)
# session.post('https://passportdatacollect.58.com/collect/init')
# print(session.cookies)


# 执行登录
finger_session = re.search('finger_session=(.+?) for', str(session.cookies)).group(1)
data = {
    'username': username,
    'password': password,
    'token': token,
    'source': '58-default-pc',
    'path': 'http%3A%2F%2Fmy.58.com%2F%3Fpts%3D{}'.format(int(time.time()*1000)),
    'domain': '58.com',
    'finger2': 'zh-CN|24|2|8|1440_900|1440_860|-480|1|1|1|undefined|1|unknown|Win32|unknown|3|false|false|false|false|false|0_false_false|d41d8cd98f00b204e9800998ecf8427e|2a3efcbd0a53bbb98d8f4f80e9060ba3',
    'isremember': 'false',
    'autologin': 'false',
    'isredirect': 'false',
    'psdk-d': 'jsdk',
    'psdk-v': '1.0.6',
    'fingerprint': finger_session,
    'callback': 'SDK_CALLBACK_FUN.successFun',
}
session.headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
session.headers['accept-encoding'] = 'gzip, deflate, br'
session.headers['accept-language'] = 'zh-CN,zh;q=0.9'
session.headers['content-type'] = 'application/x-www-form-urlencoded'
session.headers['origin'] = 'https://passport.58.com'
session.headers['referer'] = 'https://passport.58.com/login'
session.headers['upgrade-insecure-requests'] = '1'
print(session.cookies)
response = session.post('https://passport.58.com/58/login/pc/dologin', data=data).content
encoding = cchardet.detect(response)['encoding']
html = response.decode(encoding)
print(html)


# 请求个人主页
print(session.cookies)
response = session.get('http://my.58.com/index').content
encoding = cchardet.detect(response)['encoding']
html = response.decode(encoding)
print(session.cookies)
print(html)



