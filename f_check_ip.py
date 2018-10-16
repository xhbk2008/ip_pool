import requests, json


"""
###http://httpbin.org/get?a=123&b=222的返回值:
{
  "args": {
    "a": "123",
    "b": "222"
  },
  "headers": {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "close",
    "Host": "httpbin.org",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
  },
  "origin": "123.115.50.12",
  "url": "http://httpbin.org/get?a=123&b=222"
}
"""

url = 'http://httpbin.org/get?a=123&b=222'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}


def check(ip):
    """

    :param ip: IP加PORT,格式192.168.0.1:5000
    :return: 返回值时布尔类型
    """
    proxies = {
        'http': ip,  # ip-->ip:port
        'https': ip
    }
    try:
        res = requests.get(url, headers, proxies=proxies, timeout=5).text
        result = json.loads(res)
    except Exception as e:
        print("问题IP:", ip)
        return False
    if result['origin'] == ip[0:ip.index(':')]:
        print(ip, '是个高匿名IP')
        return True
    else:
        print("问题IP:", ip)
        return False
