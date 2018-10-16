import requests
from retrying import retry
from lxml import etree
import f_check_ip
from f_connection_redis import F_redis

url = 'http://www.ip3366.net/free/?stype=1&page={}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Referer': 'http://www.ip3366.net/free/?stype=1&page=7',
}


@retry(stop_max_attempt_number=3)
def get_ip_list(url):
    """
    从代理网站获取IP的函数
    :param url: 目标网站的具体分页url
    :return: 返回值是以包含PORT的IP为元素的列表
    """
    ip_list = []
    res = requests.get(url, headers=headers, timeout=5)
    html = etree.HTML(res.text)
    t_list = html.xpath('//tbody/tr')
    for i in t_list:
        ip = i.xpath('./td[1]/text()')
        ip = ip[0] if ip[0] else '111.111.111.111'
        port = i.xpath('./td[2]/text()')
        port = port[0] if port[0] else '80'
        ip_list.append(ip + ':' + port)
    return ip_list


def main():
    # 获取每页的ｉｐ
    r = F_redis()
    for i in range(1, 11):
        ip_list = get_ip_list(url.format(i))
        for j in ip_list:
            if f_check_ip.check(j):
                r.insert_ip(j)
            else:
                continue
    print("10页ip爬区结束", "*"*50)


if __name__ == '__main__':
    # url = url.format(1)
    # ip_list = get_ip_list(url)
    # print(ip_list)
    main()