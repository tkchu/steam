# -*- coding:utf8 -*-
"""
本脚本用于获取steam游戏列表及基本信息
"""
from conf import *
import json
import datetime

APPLIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
DETAIL_URL = "http://store.steampowered.com/api/appdetails/?appids={0}&cc=us&l=en"

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

def getNeedUpdateAppids():
    pass_time = datetime.datetime.now() - datetime.timedelta(days = 365) 
    #没有更新过的游戏要更新，上次更新到今天超过365天的游戏也会列入更新
    result = [info["appid"] for info in myinfo.find({
        "type":"game",
        "last_update_time":{"$lt": pass_time}
        })]
    return result

def updateDetail(appid, detail):
    newInfo = {"appid":appid,"last_update_time":datetime.datetime.now()}
    oldInfo = myinfo.find_one({"appid":appid})
    if not detail:
        try:
            if not oldInfo:
                newInfo = merge_two_dicts(newInfo, {"appid":appid,"type":False,"try_times":1}) # try_times已经尝试过的次数
                myinfo.insert_one(newInfo)
                print "insert_False_detail:" + str(appid)
            elif oldInfo['type'] == False:
                myinfo.update_one({"appid":appid}, {'$inc': {'try_times': 1}})
                print "update_False_detail:" + str(appid)
            else:
                print "update_None_detail:" + str(appid)
        except Exception as e:
            print appid,e
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
            print appid, e

def main():
    allappids = set([x for x in getAppids()])
    #先处理新的游戏
    print "----INSERTING NEW----"
    allnew = allappids - set(myinfo.distinct("appid"))
    for i, appid in enumerate(allnew):
        print "====new appid:{0}:{1}/{2}====".format(appid,i,len(allnew))
        detail = getDetail(appid)
        updateDetail(appid, detail)
    #然后更新已有的游戏
    print "----UPDATEING OLD----"
    allupdate =allappids.intersection(set(getNeedUpdateAppids()))
    for i, appid in enumerate(allupdate):
        print "====update appid:{0}:{1}/{2}====".format(appid,i,len(allupdate))
        detail = getDetail(appid)
        updateDetail(appid, detail)

if __name__ == '__main__':
    main()
