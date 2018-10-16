from redis import *
from f_check_ip import check


class F_redis(object):
    def __init__(self):
        """
        连接本地redis数据库，第５仓库
        """
        self.redis = StrictRedis(db=5)

    def insert_ip(self, ip):
        """
        向数据库中添加集合数据
        :param ip: 包含PORT的ip
        :return: 无
        """
        self.redis.sadd('ip', ip)
        # print(result)

    def get_ip(self):
        """
        从数据库中获取IP，并进行验证
        :return: 返回有效IP
        """
        ip = self.redis.srandmember('ip', 1)[0].decode('utf-8')
        # print(ip[0].decode('utf-8'), type(ip[0].decode('utf-8')), type(ip))
        if check(ip):
            return ip
        else:
            self.del_ip(ip)
            return self.get_ip()

    def get_all(self):
        return self.redis.smembers('ip')

    def del_ip(self, ip):
        """
        讲经过验证后无效的IP从数据库中删除
        :param ip: 包含PORT的IP
        :return: 无
        """
        self.redis.srem('ip', ip)


if __name__ == '__main__':
    r = F_redis()
    # for i in range(10):
    #     # r.insert_ip(i)
    #     ip = r.get_ip()
    #     print(ip, '*'*50)
    print(r.get_all())

