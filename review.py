# -*- coding:utf8 -*-
"""
本脚本用于获取steam游戏的评论
"""
import json
from conf import *
from app import *
REVIEW_URL = "https://store.steampowered.com/appreviews/{0}?json=1&language=all&filter=recent&start_offset={1}&num_per_page=100&review_type=all&purchase_type=all"

def getOneAppReview(appid, start_offset = 0):
    print "get appid:"+str(appid)+"::"+str(start_offset)
    reviewList = send_req(REVIEW_URL.format(appid, start_offset))
    if not reviewList:
        return
    reviewListJson = json.loads(reviewList.decode("utf8"))
    if reviewListJson["success"] != 1:
        return
    for review in reviewListJson["reviews"]:
        review["appid"] = appid
        review["review_id"] = str(appid)+":"+str(review["recommendationid"])
        try:
            myreview.insert_one(review)
        except Exception as e:
            print e
            pass

def getAppReview(appid, appInfo = None):
    if appInfo:
        appid = appInfo['appid']
    else:
        appInfo = myinfo.find_one({"appid":appid})

    print "="*5 + str(appid) + ":" + "review" + "="*5


    if myreview.find_one({"appid":appid}):
        #print myreview.find_one({"appid":appid})
        return

    #reviewnum_now = myreview.find({"appid":appid}).count()
    #reviewNum = appInfo["total_reviews"] - reviewnum_now
    if "total_reviews" not in appInfo:
        return
    reviewNum =  appInfo["total_reviews"]

    start_offset = (reviewNum-1) // 100 * 100
    while start_offset >= 0:
        try:
            getOneAppReview(appid, start_offset)
        except Exception as e:
            print e
            start_offset = -1
        print("reviews:" + str(appid) + ":" +str(reviewNum) + ":" + time.strftime('%Y-%m-%d %H:%M:%S'))
        start_offset -= 100

if __name__ == '__main__':
    appids = [x['appid'] for x in myinfo.find()][66000:]
    for i,appid in enumerate(appids):
        print "appid:" + str(appid) + ":" + str(i) + '/' + str(len(appids))
        getAppReview(appid)
