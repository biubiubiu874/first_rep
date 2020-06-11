# -*- coding:utf-8 -*-
# _author_='lijiachang'
# @time :2020/2/5 21:17
import yaml

def yaml_read(file_path):
    with open(file_path,encoding="utf-8") as f:
        data=yaml.load(f.read(), Loader=yaml.FullLoader)
    return data


