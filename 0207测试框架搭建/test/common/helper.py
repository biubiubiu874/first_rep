# -*- coding:utf-8 -*-
# _author_='lijiachang'
# @time :2020/2/25 9:58
import random


def generate_mobile():
    """
    随机生成一个号码
    """
    phone='1'+random.choice(['3','5','7','8','9'])
    for i in range(0,9):
        num=random.randint(0,9)
        phone=phone+str(num)
    return phone