# -*- coding:utf8 -*-
"""爬取玩家好友情况"""
import net
import user

while True:
    need_check = user.get_10_need_check()
    if need_check != []:
        for nc in need_check:
            net.get_player_summary(nc)
            net.get_owned_games(nc)
            friends = net.get_friend_list(nc)

            for friend in friends:
                if not user.is_checked(friend):
                    user.set_need_check(friend)
            user.set_checked(nc)
