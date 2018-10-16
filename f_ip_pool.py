from flask import Flask
from f_connection_redis import F_redis
from f_get_ip import main
from threading import Thread
from f_check_ip import check


app = Flask(__name__)
r = F_redis()


@app.route('/')
def getOne():
    return r.get_ip()


def checkGotIp():
    ip_set_b = r.get_all()
    for i in ip_set_b:
        if not check(i.decode('utf-8')):
            r.del_ip(i.decode('utf-8'))
    print("校验以存在的ip结束%s" % ("!"*50))


if __name__ == '__main__':
    # 一下两个函数需要并发
    # app.run()
    # main()

    t = Thread(target=checkGotIp)
    t.start()

    t1 = Thread(target=app.run)
    t1.start()

    t2 = Thread(target=main)
    t2.start()
