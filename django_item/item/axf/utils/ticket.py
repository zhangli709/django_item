import random
from time import time


def ticket_make():
    """
    创建密钥
    :return:
    """
    s = 'abcdefghijklmnopqrstuvwxyz0123456789'
    ticket = ''
    for i in range(15):
        ticket += random.choice(s)
    now_time = int(time())
    ticket = 'TK' + ticket + str(now_time)

    return ticket
