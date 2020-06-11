# -*- coding:utf-8 -*-
# _author_='lijiachang'
# @time :2020/3/1 19:36
testime_all=0
i=0
time=[]
with open(r'D:\PycharmProjects\data.log',"r",encoding='utf-8')as f:
    while True:
        data=f.readline().strip('\n')
        if not data:
            break
        str=data.split(',',2)
        if str[2]=='0':
            testime_all=int(str[1])+testime_all
            i=i+1
            time.append(int(str[1]))
time_ave=testime_all/i
maxtime=max(time)
mintime=min(time)
print("%.2f"%time_ave)
print(maxtime)
print(mintime)
