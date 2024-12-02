# -*- coding:utf8 -*-
import requests
import time
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

mydb = myclient["test"]
myinfo = mydb['info']
myreview = mydb['review']
mydata = mydb['data']

lastTime = time.time()
waitTime = 5*60.0/195

def send_req(url, wait = True):
    global lastTime
    global waitTime
    retryTimes = 1
    response = None
    result = None

    while retryTimes > 0:
        try:
            response = requests.get(url)
            if response:
                result = response.json()
        except Exception as e:
            print(e)
            print(time.strftime('%Y-%m-%d %H:%M:%S'))

        sleepTime = lastTime + waitTime - time.time()
        if(sleepTime > 0 and wait):
            print(time.strftime('%Y-%m-%d %H:%M:%S sleep for' + str(sleepTime)))
            time.sleep(sleepTime)
        lastTime = time.time()
        retryTimes -= 1

    return result

def merge_two_dicts(x, y):
    if not x:
        return y
    elif not y:
        return x

    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z