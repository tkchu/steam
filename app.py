# -*- coding:utf8 -*-
"""
本脚本用于获取steam游戏列表及基本信息
"""
from conf import *
import json
import datetime

APPLIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
DETAIL_URL = "http://store.steampowered.com/api/appdetails/?appids={0}"

def getAppids():
    """获取所有steam游戏列表"""
    response = send_req(APPLIST_URL)
    if not response:
        return
    applistJson = json.loads(response.decode("utf8"))
    appids = [i['appid'] for i in applistJson["applist"]["apps"]]
    return appids

def getDetail(appid):
    """获取某一steam游戏简介
    name:"PLAYERUNKNOWN'S BATTLEGROUNDS"
    steam_appid:578080
    """
    response = send_req(DETAIL_URL.format(appid))
    if not response:
        return
    content = json.loads(response.decode("utf8"))
    appid = int([k for k in content.keys()][0])
    result = [v for v in content.values()][0]
    result["appid"] = appid
    if result['success']:
        return result['data']
    else:
        return None

def checkNeedUpdateAppid(appid):
    oldInfo = myinfo.find_one({"appid": appid})

    if not oldInfo:
        return True
    if oldInfo and "appid" not in oldInfo:
        return True
    if oldInfo and "type" in oldInfo and oldInfo["type"] == "game":
        if "last_update_time" in oldInfo and (datetime.datetime.now() - oldInfo['last_update_time']).days > 30:
            return True
        if "price_overview" in oldInfo and "currency" in oldInfo["price_overview"] and oldInfo["price_overview"]["currency"] != "USD":
            #return True
            pass
    
    return False

    if oldInfo and "type" in oldInfo and oldInfo["type"] == False:
    # 如果之前获取失败了，那就不用重新获取了
        #print str(appid) + ": False"
        return False
    elif oldInfo and "type" in oldInfo and oldInfo["type"] != "game":
    # 如果之前获取过这个不是游戏，那就不用重新获取了
        #print str(appid) + ": No game"
        return False
    elif oldInfo and 'try_times' in oldInfo and oldInfo['try_times']>=5:
    # 如果尝试的次数很多，那也别试了
        #print str(appid) + ":already try " + str(oldInfo['try_times']) + " times"
        return False
    elif oldInfo and "last_update_time" in oldInfo and (datetime.datetime.now() - oldInfo['last_update_time']).days < 30:
    # 如果上次获取是在一周以内，那也别获取了
        #print str(appid) + ":last_update_time" + str(oldInfo['last_update_time']) 
        return False

    return False

def updateDetail(appid, detail):
    newInfo = {"appid":appid,"last_update_time":datetime.datetime.now()}
    oldInfo = myinfo.find_one({"appid":appid})
    if not detail:
        try:
            if not oldInfo:
                newInfo = merge_two_dicts(newInfo, {"appid":appid,"type":False,"try_times":1})
                myinfo.insert_one(newInfo)
                print "insert_False_detail:" + str(appid)
            elif oldInfo['type'] == False:
                myinfo.update_one({"appid":appid}, {'$inc': {'try_times': 1}})
                print "update_False_detail:" + str(appid)
        except Exception as e:
            print e
    else:
        newInfo = merge_two_dicts(newInfo, detail)
        try:
            if oldInfo:
                myinfo.update_one({"appid":appid},{"$set":newInfo},upsert=True)
                print "update_Old_Info:" + str(appid)
            else:
                myinfo.insert_one(newInfo)
                print "insert_New_Info:" + str(appid)
        except Exception as e:
            print e

def mainFindNew():
    allappids = set([x for x in getAppids()])
    allexist = set(myinfo.distinct("appid"))
    allappids = allappids - allexist

    for i, appid in enumerate(allappids):
        print "====appid:{0}:{1}/{2}====".format(appid,i,len(allappids))
        detail = getDetail(appid)
        updateDetail(appid, detail)

def mainFixAll():
    allappids = [x for x in getAppids() if checkNeedUpdateAppid(x)]

    for i, appid in enumerate(allappids):
        print "====appid:{0}:{1}/{2}====".format(appid,i,len(allappids))
        detail = getDetail(appid)
        updateDetail(appid, detail)

if __name__ == '__main__':
    mainFindNew()
