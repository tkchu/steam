# -*- coding:utf8 -*-
"""
本脚本用于获取steam tag及部分spy信息
"""
from conf import *
import json
import cfscrape

SPY_URL = "http://steamspy.com/api.php?request=appdetail&appid=%s"

scraper = cfscrape.create_scraper()

for info in myinfo.find():
    appid = info['appid']
    scraper.get(SPY_URL % appid)
    break

