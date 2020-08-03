# -*- coding:utf8 -*-
"""
本脚本用于获取steam游戏的评论
"""
import json
from conf import *
from app import *
from review import *

"""
获得所有动作策略游戏
    appInfos = myinfo.find({'total_reviews':{'$gt':100}})
    i=0
    actionAppids = []
    strategyAppids = []

    for appInfo in appInfos:
        print "appid:" + str(appInfo['appid']) + ":" + str(i) + '/' + str(appInfos.count())
        if "genres" in appInfo:
            for gen in appInfo["genres"]:
                if "description" in gen:
                    if gen["description"] == "Action":
                        actionAppids.append(appInfo["appid"])
                    if gen["description"] == "Strategy":
                        strategyAppids.append(appInfo["appid"])
        i+=1
"""

"""
添加review_id
i = 0
for review in myreview.find({"review_id":{"$exists":False}}):
    print str(i)
    review["review_id"]= str(review['appid'])+":"+str(review["recommendationid"])
    myreview.save(review)
    i+=1
"""
"""
appids = [258050, 804870, 506540, 327690, 1241100, 413710, 786450, 512020, 1227780, 331810, 806950, 204840, 249870, 475180, 251570, 589870, 1048100, 489520, 300040, 1049950, 761910, 622650, 204860, 884090, 360510, 700480, 719200, 856130, 315460, 63500, 290890, 495580, 342370, 204880, 319570, 546900, 311310, 835670, 835671, 919640, 1015140, 727130, 424030, 436320, 366690, 297060, 1200230, 6250, 616560, 978270, 535230, 663670, 1130620, 333950, 80000, 409730, 703510, 342150, 1144970, 539330, 360590, 764050, 356500, 329070, 829590, 905370, 317600, 637090, 895140, 1127110, 336040, 271730, 393390, 344240, 1154760, 960690, 1218740, 217270, 65720, 302590, 1132730, 715310, 735420, 331970, 327030, 102600, 65740, 915490, 774861, 438480, 270550, 1081560, 286940, 382330, 1190110, 444640, 960740, 315430, 575720, 260330, 508140, 243950, 343100, 389160, 319730, 65780, 473470, 400180, 553210, 299260, 212010, 6400, 243970, 956680, 444460, 252170, 755980, 300760, 444690, 364820, 251950, 581910, 657690, 534820, 475430, 98600, 207150, 1185160, 1124660, 983350, 293940, 571710, 1094710, 400660, 624970, 299340, 244450, 782670, 991780, 416080, 1076280, 745810, 884620, 269710, 688470, 220900, 299360, 307600, 280930, 719590, 305510, 369000, 297020, 268650, 547180, 201070, 774511, 573160, 432500, 293240, 780670, 455040, 455041, 334210, 233860, 1116550, 967050, 595770, 600460, 223630, 369040, 428100, 389530, 371100, 333210, 516510, 412400, 285090, 1179730, 680360, 204530, 4530, 1151390, 531530, 664000, 420290, 371140, 580040, 1241550, 4560, 512470, 473560, 440740, 905690, 914110, 244770, 1102310, 340460, 340050, 475630, 905640, 503210, 252750, 364630, 285190, 748040, 1252780, 621070, 1093720, 289300, 261550, 873220, 1063450, 342560, 529840, 336420, 209670, 1167910, 404010, 404011, 404012, 404013, 404014, 404015, 474890, 911930, 647740, 372490, 270910, 1104450, 4520, 840260, 586310, 887370, 325730, 236110, 1067600, 301650, 98900, 350810, 262750, 787040, 1106530, 421060, 338540, 639600, 29800, 633460, 461430, 729720, 260730, 502400, 1282690, 844420, 318230, 508550, 1135240, 594570, 335180, 1047180, 451010, 322190, 246420, 314010, 215710, 594591, 1262240, 344740, 316430, 606890, 649900, 754350, 294860, 259870, 301750, 508600, 979060, 625340, 1006270, 440900, 107200, 1137440, 662210, 342570, 645830, 46540, 207650, 922320, 686810, 330460, 654050, 359140, 443110, 1075950, 740080, 349310, 248570, 1071870, 492290, 2820, 824070, 479020, 389900, 711440, 965080, 1209110, 387870, 1209120, 1209121, 248610, 515040, 265000, 205610, 465710, 467760, 226100, 4920, 988980, 1022780, 936490, 375620, 234310, 275470, 926540, 416590, 840130, 432980, 268870, 346970, 1189690, 385890, 594490, 555880, 572220, 473970, 1192820, 652150, 369530, 589290, 1008510, 781190, 314860, 551820, 551821, 107410, 347030, 359320, 760730, 331930, 652190, 953250, 23460, 416680, 1293230, 1180600, 1002430, 744950, 375750, 696140, 723790, 803800, 65700, 805850, 951260, 236510, 505210, 289760, 602960, 363490, 11240, 627690, 210770, 488430, 254960, 684200, 277490, 771060, 794110, 396280, 572410, 441340, 269310, 457730, 1238020, 812040, 242860, 521230, 93200, 291860, 386070, 1227800, 1025050, 443420, 1307680, 347170, 1158180, 1158181, 658470, 252970, 269490, 216110, 404530, 314420, 294750, 879670, 328760, 742460, 366090, 201790, 91200, 351300, 404550, 275530, 779340, 342200, 314450, 236730, 257120, 412770, 572520, 564330, 33900, 228200, 244850, 302270, 638070, 291960, 9340, 543870, 1174720, 654470, 33930, 1121420, 1151170, 1074320, 1074321, 431250, 629910, 345240, 666820, 543900, 345260, 207730, 235720, 33970, 42170, 453820, 1049790, 396480, 91330, 625860, 1131720, 777880, 758990, 394450, 386260, 1025240, 510500, 253150, 427240, 622460, 1033450, 247020, 351470, 343280, 621810, 562420, 494840, 1195220, 568570, 304380, 844330, 451840, 539470, 1084680, 914700, 957710, 743640, 388370, 1076500, 541230, 238870, 445720, 111900, 814370, 269190, 1147100, 269610, 17710, 286000, 525620, 412990, 406850, 224580, 513590, 285580, 17740, 339280, 617810, 324520, 214360, 694500, 570, 322910, 654690, 348730, 370020, 916840, 793490, 206190, 853360, 1142130, 652660, 332350, 265590, 298360, 617850, 15740, 734590, 357760, 392580, 15750, 755080, 523660, 617870, 965220, 357780, 310510, 329110, 1058200, 809540, 363930, 448070, 329130, 736220, 345330, 415150, 345520, 368050, 1162680, 496240, 785850, 931260, 335830, 341300, 230860, 1308110, 91600, 587000, 343630, 1275350, 327130, 523740, 210170, 1244640, 595430, 536040, 1092860, 271850, 345580, 298480, 1266600, 259570, 693750, 398840, 341500, 251390, 288260, 802390, 415660, 468490, 204300, 427950, 63000, 703880, 1158690, 1232420, 273960, 296490, 449530, 400020, 1084980, 1000030, 503350, 577080, 386620, 1025600, 1068640, 618050, 275700, 601670, 798280, 259660, 302670, 243280, 484950, 227940, 331360, 508180, 779880, 310890, 1033840, 462440, 268200, 618100, 497940, 439930, 312960, 384960, 951940, 551190, 251530, 874460, 681330, 814740, 419480, 278810, 620190, 509600, 332400, 206500, 685340, 591530, 1132210, 798390, 505460, 978620, 294590, 593600, 423620, 446150, 18120, 499660, 890570, 22230, 1140440, 790820, 947940, 741670, 1226470, 286440, 524010, 331500, 416040, 665330, 313080, 436180, 325370, 491260, 380670, 574080, 241410, 530180, 1216470, 288520, 1263370, 204560, 444180, 662830, 558870, 224900, 493340, 423710, 788260, 283270, 554791, 1237980, 878380, 1054510, 323380, 511800, 44340, 534330, 534331, 782140, 773951, 228320, 708420, 409910, 812870, 919370, 839500, 423760, 640850, 716630, 333660, 1021790, 268130, 366440, 958320, 615400, 626550, 676500, 857980, 8170, 622470, 252270, 244750, 505740, 651150, 1247120, 1003160, 227220, 978840, 408900, 367600, 1066920, 395180, 591790, 563120, 645790, 1032120, 1262580, 348490, 444350, 6080, 222880, 315330, 737270, 718790, 331720, 447820, 753610, 858060, 108500, 202710, 1167320, 324260, 690140, 388090, 264160, 451920, 572430, 262120, 98300, 407530, 225260, 285010, 393200, 1275890, 489460, 303470, 438020, 1070330, 935930, 559100, 1236990]

reviewnum = []

for appid in appids:
    info = myinfo.find_one({"appid":appid})
    reviewnum.append((appid, info['total_reviews'], info['name']))


def myFunc(e):
  return e[1]

reviewnum.sort(key=myFunc)
print reviewnum
"""
"""
mydb = myclient["remote"]
mydb2 = myclient["steam"]
myreview = mydb['review']
myreview2 = mydb2['review']

i=0
for r in myreview.find():
    try:
        myreview2.insert_one(r)
    except Exception as e:
        print e
    i+=1
    print i
"""
print sum([x['total_reviews'] for x in myinfo.find() if 'total_reviews' in x])
