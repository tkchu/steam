import json
import pymongo
import requests
import shutil
import time

appdetailCollection = pymongo.MongoClient().steam.appdetail
detailCollection = pymongo.MongoClient().steam.detail
list_x = list(appdetailCollection.find())

startTime = time.time()
for ix,x in enumerate(list_x):
    if ix < 12043:
        continue
    appid = str(x["appid"])
    tags = x["tags"]
    if "Visual Novel" in tags:
        try:
            url = detailCollection.find_one({"appid" : appid})["content"][appid]["data"]["header_image"]
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open("./headImage/" + appid + ".jpg", 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
        except Exception as e:
            print(e)
            continue
        if time.time() - startTime < 300 / 200:
            time.sleep(-time.time() + startTime + 300 / 200)
            startTime = time.time()
    print(str(ix) + " / " + str(len(list_x)))