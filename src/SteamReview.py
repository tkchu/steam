# -*- coding:utf8 -*-
import urllib2
import time
import pymongo
import json

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
myapp = myclient["steam"]['apps']
myreview = myclient["steam"]['reviews']

lastTime = time.time()
waitTime = 5*60.0/300

def send_req(url):
    global lastTime
    global waitTime
    retryTimes = 1
    response = None
    while retryTimes > 0:
        sleepTime = lastTime + waitTime - time.time()
        if(sleepTime > 0):
            #print(time.strftime('%Y-%m-%d %H:%M:%S sleep for' + str(sleepTime)))
            time.sleep(sleepTime)
        lastTime = time.time()

        try:
            response = urllib2.urlopen(url)
            if response:
                return response.read()
            else:
                return None
        except Exception as e:
            #time.sleep(15)
            #print(e)
            #print(time.strftime('%Y-%m-%d %H:%M:%S'))
            pass
        retryTimes -= 1

APPLIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
def getAppids():
    """获取所有steam游戏列表"""
    response = send_req(APPLIST_URL)
    if not response:
        return
    applistJson = json.loads(response.decode("utf8"))
    addAppToMongo(applistJson["applist"]["apps"])

REVIEW_URL = "https://store.steampowered.com/appreviews/{0}?json=1&language=all&filter=all&num_per_page=100&day_range=9223372036854775807&review_type=all&purchase_type=all&cursor={1}"
def getReviews(appid, cursor = '*', justSummary = False):
    while True:
        myapp.update_one({'appid':appid}, { "$set": { "cursor": cursor } })
        #print str(appid) + " : " + cursor
        try:
            response = send_req(REVIEW_URL.format(appid, cursor))
            responseJson = json.loads(response.decode("utf8"))
            if responseJson["success"] == 1:
                if cursor == "*":
                    addReviewSummaryToMongo(appid, responseJson["query_summary"])
                    if justSummary:
                        return
                for review in responseJson["reviews"]:
                    review["appid"] = appid
                    addReviewToMongo(review)
                if responseJson["query_summary"]["num_reviews"] < 100:
                    break
                cursor = responseJson["cursor"]
            else:
                break
        except Exception as e:
            break

def addReviewSummaryToMongo(appid, review_summary):
    myapp.update_one({'appid':appid}, { "$set":
        {
            "review_score_desc":review_summary["review_score_desc"], #评测分数描述。
            "total_positive":review_summary["total_positive"], #正面评测的总数。
            "total_negative":review_summary["total_negative"], #负面评测的总数。
            "total_reviews":review_summary["total_reviews"], #符合查询参数的评测总数。
        } })

def addReviewToMongo(review):
    if myreview.find_one({"recommendationid":review["recommendationid"]}):
        myreview.replace_one({"recommendationid":review["recommendationid"]}, review)
    else:
        myreview.insert_one(review)

def addAppToMongo(applist):
    for app in applist:
        if not myapp.find_one({"appid":app["appid"]}):
            myapp.insert_one(app)

if __name__ == '__main__':
    for i in myapp.find():
        if 'cursor' in i:
            getReviews(i['appid'], i['cursor'])
        else:
            getReviews(i['appid'])