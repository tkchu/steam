# -*- coding:utf8 -*-
"""
本脚本用于获取steam游戏的评论
"""
import json
from conf import *
from app import *
import datetime
import urllib
import urllib2
import time

REVIEW_URL = "https://store.steampowered.com/appreviews/{0}?json=1&language=all&filter=recent&cursor={1}&num_per_page=100&review_type=all&purchase_type=all"
# 此api每天仅能调用100000次，见 https://steamcommunity.com/dev/apiterms

count = 0
countMax = 40000
def getOneAppReview(appid, cursor, findSameReviewAndBreak = False):
    #根据AppID，游标来查询，返回下一个游标，如果出问题，则返回None
    #如果 findSameReviewAndBreak为真，当找到一样ID的Review时，返回当前游标而不是继续下去
    global count
    global countMax
    count += 1
    if count >= countMax:
        print "API Limit Break"
        return -1
    print "get reviews appid:"+str(appid)+"::"+str(cursor)

    reviewList = None
    try:
        url = REVIEW_URL.format(appid, urllib.quote_plus(cursor))
        response = urllib2.urlopen(url)
        if response:
            reviewList = response.read()
        else:
            return None
    except Exception as e:
        print e

    if not reviewList:
        return None
    reviewListJson = json.loads(reviewList.decode("utf8"))
    if reviewListJson["success"] != 1:
        return None
    for review in reviewListJson["reviews"]:
        review["appid"] = appid
        review["review_id"] = str(appid)+":"+str(review["recommendationid"])
        try:
            if(myreview.find_one({"review_id": review["review_id"]})):
                if(findSameReviewAndBreak):
                    return cursor
                else:
                    myreview.delete_one({"review_id": review["review_id"]})
                    myreview.insert_one(review)
            else:
                myreview.insert_one(review)
        except Exception as e:
            print e
            pass
    return reviewListJson["cursor"]

def getAppReview(appidInfo):
    appid = appInfo['appid']
    print "="*5 + str(appid) + ":" + "review" + "="*5

    if "total_reviews" not in appInfo:
        return None

    findSameReviewAndBreak = False
    if "review_update_time" in appInfo:
        if (datetime.datetime.now()- appInfo["review_update_time"]).days < 3:
            return None
        else:
            findSameReviewAndBreak = True

    reviewNum = appInfo["total_reviews"]
    cursor = "*"

    print "reviews:" + str(appid) + ":" +str(reviewNum) + ":" + time.strftime('%Y-%m-%d %H:%M:%S')
    while True:
        newCursor = getOneAppReview(appid, cursor, findSameReviewAndBreak)
        if newCursor == None:
            break
        if newCursor == -1:
            return -1
        if newCursor == cursor:
            myinfo.update_one({"appid":appid}, {"$set":{'review_update_time': datetime.datetime.now()}})
            break
        cursor = newCursor
    return None

if __name__ == '__main__':
    count = 0
    #appInfos = [x for x in myinfo.find({"type":"game","total_reviews":{"$gt":1000}})]
    appInfos = [x for x in myinfo.find({"type":"game","total_reviews":{"$gt":2000,"$lt":12000},"last_update_time":{"$exists":True}})]
    #appInfos = [x for x in myinfo.find({"type":"game","total_reviews":{"$exists":True} })]
    #appInfos = [x for x in myinfo.find({"appid":1076600})]
    appInfosLen = len(appInfos)
    reviewsCount = sum([info["total_reviews"] for info in appInfos])
    print "{0} app will get {1} reviews".format(appInfosLen, reviewsCount)
    print reviewsCount/100000/100.0

    for i,appInfo in enumerate(appInfos):
        print "appid:" + str(appInfo['appid']) + ":" + str(i) + '/' + str(appInfosLen)
        
        appLimit = getAppReview(appInfo)
        if appLimit == -1:
            break
