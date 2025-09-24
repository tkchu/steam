# -*- coding:utf8 -*-
"""
本脚本用于寻找一些值得参考的游戏
"""
from conf import *
import json
import datetime

TOTAL_REVIEWS_MIN = 5000
TOTAL_REVIEWS_MAX = 10000
EXCLUDE_TAGS = {
    "",
}
if __name__ == '__main__':
    infos = [info for info in myinfo.find(
        {
        "type":"game",
        "is_free":False,
        "appid":{"$exists":True},
        "supported_languages":{"$regex":"Chine"},
        "total_reviews":{"$gt":TOTAL_REVIEWS_MIN,"$lt":TOTAL_REVIEWS_MAX},
        })]
    infos.sort(key=lambda x:x[u'total_positive'])
    for game in infos:
        print("{0},#**{1}** has {2} positive reviews.".format(game["appid"], game[u"name"], game["total_positive"]))
    print(len(infos))

