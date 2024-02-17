# -*- coding:utf8 -*-
"""
本脚本用于寻找好游戏
"""
from conf import *
import operator

fun_word = "addict"

if __name__ == '__main__':
    infos = myinfo.find({"type":"game","total_reviews":{"$gt":500,"$lt":10000}})
    
    print "{0} games to find".format(infos.count())

    count = 0
    allInfoSort = []
    for info in infos:
        appid = info["appid"]
        result = myreview.find({"appid":appid, "language":"english", "review":{"$regex":fun_word}})
        result_count = result.count()

        info["fun_count"] = result_count
        info["fun_rate"] = result_count * 1.0 /info["total_reviews"]
        allInfoSort.append(info)

        count += 1
        print "{0}/{1}".format(count,infos.count())

    allInfoSort = sorted(allInfoSort, key = operator.itemgetter("fun_count"))
    #allInfoSort = sorted(allInfoSort, key = operator.itemgetter("fun_rate"))

    for info in allInfoSort:
        rate = info["fun_count"] * 1.0 / info["total_reviews"]
        try:
            if info["is_free"]:
                print "Free {0}:{1} has {2} {3} reviews in {4}, rate:{5}".format(info["appid"], info["name"].encode('utf-8'), info["fun_count"], fun_word, info["total_reviews"], rate)
            else:
                print "{0}:{1} has {2} {3} reviews in {4}, rate:{5}".format(info["appid"], info["name"].encode('utf-8'), info["fun_count"], fun_word, info["total_reviews"], rate)
        except Exception as e:
            print e