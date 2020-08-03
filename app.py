# -*- coding:utf8 -*-
"""
本脚本用于获取steam游戏列表及基本信息
"""
from conf import *
import json

APPLIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
DETAIL_URL = "http://store.steampowered.com/api/appdetails/?appids={0}"
REVIEW_URL = "https://store.steampowered.com/appreviews/{0}?json=1&language=all&filter=recent&start_offset={1}&num_per_page={2}&review_type=all&purchase_type=all"

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

def getStatus(appid):
    """获取某一steam游戏的review简介
    total_positive:640530,
    total_negative:40469,
    total_reviews:680999
    """
    response = send_req(REVIEW_URL.format(appid, 0, 0))
    if not response:
        return
    reviewListJson = json.loads(response.decode("utf8"))
    if reviewListJson["success"] == 1:
        reviewListJson["query_summary"]["appid"] = appid
        return reviewListJson["query_summary"]
    else:
        return None

if __name__ == '__main__':
    allappids = getAppids()
    for i, appid in enumerate(allappids):
        print str(appid) + ":" + str(i) + "/" + str(len(allappids))
        oldInfo = myinfo.find_one({"appid": appid})
        if oldInfo and "type" in oldInfo and oldInfo["type"] != False:
        # 如果已经有了，那就不用重新获取了
            continue
        if oldInfo and 'try_times' in oldInfo and oldInfo['try_times']>5:
        # 如果尝试的次数很多，那也别试了
            print str(appid) + ":" + str(i) + "/" + str(len(allappids)) + ":already try " + str(oldInfo['try_times']) + " times"
            continue
        detail = getDetail(appid)
        status = getStatus(appid)
        if not detail or not status:
            try:
                if not oldInfo:
                    newInfo = {"appid":appid,"type":False,"try_times":1}
                    myinfo.insert_one(newInfo)
                    print("insert_one:" + str(appid))
                elif oldInfo['type'] == False:
                    myinfo.update_one({"appid":appid}, {'$inc': {'try_times': 1}})
                    print("update_one:" + str(appid))
            except Exception as e:
                pass

        else:
            newInfo = merge_two_dicts(detail,status)
            try:
                if oldInfo:
                    if oldInfo['type'] == False:
                        myinfo.delete_one({"appid":appid})
                        myinfo.insert_one(newInfo)
                else:
                    myinfo.insert_one(newInfo)
                print("insert_one:" + str(appid))
            except Exception as e:
                pass