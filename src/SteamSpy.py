# -*- coding:utf8 -*-
import time
import pymongo
import json
import lxml
from selenium import webdriver

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
myapp = myclient["steam"]['apps']
myreview = myclient["steam"]['reviews']

SPY_URL = "https://steamspy.com/api.php?request=appdetails&appid={0}"

browser = webdriver.Chrome()

def getAppSpy(appid):
    try:
        browser.get(SPY_URL.format(appid))
        retryTimes = 10
        while retryTimes > 0:
            try:
                time.sleep(1)
                responseJson = json.loads(browser.page_source[84:-20])
                addSpyToMongo(responseJson)
                break
            except Exception as e:
                print(e)
                retryTimes -= 1
    except Exception as e:
        pass

def addSpyToMongo(spy):
    myapp.update_one({'appid':spy["appid"]}, { "$set":
    {
        "spy":spy
    } }, upsert = True)

if __name__ == '__main__':
    for app in myapp.find({"spy":{"$exists":False}}):
        getAppSpy(app['appid'])