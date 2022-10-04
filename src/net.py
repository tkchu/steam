# -*- coding:utf8 -*-
"""
一切与网路相关的数据都从这里获得
获得之后按原样存储到mongodb中
"""

import urllib2
import socket
import json
import pymongo

m_cli = pymongo.MongoClient()
m_db = m_cli.steam

m_player = m_db.player_summary
m_friend = m_db.friend_list
m_achieve = m_db.player_achievement
m_owned = m_db.owned_game

STEAM_KEY = "AF20772EDDAF46342B4D37700FC4BDBC"
SPY_URL = "http://steamspy.com/api.php?request=all"
DETAIL_URL = "http://store.steampowered.com/api/appdetails/?appids=%(appid)s"
GLOBAL_ACHIEVEMENT_PERCENTAGES_URL = "http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid=%(appid)s"
PLAYER_SUMMARIES_URL = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%(STEAM_KEY)s&steamids=%(userid)s"
FRIEND_LIST_URL = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=%(STEAM_KEY)s&steamid=%(userid)s&relationship=friend"
PLAYER_GAME_ACHIEVEMENT_URL = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=%(appid)s&key=%(STEAM_KEY)s&steamid=%(userid)s"
OWNED_GAME_URL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%(STEAM_KEY)s&steamid=%(userid)s"

def send_req(url):
    req=urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    res=urllib2.urlopen(req)
    return res.read()
def get_json_from_url(url):
    """使用urllib下载文件"""
    try:
        jsonContent = send_req(url)
        jsonData = json.loads(jsonContent)
    except Exception as e:
        return {}
    else:
        return jsonData

def get_all_game():
    """从SteamSpy上获得所有游戏的列表"""
    return get_json_from_url(SPY_URL)
def get_game_detail(appid):
    """从Steam上获得游戏的具体信息"""
    data = {
        "appid":appid
    }
    return get_json_from_url(DETAIL_URL % data)
def get_player_summary(userid):
    """获取玩家信息"""
    data = {
        "userid" : userid,
        "STEAM_KEY" : STEAM_KEY
    }
    jsonData = get_json_from_url(PLAYER_SUMMARIES_URL % data)
    m_player.insert({'userid':userid, 'content':jsonData})

def get_friend_list(userid):
    """获取朋友列表"
    friend_list_json
        {}: 这个人的信息是隐藏的
        或者：
        {
            "friendslist":{
                "friends":[
                    {
                        "steamid": int,
                        "relationship": "friend",
                        "friend_since": int,
                    },
                    ...
                ]
            }
        }
    """
    data = {
        "userid" : userid,
        "STEAM_KEY" : STEAM_KEY,
    }
    jsonData = get_json_from_url(FRIEND_LIST_URL % data)
    m_friend.insert({'userid':userid, 'content':jsonData})

    friends = []
    if 'friendslist' in jsonData and 'friends' in jsonData['friendslist']:
        for profile in jsonData['friendslist']['friends']:
            friends.append(profile['steamid'])
    return friends

def get_owned_games(userid):
    """获取拥有的游戏列表"""
    data = {
        "userid" : userid,
        "STEAM_KEY" : STEAM_KEY,
    }
    jsonData = get_json_from_url(OWNED_GAME_URL % data)
    m_owned.insert({'userid':userid, 'content':jsonData})
