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

def updateTotalReview(appid, reviewListJson):
    reviewStatus = {}
    reviewStatus["total_positive"] = reviewListJson["query_summary"]["total_positive"]
    reviewStatus["total_negative"] = reviewListJson["query_summary"]["total_negative"]
    reviewStatus["total_reviews"] = reviewListJson["query_summary"]["total_reviews"]

    myquery = {"appid":appid}
    newvalues = {"$set":reviewStatus}

    myinfo.update_one(myquery, newvalues, upsert = True)

count = 0
countMax = 100000
countTime = datetime.datetime.now()

def CheckAPILimit():
    global count
    global countMax
    global countTime
    if (datetime.datetime.now()- countTime).days>1:
        countTime = datetime.datetime.now()
        count = 0
    count += 1
    return count >= countMax

def getReviewList(appid, cursor):
    reviewListJson = None
    try:
        url = REVIEW_URL.format(appid, urllib.quote_plus(cursor))
        response = urllib2.urlopen(url)
        if response:
            reviewListJson = json.loads(response.read().decode("utf8"))
            if reviewListJson["success"] != 1:
                reviewListJson = None
    except Exception as e:
        print e
    return reviewListJson

def getOneAppReview(appid, cursor, findSameReviewAndBreak = False):
    #根据AppID，游标来查询，返回下一个游标，如果出问题，则返回None
    #如果 findSameReviewAndBreak为真，当找到一样ID的Review时，返回当前游标而不是继续下去
    if CheckAPILimit():
        print "API Limit Break"
        return -1

    print "try get reviews appid:"+str(appid)+"::"+str(cursor)

    reviewListJson = getReviewList(appid, cursor)

    if cursor == "*":
        updateTotalReview(appid, reviewListJson)

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
    return reviewListJson["cursor"]

def checkFindSameReviewAndBreak(appidInfo):
    #如果之前有update，那么找到相同的review就结束并返回
    result = False
    if "review_update_time" in appInfo and (datetime.datetime.now()- appInfo["review_update_time"]).days < 30:
        print "already get when {0}".format(appInfo["review_update_time"])
        result = True
    return result

def getAppReview(appidInfo):
    findSameReviewAndBreak = checkFindSameReviewAndBreak(appidInfo)
    
    if "total_reviews" not in appInfo or findSameReviewAndBreak:
        # 临时处理，目前只要有review就直接返回，也不处理appinfo不全的
        return None
    
    appid = appInfo['appid']
    reviewNum = appInfo["total_reviews"]
    print "appid:{0}:review:{1}:{2}".format(appid,reviewNum,time.strftime('%Y-%m-%d %H:%M:%S'))

    cursor = "*"
    while True:
        newCursor = getOneAppReview(appid, cursor, findSameReviewAndBreak)
        if newCursor == None:
            return None
        if newCursor == -1:
            return -1
        if newCursor == cursor:
            myinfo.update_one({"appid":appid}, {"$set":{'review_update_time': datetime.datetime.now()}})
            return None

        cursor = newCursor

def getAppInfos():
    appInfos = [x for x in myinfo.find({"type":"game","total_reviews":{"$gt":40000,"$lt":50000}})]
    #appInfos = [x for x in myinfo.find({"type":"game","total_reviews":{"$gt":2000,"$lt":12000},"last_update_time":{"$exists":True}})]
    #appInfos = [x for x in myinfo.find({"type":"game","total_reviews":{"$exists":True} })]
    #appInfos = [x for x in myinfo.find({"appid":1076600})]
    appInfosLen = len(appInfos)
    reviewsCount = sum([info["total_reviews"] for info in appInfos])
    print "{0} app will get {1} reviews, take {2} days to run".format(appInfosLen, reviewsCount,reviewsCount/1000000/100.0)
    return appInfos

if __name__ == '__main__':
    count = 0
    appInfos = getAppInfos()
    appInfosLen = len(appInfos)
    for i,appInfo in enumerate(appInfos):
        print "====appid now {0} is {1}/{2}=====".format(appInfo['appid'], i, appInfosLen)
        appLimit = getAppReview(appInfo)
        if appLimit == -1:
            break
