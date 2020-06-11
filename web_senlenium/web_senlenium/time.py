
# -*- coding:utf-8 -*-
# _author_='lijiachang'
# @time :2020/3/20 11:18

import datetime

now = datetime.datetime.now()
print(str(now-datetime.timedelta(days=-5))[:10])