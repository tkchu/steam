import redis

r_cli = redis.StrictRedis(host='localhost', port=6379, db=0)

def is_checked(userID):
    if r_cli.sismember("checked", userID) == 1:
        return True
    else:
        return False

def get_10_need_check():
    return r_cli.srandmember("need_check", 10)

def set_checked(userID):
    r_cli.sadd("checked", userID)
    r_cli.srem("need_check", userID)

def set_need_check(userID):
    if r_cli.sismember("checked", userID) != 1:
        r_cli.sadd("need_check", userID)

def set_friend_list(userID, friend_list):
    data = {'user':userID, 'friends': friend_list}
    m_collection.insert(data)
