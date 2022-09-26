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

    total_review = reviewStatus["total_reviews"]
    print "appid:{0}:review:{1}:{2}".format(appid,total_review,time.strftime('%Y-%m-%d %H:%M:%S'))
    return total_review

count = 0
countMax = 100000
countTime = datetime.datetime.now()

def CheckAPILimit():
    return False
    global count, countMax, countTime
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

appcount = 0
appreview = 0
def getOneAppReview(appid, cursor, findSameReviewAndBreak = False):
    #根据AppID，游标来查询，返回下一个游标，如果出问题，则返回None
    #如果 findSameReviewAndBreak为真，当找到一样ID的Review时，返回当前游标而不是继续下去
    if CheckAPILimit():
        print "API Limit Break"
        return -1

    reviewListJson = getReviewList(appid, cursor)
    if not reviewListJson:
        return None

    global appcount,appreview
    if cursor == "*":
        appcount = 0
        appreview = updateTotalReview(appid, reviewListJson)
    appcount +=1
    print "try get reviews appid:{0}::{1}:{2}/{3}".format(appid,cursor, appcount, (appreview-1)/100+2)

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
    if "review_update_time" in appidInfo and (datetime.datetime.now()- appidInfo["review_update_time"]).days < 30:
        print "already get when {0}".format(appidInfo["review_update_time"])
        result = True
    return result

def getAppReview(appidInfo, cursor="*"):
    findSameReviewAndBreak = checkFindSameReviewAndBreak(appidInfo)
    
    if findSameReviewAndBreak:
        # TEMP临时处理，目前只要有review就直接返回，而不是按道理的一直到找到重复的再返回
        return None
    appid = appidInfo["appid"]

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

def getAppReviewByID(appid, cursor ="*"):
    info = myinfo.find_one({"appid":appid})
    return getAppReview(info,cursor)

def getAppids():
    appInfos = [ x for x in myinfo.find({"type":"game","review_update_time":{"$exists":False}})]
    #appInfos = [ x for x in myinfo.find({"type":"game","review_update_time":{"$exists":False},"is_free":False })]
    #appInfos = [x for x in myinfo.find({"type":"game","total_reviews":{"$gt":2000,"$lt":12000},"last_update_time":{"$exists":True}})]
    #appInfos = [x for x in myinfo.find({"type":"game","total_reviews":{"$exists":True} })]
    #appInfos = [x for x in myinfo.find({"appid":1076600})]
    appids = [x['appid'] for x in appInfos if 'appid' in x]
    return appids

if __name__ == '__main__':
    #getAppReviewByID(730,"AoJ4ibXD3tICfIKeUA==")
    
    count = 0
    appids = sorted(getAppids())
    appidsLen = len(appids)
    for i,appid in enumerate(appids):
        print "====appid now {0} is {1}/{2}=====".format(appid, i, appidsLen)
        appLimit = getAppReviewByID(appid)
        if appLimit == -1:
            break