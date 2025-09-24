# -*- coding:utf8 -*-
"""
本脚本用于从玩家已经拥有的steam游戏中找到特定类型的游戏
支持中文，一定的好评的游戏
且游玩时间少于10分钟
"""
from conf import *
import json
import datetime

STEAM_API_KEY = "CC7C14E1120AE700523D2D77F03693F1"
STEAM_USER_ID = "76561198140138947"
OWNED_GAME_URL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&format=json".format(STEAM_API_KEY,STEAM_USER_ID)

IGNORE_GAME = {
865610,#**Tails Noir** has 2042 positive reviews.
339400,#**Runestone Keeper** has 2064 positive reviews.
1740300,#**Smushi Come Home** has 2070 positive reviews.
1372320,#**Cloud Gardens** has 2098 positive reviews.
1176710,#**Space Crew: Legendary Edition** has 2137 positive reviews.
1712840,#**Tiny Tina's Assault on Dragon Keep: A Wonderlands One-shot Adventure** has 2223 positive reviews.
1172650,#**INDUSTRIA** has 2236 positive reviews.
969760,#**Omno** has 2237 positive reviews.
485460,#**The Banner Saga 3** has 2276 positive reviews.
585690,#**Minimalism** has 2282 positive reviews.
1501610,#**Nova Lands** has 2288 positive reviews.
1220150,#**Blue Fire** has 2311 positive reviews.
1221250,#**NORCO** has 2343 positive reviews.
1354830,#**Cat Cafe Manager** has 2391 positive reviews.
898890,#**Endling - Extinction is Forever** has 2448 positive reviews.
421170,#**Indivisible** has 2473 positive reviews.
1287840,#**Disciples: Liberation** has 2603 positive reviews.
699920,#**Despotism 3k** has 2851 positive reviews.
1265820,#**Fights in Tight Spaces** has 2899 positive reviews.
802890,#**Muv-Luv Alternative (マブラヴ オルタネイティヴ)** has 2930 positive reviews.
1054510,#**Survivalist: Invisible Strain** has 2960 positive reviews.
684450,#**Surviving the Aftermath** has 3050 positive reviews.
1599020,#**Tinykin** has 3050 positive reviews.
466130,#**White Day: A Labyrinth Named School** has 3149 positive reviews.
732370,#**Juicy Realm** has 3170 positive reviews.
281640,#**The Banner Saga 2** has 3226 positive reviews.
555000,#**GOAT OF DUTY** has 3476 positive reviews.
1038250,#**DIRT 5** has 3539 positive reviews.
1130410,#**Cyber Hook** has 3643 positive reviews.
729000,#**Wytchwood** has 3670 positive reviews.
1534980,#**Terminus: Zombie Survivors** has 3671 positive reviews.
1590910,#**Forgive Me Father** has 3878 positive reviews.
618140,#**Barro** has 3897 positive reviews.
712730,#**SIMULACRA** has 3934 positive reviews.
1112890,#**Calico** has 4148 positive reviews.
1118240,#**Lake** has 4161 positive reviews.
1293180,#**SuchArt: Genius Artist Simulator** has 4198 positive reviews.
1213700,#**Spirit of the North** has 4320 positive reviews.
1042490,#**Call of the Sea** has 4398 positive reviews.
1144770,#**SLUDGE LIFE** has 4433 positive reviews.
857980,#**Void Bastards** has 4511 positive reviews.
1227650,#**Bang-On Balls: Chronicles** has 4533 positive reviews.
461950,#**Beat Cop** has 4585 positive reviews.
404680,#**Hob** has 4608 positive reviews.
1058650,#**Beyond The Wire** has 4764 positive reviews.
1507190,#**Machinika: Museum** has 5081 positive reviews.
757320,#**Atomicrops** has 5083 positive reviews.
981430,#**Gordian Quest** has 5128 positive reviews.
1119980,#**In Sound Mind** has 5369 positive reviews.
1218210,#**Coromon** has 5465 positive reviews.
1271700,#**HOT WHEELS UNLEASHED™** has 5638 positive reviews.
2478970,#**Tomb Raider I-III Remastered Starring Lara Croft** has 6006 positive reviews.
640590,#**The LEGO® NINJAGO® Movie Video Game** has 6074 positive reviews.
674500,#**Total Tank Simulator** has 6318 positive reviews.
1016120,#**PGA TOUR 2K21** has 6372 positive reviews.
970830,#**The Dungeon Of Naheulbeuk: The Amulet Of Chaos** has 6474 positive reviews.
4560,#**Company of Heroes - Legacy Edition** has 6507 positive reviews.
999220,#**Amnesia: Rebirth** has 6608 positive reviews.
1199030,#**Tainted Grail: Conquest** has 6773 positive reviews.
290300,#**Rebel Galaxy** has 6849 positive reviews.
960690,#**One Step From Eden** has 6892 positive reviews.
897450,#**The Survivalists** has 6975 positive reviews.
1136160,#**Internet Cafe Simulator** has 7171 positive reviews.
539470,#**Police Stories** has 7313 positive reviews.
20,#**Team Fortress Classic** has 7566 positive reviews.
1272320,#**Diplomacy is Not an Option** has 7610 positive reviews.
1202900,#**Assemble with Care** has 7637 positive reviews.
407530,#**ARK: The Survival Of The Fittest** has 7749 positive reviews.
973580,#**Sniper Ghost Warrior Contracts** has 8827 positive reviews.
312670,#**Strange Brigade** has 8974 positive reviews.
616560,#**Ultimate Epic Battle Simulator** has 9285 positive reviews.
792300,#**The Beast Inside** has 9304 positive reviews.
1286350,#**BPM: BULLETS PER MINUTE** has 10026 positive reviews.
1188930,#**Chrono Ark** has 10757 positive reviews.
826630,#**Iron Harvest** has 10848 positive reviews.
280,#**Half-Life: Source** has 11047 positive reviews.
280160,#**Aragami** has 11463 positive reviews.
489630,#**Warhammer 40,000: Gladius - Relics of War** has 11495 positive reviews.
428690,#**Youtubers Life** has 11901 positive reviews.
222480,#**Resident Evil Revelations** has 12115 positive reviews.
738520,#**Breathedge** has 12465 positive reviews.
1318690,#**shapez** has 12947 positive reviews.
1150440,#**Aliens: Dark Descent** has 13094 positive reviews.
237990,#**The Banner Saga** has 13783 positive reviews.
903950,#**Last Oasis** has 14767 positive reviews.
1496790,#**Gotham Knights** has 15118 positive reviews.
289130,#**ENDLESS™ Legend** has 15540 positive reviews.
882100,#**XCOM®: Chimera Squad** has 16200 positive reviews.
895870,#**Project Wingman** has 17721 positive reviews.
681280,#**Descenders** has 17736 positive reviews.
374040,#**Portal Knights** has 18017 positive reviews.
517630,#**Just Cause 4 Reloaded** has 18519 positive reviews.
1291340,#**Townscaper** has 19979 positive reviews.
1127400,#**Mindustry** has 20517 positive reviews.
1149620,#**Gas Station Simulator** has 21624 positive reviews.
1599600,#**PlateUp!** has 21655 positive reviews.
287290,#**Resident Evil Revelations 2** has 22176 positive reviews.
1252330,#**DEATHLOOP** has 22199 positive reviews.
519860,#**DUSK** has 22566 positive reviews.
447020,#**Farming Simulator 17** has 23256 positive reviews.
1449560,#**Metro Exodus** has 23961 positive reviews.
304240,#**Resident Evil** has 24213 positive reviews.
640820,#**Pathfinder: Kingmaker — Enhanced Plus Edition** has 25831 positive reviews.
3240220,#**Grand Theft Auto V Enhanced** has 26083 positive reviews.
57300,#**Amnesia: The Dark Descent** has 32059 positive reviews.
1557740,#**ROUNDS** has 33600 positive reviews.
967050,#**Pacify** has 35973 positive reviews.
312520,#**Rain World** has 38390 positive reviews.
972660,#**Spiritfarer®: Farewell Edition** has 42677 positive reviews.
4500,#**S.T.A.L.K.E.R.: Shadow of Chernobyl** has 44261 positive reviews.
774361,#**Blasphemous** has 45204 positive reviews.
285900,#**Gang Beasts** has 50821 positive reviews.
219640,#**Chivalry: Medieval Warfare** has 54048 positive reviews.
20900,#**The Witcher: Enhanced Edition Director's Cut** has 55568 positive reviews.
1030840,#**Mafia: Definitive Edition** has 76474 positive reviews.
683320,#**GRIS** has 79343 positive reviews.

1158310,#**Crusader Kings III** has 109143 positive reviews.
552500,#**Warhammer: Vermintide 2** has 112620 positive reviews.
526870,#**Satisfactory** has 220768 positive reviews.
48700,#**Mount & Blade: Warband** has 162087 positive reviews.
49520,#**Borderlands 2** has 268827 positive reviews.
960090,#**Bloons TD 6** has 340126 positive reviews.
346110,#**ARK: Survival Evolved** has 607012 positive reviews.
945360,#**Among Us** has 641883 positive reviews.
}
TOTAL_REVIEWS_MIN = 2000
TOTAL_REVIEWS_MAX = 10000000

if __name__ == '__main__':
    response = send_req(OWNED_GAME_URL)
    if response:
        owned_game = set()
        already_played = set()
        for x in response["response"]["games"]:
            owned_game.add(x["appid"])
            if(x["playtime_forever"] > 10):
                already_played.add(x["appid"])

    owned_game -= already_played
    owned_game -= IGNORE_GAME
    game_support_chinese = []
    for k in owned_game:
        info = myinfo.find_one({
            "appid":k,
            "supported_languages":{"$regex":"Chine"},
            "total_positive":{"$gt":TOTAL_REVIEWS_MIN,"$lt":TOTAL_REVIEWS_MAX},
            "is_free":False
            })
        if info:
            game_support_chinese.append((k,info))
    game_support_chinese.sort(key=lambda x:x[1][u'total_positive'])

    for game in game_support_chinese:
        try:
            print("{0},#**{1}** has {2} positive reviews.".format(game[0], game[1][u"name"], game[1]["total_positive"]))
        except Exception as e:
            print(game)
            print(e)
    print(len(game_support_chinese))