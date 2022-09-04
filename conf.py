# -*- coding:utf8 -*-
import urllib2
import time
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

mydb = myclient["remote"]
myinfo = mydb['info']
myreview = mydb['review']

lastTime = time.time()
waitTime = 5*60.0/195

def send_req(url):
    global lastTime
    global waitTime
    retryTimes = 1
    response = None
    while retryTimes > 0:
        sleepTime = lastTime + waitTime - time.time()
        if(sleepTime > 0):
            print(time.strftime('%Y-%m-%d %H:%M:%S sleep for' + str(sleepTime)))
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
            print(e)
            print(time.strftime('%Y-%m-%d %H:%M:%S'))
        retryTimes -= 1

def merge_two_dicts(x, y):
    if not x:
        return y
    elif not y:
        return x

    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z